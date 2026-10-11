# Inventory, extraction, release gates, and handoff

## Inventory and repository map

Collect evidence for:

- deployable services/processes, CLI tools, libraries, web packages, desktop/mobile shells;
- containers/image pipelines, infrastructure, deployment configuration, Actions and release workflows;
- documentation/static sites, profile/branding assets, issue data and repository automation;
- languages, package managers, build frameworks, workspace configuration and lockfiles;
- package names, registries, release channels, tags, internal dependencies, generated-code relationships;
- licenses, notices, vendored code, differing distribution terms;
- secrets/credentials, local state, binaries, caches and generated artifacts that must not migrate;
- CODEOWNERS/natural ownership, cross-directory file references, tests with monorepo-relative assumptions.

Run a secret scan before staging any destination, including history that will be retained. Report redacted findings and paths. Resolve findings before pushing; if real credentials were exposed, prepare remediation without silently rotating external credentials.

Choose boundaries by ownership, release cadence, access, licensing, and deployability. Avoid splitting by directory alone or retaining a grouping that crosses real access/license boundaries. Reference taxonomy, adapted to evidence: private `infra`; core/CLI; UI; desktop/application shell; independently deployed services; private image pipelines with distinct licensing; sensitive source/build units; plugins/integrations; registry repositories such as a Homebrew tap; initially private `.github`; initially private `<ORG>.github.io`.

For each repository document source paths, name/description, initial/intended visibility, ownership/access, license, release unit/version source, build/test commands, incoming/outgoing dependencies, history strategy, Actions permissions/secrets, and acceptance checks. Resolve dependency cycles and generated-code ownership before extraction. Prefer explicit published packages, schemas, generated clients, or build artifacts over cross-repository relative imports. Present the map for approval before external resource creation.

## Reproducible extraction

Create approved destinations through OpenTofu as private empty repositories. Local extraction can be prepared ahead of creation. Use disposable independent clones or an equivalent isolated method; confirm that shared object storage or worktree operations cannot rewrite the original. Prefer `git filter-repo` or equivalent reproducible history extraction. Record exact commands, source revision, included paths, root rewrites, resulting commits and tag policy. Never run destructive filtering against the original.

Per destination:

- retain owned source/tests/docs/schemas/fixtures/build files;
- repair imports, workspaces, paths, metadata, repository URLs, badges, documentation links;
- replace implicit dependencies with explicit packages/artifacts or documented development linking;
- retain licenses, notices, attribution and vendored obligations;
- retain only tags that unambiguously describe this unit; avoid pushing unrelated or publish-triggering tags;
- exclude secrets, local state, caches, builds, editor state and machine-local configuration;
- add a focused README covering setup, development, validation, build, release and boundaries;
- add project-specific agent instructions where used; initialize a repository-local issue tracker only when intended.

Review workflows and publication triggers before any approved push. Push only after local acceptance passes. Leave source removal to a separate approved cleanup after consumers migrate.

## Stable developer interface

Every code repository exposes `just` (command list), `just setup`, `just check`, `just test`, and `just build`. Add lint/format/typecheck/dev/package/release/image recipes where meaningful. Adapt internals to each ecosystem. `just check` is the fast authoritative pre-merge gate composing relevant formatter, linter, type checker, tests, build validation, schemas and license checks. Separate expensive network, load, signing, publishing and cross-platform gates by clear names.

Preserve correctly scoped configuration:

| Ecosystem | Retain/adapt |
|---|---|
| Python | `pyproject.toml`, `uv.lock`, build backend, Ruff, pytest, package metadata |
| Node/TypeScript | `package.json`, pinned `packageManager`, lockfile, TypeScript, applicable Vite/Next/Astro/Turbo configuration |
| Rust/Tauri | manifests, `Cargo.lock`, toolchain, formatting/Clippy and Tauri configuration |
| Containers | Dockerfiles, buildx bake, pinned bases, platform matrix, SBOM/license gates |
| Infra | `.mise.toml`, provider lockfile, SOPS configuration, validate-only CI |

Remove workspace orchestration such as Turborepo when the destination no longer has a real multi-package workspace. Commit lockfiles and pin dependencies. CI runs the relevant gates with least privilege and without unexpected package publication.

## Commitizen and releases

Use Conventional Commits and Commitizen where a repository owns independently versioned artifacts. Version authority follows PEP 621 (Python), package metadata (Node), Cargo metadata/controlled file (Rust), or an explicit multi-artifact version file. Synchronize manifests and lockfiles using pre-bump hooks where needed. Default to `v$version` annotated tags unless an established channel requires another format.

Expose `just bump-preview` and `just bump`. Verify the installed Commitizen version's behavior: preview shows calculated version and changelog without modifying files; do not assume a dry-run option covers every hook. Test preview in a disposable checkout and confirm no changes. Bump is local preparation, not release authorization. Repositories without meaningful versioned artifacts stay unversioned with the reason documented.

Release workflows build the tagged commit only from an approved version tag or explicit dispatch, run the full release gate, and use least-privilege permissions. Prefer OIDC Trusted Publishers to stored registry tokens. Generate applicable checksums, provenance, SBOMs and required notices. Use narrowly installed GitHub Apps for necessary cross-repository automation rather than cross-repository PATs. Migration verification uses safe dry runs; actual publication/releases require separate authorization.

## Evidence required before completion

Collect current results for every applicable check; mark exclusions with reasons and pending checks as pending:

- destination exists with intended visibility, correct default branch/merge policy and supported protection;
- clean local working tree, no tracked plaintext/private identities, redacted secret scan of retained history;
- URLs and metadata point to the new location; clean checkout installs dependencies;
- `just check`, tests, production build and applicable release dry run pass; CI passes;
- licenses/notices retained; relevant history and tag results verified against the extraction record;
- consumers use explicit versions or documented development links;
- OpenTofu post-apply plan is empty; authorized operator and recovery path decrypt SOPS examples safely;
- organization profile renders; Astro deployment/links/assets/404/responsive layout are healthy;
- original monorepo remains intact (compare its revision and initial working-tree state; preserve pre-existing changes).

Finish with the approved repository map; created repositories/visibility; extraction method/history result per destination; added files/configuration; verification commands/results; unresolved dependencies/manual owner actions; SOPS/age/state security and recovery notes; and a proposed second-phase cleanup plan. The cleanup proposal identifies consumer cutover, rollback window, archival/tag preservation and separately approved removal. Never equate creation with completion.
