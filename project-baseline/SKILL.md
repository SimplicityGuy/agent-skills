---
name: project-baseline
description: Bootstrap a new repo OR audit/retrofit an existing repo against Robert's standard project baseline. Covers Python (uv), Rust (cargo), Node (npm) — apply only the slices that match the stack. Enforces SHA-locked pre-commit hooks, SHA-pinned GitHub Actions with `# vX.Y.Z` comments, justfile as the single command source-of-truth (every CI step calls `just <cmd>`), an `update-project.sh` that auto-applies minor/patch and gates major behind `--major`, Dependabot, weekly dependency update PR workflow, monthly GHCR image cleanup, PR-scoped cache cleanup, Dockerfile OCI metadata labels, Mermaid architecture diagrams in README and docs, ruff/mypy/bandit config with project-standard rules, ≥85% test coverage, git-worktree + PR development flow, and a sorted pyproject.toml. Modeled on the discogsography / phaze / cronduit / nox-scripts conventions. Trigger when the user says any of "new repo", "bootstrap a repo", "set up a new project", "project baseline", "bring this repo to standard", "audit my repo against standards", "add CI to this project", "add pre-commit", "set up GitHub Actions", "what's missing in this repo", or starts a fresh repo and asks for the "usual setup".
---

# project-baseline

The standard kit every new repo gets, and the audit checklist every existing repo is measured against. **Apply only the slices that match the detected stack** — Python, Rust, Node, or any combination.

## When to use

- **Green-field**: a repo was just `git init`'d (or is about to be) and needs the full kit
- **Brown-field audit**: an existing repo is missing pieces of the baseline and needs to be brought up to standard
- **Verification**: confirming a "we already have this" claim against the baseline checklist

If the user says *"the usual setup"*, *"my standard stack"*, *"like discogsography"*, *"like phaze"*, or asks to add any single component below (pre-commit, dependabot, cleanup workflow, update script), use this skill — even when they don't name it.

## What's in the baseline

Every check below has a corresponding asset under `assets/`. If a slice doesn't apply to the detected stack (e.g. no Rust → skip `Dockerfile.rust`), drop it.

| Requirement | Asset | Applies to |
|---|---|---|
| Pre-commit, SHA-locked with `# frozen: <tag>` comments | `assets/.pre-commit-config.yaml` | all |
| `pyproject.toml` sorted by key/heading, ruff + mypy + bandit + coverage configured | `assets/pyproject.toml.template` | Python |
| `Cargo.toml` with `[profile.release]` hardened (lto, strip, codegen-units=1) | `assets/Cargo.toml.template` | Rust |
| `package.json` with pinned engines and audit script | `assets/package.json.template` | Node |
| Justfile organized by group; **every CI step calls `just <cmd>`** | `assets/justfile.template` | all |
| `update-project.sh` — minor/patch auto, `--major` flag for major | `assets/scripts/update-project.sh` | all |
| GitHub Actions, third-party actions SHA-pinned with `# vX.Y.Z` comments | `assets/workflows/*.yml` | all |
| Composite actions for shared CI logic | `assets/actions/*/action.yml` | all |
| Dependabot (github-actions + docker + pip + cargo + npm) | `assets/dependabot.yml` | all |
| Cleanup cache on PR close | `assets/workflows/cleanup-cache.yml` | all |
| Cleanup GHCR images monthly | `assets/workflows/cleanup-images.yml` | Docker repos |
| Update-dependencies workflow on cron (Monday 09:00 PT) | `assets/workflows/update-dependencies.yml` | all |
| Dockerfile with OCI labels + non-root + healthcheck | `assets/Dockerfile.python`, `assets/Dockerfile.rust` | Docker |
| Mermaid architecture diagrams in README + `docs/architecture.md` | `assets/docs/mermaid-conventions.md` | all |
| Ruff: line-length 150, py313 target, standard lint selection | `pyproject.toml.template` | Python |
| Coverage: ≥85%, `fail_under = 85` enforced | `pyproject.toml.template` | Python |
| `.yamllint` strict | `assets/.yamllint` | all |
| Worktree + PR development workflow documented | this file (§ "Worktree + PR workflow") | all |
| README with banner, full badge set, nav bar, and the standard section order | `assets/README.md.template` (scaffold) + invoke the `readme` skill for content | all |
| `docs/` suite (index, categorized guides) | invoke the `comprehensive-docs` skill | all |

## Stack detection

Inspect the repo (or planned repo) and apply only what fits:

