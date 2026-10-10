---
name: repo-ci-setup
description: Use when setting up or auditing GitHub repo automation - Dependabot config, Dependabot labels, SHA-pinned GitHub Actions workflows, required status checks that block PRs, or Node 20 deprecation notices. Triggers on "dependabot", "dependabot.yml", "required checks", "block PRs", "pin actions", "node20 deprecated", "branch ruleset".
---

# Repo CI Setup

Set up Dependabot, pinned workflows, and required checks for a SimplicityGuy repo the way they were done for `agent-skills`, modeled on `homelab`. Repo settings (rulesets, labels, merge methods) are managed as code in `homelab/infra/opentofu/github`, so they are changed there and not by hand in the GitHub UI.

## When to Use

- A new repo needs `.github/dependabot.yml`
- A workflow should block PRs until it passes
- Workflow actions need pinning or bumping
- CI logs show a Node 20 deprecation notice
- Auditing a repo for drift from this baseline

## Dependabot

Copy the shape of `homelab/.github/dependabot.yml`, keeping only the ecosystems the repo actually has:

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
      - "SimplicityGuy"
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
2. Get them under management: regenerate the homelab inventory (see below) so the labels are adopted into OpenTofu.

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

When replacing an action with its CLI, diff the defaults. Actions often set inputs the CLI does not: for `skill-check` the action defaulted `security-scan` to false while the CLI defaults it on, and the scan failed the job with zero findings until `--no-security-scan` was added. Read the action's `index.js` to see the exact flags it passes.

## Required Checks That Block PRs

Blocking is a repo ruleset, managed in the homelab OpenTofu `github` module.

1. Get the workflow merged or at least run once, since GitHub only offers checks it has seen.
2. Create the ruleset on the live repo with the REST API: target the default branch (`~DEFAULT_BRANCH`), no bypass actors, rules `deletion`, `non_fast_forward`, `pull_request` (0 required approvals), and `required_status_checks` with one entry per job name and `integration_id` `15368` (GitHub Actions).
3. Adopt it into OpenTofu (below). The module must support `required_status_checks` rules; it does as of the `agent-skills` change.
4. Remember the consequence: direct pushes to the default branch are blocked, so all changes go through a PR.

## Adopting Repo Settings Into homelab

Work from a branch in `homelab`.

1. Make the live change first (ruleset, labels, merge methods). The inventory is generated from live GitHub.
2. Regenerate: `scripts/github-inventory --owner SimplicityGuy`.
3. Update the count assertions in `infra/opentofu/github/tests/owner.tftest.hcl` (repos, rulesets, labels) to match.
4. Run `tofu test` in a clean copy of the module directory without `.terraform`: after `scripts/tofu` has run, `.terraform` points at the S3 backend and a plain `tofu init -backend=false` cannot reach it. Run `tofu init -backend=false` in the clean copy first, since new test runs need modules registered.
5. Plan, then apply the saved plan: `scripts/tofu -m github plan -input=false -out=PLAN`, review it (adoption should be imports only, with no adds, changes, or destroys), then `scripts/tofu -m github apply PLAN`.
6. Verify: `scripts/github-state-reconcile`, then `scripts/github-coverage-report -o infra/opentofu/github/COVERAGE.md` and its `--check`.
7. If gitleaks flags an `address_key` string in `desired-state.json` as a generic API key, add its `file:rule:line` fingerprint to `.gitleaksignore`. These are false positives, and the fingerprints are line-number based, so they may need refreshing after the next regeneration.
8. Commit and open the PR. Merge only when CI is green.

To enforce a fleet-wide setting (for example `allow_merge_commit = true`), pin it in `modules/owner/repositories.tf` on `github_repository.this` so it survives inventory regeneration. Archived repos cannot change settings and keep their observed values.

## Verify Before Finishing

- The PR's required checks pass, and the first Dependabot run opens PRs with the expected labels and commit prefix.
- The deprecation notice is gone from the CI log.
- A final plan shows no changes.

## Pitfalls

- Unquoted `description:` values in skill frontmatter break at the first `: `; use a dash or quote the value.
- Merge methods differ per repo, so check which are allowed before running `gh pr merge`. Squash is the safe default.
- Linters are a floor: passing them does not prove a skill or workflow is correct.
