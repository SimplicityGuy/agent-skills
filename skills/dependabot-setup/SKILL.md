---
license: MIT
name: dependabot-setup
description: Use when configuring Dependabot on a repo, checking an existing repo's Dependabot setup for problems, fixing red Dependabot PRs, or rolling the same Dependabot setup out across every repo an owner has. Triggers on "dependabot", "dependabot.yml", "dependabot labels", "dependabot secrets", "red dependabot PRs", "audit dependabot", "all repos".
---

# Dependabot Setup

Get Dependabot to the same known-good state on one repo or many, and bring older repos up to it. Three modes share one definition of "correct":

- **Configure**: a repo has no or a minimal Dependabot setup.
- **Audit and fix**: a repo already has Dependabot and may be wrong, stale or red.
- **Fleet**: run Configure or Audit across every repo an owner has.

## Target state

A repo is correct when all of these hold:

1. `.github/dependabot.yml` has one block per ecosystem the repo actually uses, and no block for one it does not.
2. Each block yields **one PR for version updates and one for security updates**, through `groups` with `applies-to`.
3. Every `directory` in the config exists.
4. Every label the config names exists on the repo.
5. Workflows run on Dependabot PRs, so every secret they read exists in the **Dependabot** secrets store (separate from Actions secrets).
6. Dependabot PRs are green, or red for a reason someone has decided on.

## Config shape

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
      actions-version-updates:
        applies-to: version-updates
        patterns:
          - "*"
      actions-security-updates:
        applies-to: security-updates
        patterns:
          - "*"
```

Repeat the block per ecosystem, changing the prefix and labels to match. Note deliberate gaps (compose files, provider pins owned by another script) in a header comment so an audit does not "fix" them.

Detect ecosystems from manifests:

| Found in repo | Ecosystem |
|---|---|
| `.github/workflows/*.yml` | `github-actions` |
| `pyproject.toml` + `uv.lock` | `uv` (not `pip`) |
| `requirements*.txt`, `poetry.lock` | `pip` |
| `package.json` | `npm` |
| `Dockerfile` | `docker` |
| `docker-compose*.yml` | `docker-compose` |
| `.pre-commit-config.yaml` | `pre-commit` |
| `go.mod`, `Cargo.toml` | `gomod`, `cargo` |
| `*.tf` | `terraform` |

## Configure (one repo)

1. List manifests, map them to ecosystems, and write the config.
2. Create the labels the config names (`dependencies` `0366d6`, `ci` `ededed`, plus `python`, `docker`, `javascript` as needed). A missing label means a silently unlabelled PR.
3. Open a PR. Merge it when green.
4. Confirm the first Dependabot run opens PRs with the expected labels and commit prefix.

## Audit and fix (an existing repo)

Run these checks, then fix every miss in one PR.

| Check | How | Typical fix |
|---|---|---|
| Missing ecosystem | Compare the manifest table above with `dependabot.yml` | Add the block |
| Stale ecosystem or directory | Each `directory` must exist; a removed service path makes every Dependabot run fail | Delete the block |
| Wrong ecosystem | `pip` in a uv project | Switch to `uv` |
| Not split security vs version | Blocks lack `applies-to` groups | Add both groups |
| Missing labels | `gh label list` against the config | Create them |
| Missing Dependabot secrets | Grep workflows for `secrets.`, compare with `gh secret list --app dependabot` | Add the secret, never paste values into chat |
| Open or red PRs | `gh pr list --author "app/dependabot" --json number,title,statusCheckRollup` | See below |
| Failing Dependabot runs | Latest "Dependabot Updates" run on the default branch | Fix the config error it names |

A secret missing from both stores only matters if its step runs.

### Red Dependabot PRs

Investigate each to its cause and fix that, not the symptom. Close a PR only when a green one supersedes it.

- **`pip` in a uv project.** Dependabot edits `pyproject.toml` but cannot rewrite `uv.lock`, so `uv lock --check` fails and a rebase cannot fix it. Use the `uv` ecosystem.
- **Pinned vendor or license manifests.** Bumps trip files such as `vendor-licenses.mjs` or `THIRD_PARTY_NOTICES.md`. Update the manifest on the Dependabot branch, or ahead of the next bump.
- **Measured version caps.** Ignore minor and major updates for a guarded dependency and keep patch and security updates. Raising the cap is an operator decision.
- **Shared scanner failures on main.** One pre-existing audit finding turns every PR red. Fix it once in a combined PR.
- **Direct pins that conflict.** For example a transitive package pinned while its parent requires another version. Drop the direct pin.

Merge Dependabot PRs that are green or have no CI. Do not use `--admin` and do not skip checks.

## Fleet

Use one coordinating session that fans out one agent per repo. Re-check real state yourself at the end, because agent "MERGED" reports are not reliable.

1. **Scope explicitly.** Name the owners, and skip other owners and forks. Enumerate with `gh repo list OWNER --no-archived --source --json name`. A repo with no local clone still counts, so look it up on GitHub before calling it absent.
2. **Pick the mode per repo.** Run Configure where Dependabot is missing and Audit and fix where it exists.
3. **Dispatch.** A prompt that worked:

   > For all of the repos, please do the following:
   > - merge any open Dependabot PRs
   > - add a Dependabot configuration that will create 1 PR per ecosystem; one for security issues and one for regular version bumps
   > - ensure all repos are configured to run the github workflows on dependabot PRs
   >
   > Once the PR for the dependabot update configuration is created and green, merge it. Do this for all repos owned by org-a and org-b. Skip any other owners; skip forks too.

4. **Finish with a second pass.** Re-query every repo for open PRs and red checks. Dependabot reopens regrouped PRs after a config merge, so a second pass is normal. Report what still needs an operator decision instead of forcing it.

## Pitfalls

- Merge methods differ per repo. Check which are allowed before `gh pr merge`; squash is the safe default.
- A repo ruleset requiring checks can block Dependabot PRs; the checks must run on them, which is why the secrets check matters.
- Settings managed as code (OpenTofu or Terraform) should record labels and rulesets there too, or the next apply removes them.