| Signal | Stack |
|---|---|
| `pyproject.toml` exists or about to be created | Python |
| `Cargo.toml` exists | Rust |
| `package.json` exists | Node |
| Multiple service subdirs each with own `pyproject.toml` | Python monorepo (uv workspace) |
| `Dockerfile` or `Dockerfile.*` exists or services will be containerized | Docker |
| No `Dockerfile` and won't ship containers | Skip `cleanup-images.yml`, Docker-related dependabot, Docker build workflow |

For multi-stack repos, layer the slices. Discogsography is the canonical multi-stack example (Python + Rust + Node + Docker monorepo); phaze is single-Python+Docker; cronduit is Rust+Docker; nox-scripts is Python+Ansible+OpenTofu (no Docker).

## Justfile as the single command source-of-truth

**Hard rule:** every command you can run locally must be `just <something>`, and every CI step that runs that command must invoke `just <something>` — not the underlying tool directly. This means one place to update when a command changes.

Concretely, in workflows you must see this pattern:

```yaml
- name: 🧪 Run tests
  run: just test-cov
```

Never this:

```yaml
- name: 🧪 Run tests
  run: uv run pytest --cov=src --cov-report=xml   # ❌ duplicates the justfile recipe
```

The justfile is organized by group using just's `[group('name')]` attribute. Standard groups:

- `setup` — install, init, sync, lock-upgrade, update-deps, update-hooks
- `quality` — lint, lint-python, format, security, pip-audit
- `test` — test, test-cov, test-ci (plus `test-<service>` per service in monorepos)
- `docker` — docker-build, docker-validate, docker-compose-validate, up, down, logs, rebuild
- `rust` (when Rust is present) — extractor-build, extractor-test, extractor-fmt, extractor-clippy, extractor-audit, extractor-deny
- `node` (when Node is present) — install-js, test-js, test-js-cov, update-npm
- `dev` — dev, run, monitor, check-errors

When adding a new command:

1. Add it to `justfile` under the right `[group(...)]`
2. If CI needs it, the CI step calls `just <name>` — never reinline
3. Bump the README's tooling badges if a new tool is introduced

When auditing: grep workflows for tool invocations that should have been `just <cmd>`:

```bash
# Look for direct tool invocations in workflows that should be just <cmd>
grep -E '^(  +run: )(uv |cargo |pre-commit |pytest |ruff |mypy |bandit |npm |docker )' .github/workflows/*.yml
```

If any matches turn up, flag them and rewrite them as `just <name>` calls.

## SHA-pinning conventions

Two conventions are in play. Apply both rigorously — `pre-commit autoupdate --freeze` and Dependabot together keep the comments honest.

**Pre-commit (`# frozen: <tag>`):**

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: 6fec9b7edb08fd9989088709d864a7826dc74e80  # frozen: v0.15.12
  hooks:
    - id: ruff
```

The `rev:` is a full SHA. The `# frozen: <tag>` comment is what `pre-commit autoupdate --freeze` writes — keep it untouched.

**GitHub Actions (`# vX.Y.Z`):**

For third-party actions, pin to a SHA and append a `# vX.Y.Z` comment:

```yaml
- uses: extractions/setup-just@53165ef7e734c5c07cb06b3c8e7b647c5aa16db3 # v4.0.0
```

For first-party (`actions/checkout`, `actions/setup-python`, `docker/*`, `github/codeql-action`) you may pin by major-version tag (`@v6`) — Dependabot still tracks them.

When upgrading: resolve the new tag to a SHA via `gh api repos/<owner>/<repo>/git/refs/tags/<tag>` and update both the SHA and the comment in the same commit.

## update-project.sh contract

The script under `assets/scripts/update-project.sh` is the canonical implementation. Its contract:

- **Default (no flags)**: applies minor + patch updates for all ecosystems (Python via `uv lock --upgrade` — but the script wraps it to filter major bumps; Rust via `cargo update`; Node via `npm update --save`; pre-commit via `just update-hooks`; Docker base image refresh).
- **`--major`**: also includes major version bumps for all ecosystems. For Rust, runs `cargo upgrade --incompatible` (cargo-edit). For Python, lets uv unpinned `>=X` constraints flow up.
- **`--python <version>`**: also updates the Python version across `pyproject.toml`, Dockerfiles, workflows, CLAUDE.md, README.
- **`--dry-run`**: no writes; reports what would change.
- **`--no-backup`**: skip the `backups/project-updates-<ts>/` snapshot. Use in CI.
- **`--skip-tests`**: don't run `just test-all` post-update. Use when chaining.

All tool invocations inside the script must call `just <cmd>` where a recipe exists. The script never reaches around the justfile.

## update-dependencies workflow contract

`assets/workflows/update-dependencies.yml`:

