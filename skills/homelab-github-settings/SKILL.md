---
name: homelab-github-settings
description: Use when a SimplicityGuy GitHub repo setting (ruleset, label, merge method) was changed live and must be adopted into the homelab OpenTofu github module, or when regenerating the github inventory. Triggers on "adopt into homelab", "github-inventory", "desired-state.json", "owner.tftest.hcl", "github-state-reconcile".
---

# Homelab GitHub Settings

SimplicityGuy repo settings (rulesets, labels, merge methods) are managed as code in `homelab/infra/opentofu/github`, so they are changed there and not by hand in the GitHub UI. This is the SimplicityGuy-specific companion to the generic `repo-ci-setup` skill.

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

## Pitfalls

- The inventory is generated from live GitHub, so a setting that was never made live is not adopted.
- Unrelated drift in `desired-state.json` or `inventory.json` after regeneration belongs in its own commit, not this one.
