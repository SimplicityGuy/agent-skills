---
name: repo-ci-setup
description: Use when setting up or auditing GitHub repo automation - Dependabot config, Dependabot labels, SHA-pinned GitHub Actions workflows, required status checks that block PRs, Node 20 deprecation notices, or rolling the same Dependabot setup out across every repo an owner has. Triggers on "all repos", "fleet sweep", "red dependabot PRs", "dependabot", "dependabot.yml", "required checks", "block PRs", "pin actions", "node20 deprecated", "branch ruleset".
---

# Repo CI Setup

Set up Dependabot, pinned workflows, and required checks that block PRs on a GitHub repo. If your repo settings (rulesets, labels, merge methods) are managed as code, for example with OpenTofu or Terraform, make or record each change there too instead of leaving it as hand-edited drift.

## When to Use

- A new repo needs `.github/dependabot.yml`
- A workflow should block PRs until it passes
- Workflow actions need pinning or bumping
- CI logs show a Node 20 deprecation notice
- Auditing a repo for drift from this baseline

## Dependabot

Use this shape, keeping only the ecosystems the repo actually has:

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
      timezone: "America/Los_Angeles"
    commit-message:
      prefix: "ci"
      include: "scope"
    labels:
      - "dependencies"
      - "ci"
    assignees:
      - "your-github-username"
    groups:
      actions:
        patterns:
          - "*"
```

- Add a `pip` (prefix `deps`, `prefix-development: deps-dev`, label `python`) or other block only when the repo has that manifest. Group production, development, and security updates separately.
- Dependabot cannot update what it does not cover. Note any deliberate gaps in a header comment (for example, compose files, or provider pins owned by another script).

### Labels

The `labels:` list names labels but does not reliably create them, so a missing label means a silently unlabelled PR.

1. Create them on the repo first: `dependencies` color `0366d6`, `ci` color `ededed`, and `python` / `docker` / `javascript` as needed.
2. If repo settings are managed as code, add the labels there so the next apply does not remove them.

## Workflows

- Pin every action to a full commit SHA with the version in a trailing comment, so Dependabot can still bump it:
  `uses: owner/repo@<40-char-sha> # v1.2.3`
- Resolve a tag to its SHA with `gh api repos/OWNER/REPO/git/ref/tags/TAG --jq .object`. If the object type is `tag` (annotated), dereference it with `gh api repos/OWNER/REPO/git/tags/SHA` and use the commit SHA it points to.
- Set `permissions: contents: read` at the top and add `concurrency` with `cancel-in-progress: true` for PR workflows.
- Give each job a short, stable `name:`. The job name is the required-check name, so renaming it later breaks the ruleset.

### Node 20 deprecation notices

The notice names the offending actions. For each, read its `action.yml` and check `runs.using`:

- `node20`: bump to a release that declares `node24` (`actions/checkout` v7 does).
- Still `node20` with no newer release: stop using the action and run the same tool's CLI in a `run:` step with a pinned version.

When replacing an action with its CLI, diff the defaults. Actions often set inputs the CLI does not: for `skill-check` the action defaulted `security-scan` to false while the CLI defaults it on, and the scan failed the job with zero findings until `--no-security-scan` was added. The cause was a missing `SNYK_TOKEN`: the scanner (Snyk Agent Scan) needs an account token and exits non-zero without one. Turning the scan on means adding that token as a repo secret, and fork PRs will not receive it. Read the action's `index.js` to see the exact flags it passes.

## Required Checks That Block PRs

Blocking is a repo ruleset.

1. Get the workflow merged or at least run once, since GitHub only offers checks it has seen.
2. Create the ruleset on the live repo with the REST API: target the default branch (`~DEFAULT_BRANCH`), no bypass actors, rules `deletion`, `non_fast_forward`, `pull_request` (0 required approvals), and `required_status_checks` with one entry per job name and `integration_id` `15368` (GitHub Actions).
3. If repo settings are managed as code, adopt the ruleset there so it does not drift. Make sure your tooling supports `required_status_checks` rules.
4. Remember the consequence: direct pushes to the default branch are blocked, so all changes go through a PR.

## Fleet Sweep

Use when the same Dependabot setup must land on every repo an owner has. Run it from one coordinating session that fans out one agent per repo, then re-checks real state itself, because agent "MERGED" reports are not reliable.

Scope it explicitly: the owners to cover (for example `org-a` and `org-b`), skipping other owners and forks. Enumerate with `gh repo list OWNER --no-archived --source --json name`. Repos whose clone is not local still count, so look them up on GitHub before calling them absent.

The original request, to reuse:

> For all of the repos, please do the following:
> - merge any open Dependabot PRs
> - add a Dependabot configuration that will create 1 PR per ecosystem; one for security issues and one for regular version bumps
> - ensure all repos are configured to run the github workflows on dependabot PRs
>
> Once the PR for the dependabot update configuration is created and green, merge it. Do this for all repos owned by org-a and org-b. Skip any other owners; skip forks too.

Per repo, in order:

1. Merge open Dependabot PRs that are green or have no CI. Do not use `--admin` and do not skip checks.
2. Open a config PR with one version-updates group and one security-updates group per ecosystem the repo actually has, then merge it when green.
3. Confirm workflows run on Dependabot PRs. Dependabot PRs read the **Dependabot** secrets store, not Actions secrets. List what the workflows reference and copy each into Dependabot secrets, using your secrets tooling when you cannot read the value, and never paste values into chat. A secret missing from both stores only matters if its step runs.
4. Create every label the config references, and record them in your settings-as-code if you have any.
5. Investigate each red Dependabot PR to its cause and fix that, not the symptom. Close a PR only when it is superseded by a green one.

Known red-PR causes:

- **`pip` in a uv project.** Dependabot edits `pyproject.toml` but cannot rewrite `uv.lock`, so `uv lock --check` fails and a rebase cannot fix it. Use the `uv` ecosystem.
- **Pinned vendor or license manifests.** Bumps trip files such as `vendor-licenses.mjs` or `THIRD_PARTY_NOTICES.md`. Update the manifest on the Dependabot branch, or ahead of the next bump.
- **Measured version caps.** Ignore minor and major updates for a guarded dependency (for example litellm) and keep patch and security updates. Raising the cap is an operator decision.
- **Shared scanner failures on main.** One pre-existing audit finding turns every PR red. Fix it once in a combined PR.
- **Direct pins that conflict.** For example `pydantic-core` pinned while the parent requires another version. Drop the direct pin.

Finish by re-querying every repo for open PRs and red checks. Dependabot reopens regrouped PRs after a config merge, so a second pass is normal. Report what still needs an operator decision rather than forcing it.

## Verify Before Finishing

- The PR's required checks pass, and the first Dependabot run opens PRs with the expected labels and commit prefix.
- The deprecation notice is gone from the CI log.
- If settings are managed as code, a final plan shows no changes.

## Pitfalls

- Unquoted `description:` values in skill frontmatter break at the first `: `; use a dash or quote the value.
- Merge methods differ per repo, so check which are allowed before running `gh pr merge`. Squash is the safe default.
- Linters are a floor: passing them does not prove a skill or workflow is correct.