- Runs on cron Monday 09:00 UTC (≈1–2 AM PT)
- `workflow_dispatch` input `major_upgrades: bool` → passes `--major` through
- Calls `./scripts/update-project.sh --no-backup` with optional `--major`
- Opens a PR titled `chore: update dependencies (N packages)` against `automation/updates` branch
- Assigns the PR to the repo owner (set via the `assignees` field — `SimplicityGuy` is the canonical value for this user)

The PR body embeds the script's own summary. Don't reinvent — point to the canonical version in `assets/scripts/update-project.sh` and `assets/workflows/update-dependencies.yml`.

## Worktree + PR workflow

The development pattern is: branch in a git worktree, push, open a PR, merge through CI. **Never commit directly to `main`.** When this skill bootstraps a repo, document this in the project's CONTRIBUTING.md or CLAUDE.md.

The mechanics:

```bash
# Start work on a new feature
git worktree add ../<repo>-feature-x -b feature/x
cd ../<repo>-feature-x

# ...make changes, commit...

git push -u origin feature/x
gh pr create --title "feat: x" --body "..." --base main

# After merge
cd ../<repo>            # back to main worktree
git pull
git worktree remove ../<repo>-feature-x
git branch -d feature/x
```

This composes cleanly with the `superpowers:using-git-worktrees` skill — invoke it when actually starting feature work in a baseline repo.

## README layout

The README is part of the baseline. The scaffold lives at `assets/README.md.template` — it carries the canonical badge set, the centered header block (banner image, no H1, bold description), the centered nav bar, and placeholders for the standard sections in order: 🎯 What is → 🏛️ Architecture → 🌟 Features → 🚀 Quick Start → 📖 Documentation → 👨‍💻 Development → 🛠️ Technology Stack → 💬 Community → 📜 License → 🙏 Acknowledgments.

**Compose with the existing `readme` skill.** The scaffold gives you the bones; the [`readme`](../readme.skill.md) skill carries the deep content guide for each section (what goes in the "What is" paragraph, how to structure the services table, badge rules, navigation anchor conventions, etc.). After dropping the scaffold into the target repo, invoke the `readme` skill to fill out each section.

Badge groups, in order:

1. **CI/CD status** — Build / Code Quality / Tests / codecov. Each links to its workflow page.
2. **Static info** — license, language version, package manager (`uv`), task runner (`just`), linter (`Ruff`), pre-commit, type checker (`mypy`), security scanner (`Bandit`), Docker readiness, AI tooling (`Claude Code`).
3. **Stack-specific** — Rust (`Cargo`, `Clippy`), Node (`Node 24+`) — uncomment in the template as applicable.

For the `docs/` directory suite (index, role-based guides), invoke the `comprehensive-docs` skill in addition.

## Mermaid diagram conventions

Every project has at least:

- **One Mermaid `graph TD` in the root README** showing services + data stores + flow direction
- **`docs/architecture.md`** with finer-grained diagrams (one per logical concern: data flow, service comms, message queue, schema)

