---
license: MIT
name: repo-ci-setup
description: Use when setting up or auditing GitHub repo automation - SHA-pinned GitHub Actions workflows, required status checks that block PRs, or Node 20 deprecation notices. Triggers on "required checks", "block PRs", "pin actions", "node20 deprecated", "branch ruleset".
---

# Repo CI Setup

Set up SHA-pinned workflows and required checks that block PRs on a GitHub repo. For Dependabot configuration, labels, auditing and fleet rollouts, use `dependabot-setup`. If your repo settings (rulesets, labels, merge methods) are managed as code, for example with OpenTofu or Terraform, make or record each change there too instead of leaving it as hand-edited drift.

## When to Use

- A workflow should block PRs until it passes
- Workflow actions need pinning or bumping
- CI logs show a Node 20 deprecation notice
- Auditing a repo for drift from this baseline

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

## Verify Before Finishing

- The PR's required checks pass.
- The deprecation notice is gone from the CI log.
- If settings are managed as code, a final plan shows no changes.

## Pitfalls

- Unquoted `description:` values in skill frontmatter break at the first `: `; use a dash or quote the value.
- Merge methods differ per repo, so check which are allowed before running `gh pr merge`. Squash is the safe default.
- Linters are a floor: passing them does not prove a skill or workflow is correct.