See `assets/docs/mermaid-conventions.md` for the styling rules (subgraphs for layers, emoji-prefixed node labels matching service identifiers, consistent fill colors per node type — copy the palette from discogsography's README).

## How to run this skill

### Green-field: bootstrap a new repo

1. Confirm repo root and stack with the user (Python? Rust? Node? combination? Docker?).
2. Detect the slices that apply (see § "Stack detection").
3. Copy the applicable assets into the repo, **with placeholders substituted**:
   - `<PROJECT_NAME>` → user-confirmed project name (kebab-case)
   - `<PROJECT_DESCRIPTION>` → one-line description
   - `<OWNER>` → GitHub owner (default `SimplicityGuy` unless the user says otherwise — check git config first)
   - `<AUTHOR_NAME>` / `<AUTHOR_EMAIL>` → from git config
   - `<PYTHON_VERSION>` → latest stable (default `3.13`)
   - `<LICENSE>` → ask; default `MIT` for personal projects, `PolyForm-Noncommercial-1.0.0` for discogsography-class work
   - `<SERVICES>` → list of service names if monorepo, else just `<PROJECT_NAME>`
4. Initialize and verify:
   ```bash
   git init -b main          # if not already
   just init                 # installs pre-commit hooks
   just install              # syncs deps
   just lint                 # baseline pre-commit pass
   just test                 # baseline test pass (will fail if no tests yet — that's OK on day 1)
   ```
5. Make the first commit *after* pre-commit passes:
   ```bash
   git add -A
   git commit -m "chore: bootstrap project baseline"
   ```
6. Create a GitHub repo (if not already) and push.
7. Set repo settings: branch protection on `main` (require PRs, require status checks, require linear history); enable Dependabot security alerts; enable Code Scanning.

### Brown-field: audit/retrofit an existing repo

1. Read each baseline check (the table at the top) and compare against the repo:
   ```bash
   ls .pre-commit-config.yaml .github/dependabot.yml justfile pyproject.toml 2>/dev/null
   ls .github/workflows/{cleanup-cache,cleanup-images,update-dependencies}.yml 2>/dev/null
   grep -c "frozen:" .pre-commit-config.yaml 2>/dev/null
   ```
2. Produce a punch-list of what's missing or non-compliant.
3. **Ask before bulk-applying** — don't overwrite an existing `.pre-commit-config.yaml` without confirmation; some repos have intentional divergences (cronduit has no pre-commit yet, by design at time of writing).
4. Apply gaps one-at-a-time as separate commits, each scoped to one slice:
   - `chore: add SHA-locked pre-commit config`
   - `chore: add dependabot config`
   - `chore: add cleanup workflows`
   - etc.
5. After each commit, run `just lint` and verify CI passes locally.

## Verification checklist

Before declaring a repo "baseline-compliant", confirm:

- [ ] `pre-commit run --all-files` passes
- [ ] `.pre-commit-config.yaml` has `# frozen:` comments on every `rev:` line
- [ ] Every third-party action in `.github/workflows/*.yml` is pinned to a SHA with `# vX.Y.Z` comment
- [ ] `dependabot.yml` covers every ecosystem present (github-actions + at least one of pip/cargo/npm/docker)
- [ ] `cleanup-cache.yml` exists and triggers on `pull_request: closed`
- [ ] `cleanup-images.yml` exists IFF the repo publishes containers
- [ ] `update-dependencies.yml` exists, runs on Monday cron, accepts `major_upgrades` input
- [ ] `scripts/update-project.sh` exists, is `+x`, has `--major` / `--dry-run` / `--no-backup` flags
- [ ] `justfile` exists; every workflow `run:` line that invokes a tool calls `just <cmd>`
- [ ] `pyproject.toml` (if Python) has ruff line-length 150, target-version `py313`, the standard lint selection, mypy strict, coverage `fail_under = 85`
- [ ] Sections in `pyproject.toml` are sorted (alphabetical by table heading; keys within each table also sorted where meaningful)
- [ ] Dockerfile (if present) has the full OCI label set, non-root user, healthcheck
- [ ] README has a Mermaid `graph TD` for architecture
- [ ] `.yamllint` exists with strict mode

If a single item is missing on a "complete" claim, push back and fix it before moving on. Drift compounds — incomplete baselines are how repos rot.

## Pointers to bundled assets

The asset bundle under `assets/` is the canonical, parameterized copy of each template. Read the relevant ones before writing into the target repo:

- `assets/.pre-commit-config.yaml` — copy as-is; only the local hooks section is project-specific
- `assets/pyproject.toml.template` — substitute placeholders; merge into existing `pyproject.toml` for retrofits
- `assets/Cargo.toml.template` — for new Rust crates; merge `[profile.release]` and `[lints]` for retrofits
- `assets/justfile.template` — start from the relevant subset (setup + quality + test always; docker/rust/node by stack)
- `assets/dependabot.yml` — keep only the ecosystems the repo uses
- `assets/Dockerfile.python` / `assets/Dockerfile.rust` — per-service Dockerfiles; substitute service-specific labels
- `assets/scripts/update-project.sh` — copy as-is, mark `+x`; the script auto-detects which ecosystems to update
- `assets/workflows/*.yml` — copy the ones that apply; each workflow's first comment explains its trigger and scope
- `assets/actions/*/action.yml` — composite actions; copy into `.github/actions/<name>/action.yml`
- `assets/README.md.template` — README scaffold with the canonical badge set and section order; substitute placeholders, then invoke the `readme` skill to fill in content
- `assets/docs/mermaid-conventions.md` — short style guide; don't copy into the target repo, just follow it when writing diagrams

## Companion skills

This skill is intentionally narrow: bootstrap + audit. Three other skills cover adjacent ground and should be invoked alongside as needed:

- **`readme`** — content guide for the README's individual sections (what goes in "What is", architecture, features, etc.). Use after dropping `assets/README.md.template` into the target repo.
- **`comprehensive-docs`** — builds the full `docs/` suite (index, categorized guides, role-based navigation). Use once the project has substance worth documenting.
- **`brand-asset-audit`** — audit and generate brand assets (banner, logos, OG image) referenced by the README header. Use when the project doesn't yet have a banner image.

When in doubt about a pattern that isn't bundled, the live reference repos are: discogsography (multi-stack monorepo), phaze (single Python+Docker), cronduit (Rust+Docker), nox-scripts (Python+Ansible). Cross-check the latest version of any pattern there before transplanting an older version from this skill.
