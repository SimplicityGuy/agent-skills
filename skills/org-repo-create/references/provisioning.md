# Repository preparation and acceptance

## Existing infra integration

Locate the canonical repository map and shared defaults. Add a private entry with name/description, homepage/topics where relevant, owner/team access, feature flags (issues/projects/wiki/discussions), merge methods, merged-branch deletion, labels, and supported rulesets. Preserve repository-specific development protocols. Use `auto_init = false` and leave public intent unactivated until separately approved.

Check `gh auth status`, organization access and current plan capabilities without displaying tokens. Verify current provider schemas and official feature documentation. Never assert protection is present from configuration alone. Provision with existing version-constrained OpenTofu providers and committed `.terraform.lock.hcl`; do not unnecessarily upgrade unrelated providers.

Run formatting checks, `tofu init -backend=false -input=false` and `tofu validate` without live state, using an isolated validation directory if necessary. Obtain runtime authentication from `gh auth token` for local plan/apply. Protect plan/state files and suppress secret values. Review the full plan, not just the new repository resource. If unrelated drift/destructive changes appear, resolve or isolate them before requesting approval; do not casually apply or use targeting to hide unresolved changes. After approved apply, verify an empty post-apply plan or report remaining drift as incomplete.

Use existing SOPS-encrypted secret sources and recipient/recovery policy. Never place identities or plaintext intermediates in Git. Where Secure Enclave is used, decryption follows the configured operator policy and is machine-bound; do not assume CI can reuse it. If setting up encryption is actually necessary, consult the `monorepo-to-org` infrastructure reference and current SOPS/age-plugin-se upstream guidance. Keep infra CI validate-only until an explicitly approved secure CI plan/apply design exists.

## Local scaffold

Prepare in a new recoverable workspace directory. Never overwrite pre-existing files or mutate unrelated source. Use the selected stack and approved template/source strategy; keep imported licenses and notices, and inspect retained history for secrets. Produce useful runnable code or tooling for the specified purpose without inventing unrelated product features. If application behavior is unspecified, provide a minimal runnable starter and state its limits.

Include:

- focused README: purpose, setup, development, validation, build, architecture/dependency boundaries, versioning/release or why unversioned;
- license/required notices, `.gitignore`, applicable agent instructions and CODEOWNERS using confirmed owners;
- pinned tools through the organization's mechanism (normally `.mise.toml`), pinned dependencies/package manager and committed lockfiles;
- `Justfile`/`justfile` with default command listing and `setup`, `check`, `test`, `build`; add meaningful dev/lint/format/typecheck/package/image recipes;
- CI invoking real gates, least-privilege permissions, pinned actions and real check names; optional Dependabot on opt-in only;
- stack-specific build framework: Python `pyproject.toml`/build backend/Ruff/pytest/`uv.lock`; Node manifests/pinned `packageManager`/TypeScript/lockfile; Rust manifests/toolchain/formatting/Clippy/`Cargo.lock`; containers pinned bases/buildx platforms/SBOM/license gates as applicable.

`just check` is the fast authoritative pre-merge gate combining applicable formatting, linting, typing, tests, build/schema/license validation. Expensive network, signing, cross-platform and publishing gates get separate clear names. Do not retain Turborepo or other workspace orchestration for a single-package project. Set package metadata, repository URLs and links to the intended destination.

## Versioned artifacts

Use Conventional Commits and Commitizen only for meaningful independently versioned artifacts. Authority follows PEP 621, Node package metadata, Cargo metadata/controlled file, or explicit multi-artifact version file. Default to annotated `v$version` tags unless the existing release channel differs. Synchronize lockfiles/manifests with hooks where needed.

Provide `just bump-preview` (version/changelog without changing files) and `just bump` (local version update). Verify current Commitizen semantics and preview/hook behavior in a disposable checkout. Safe release dry runs must not upload artifacts, push tags or publish packages.

Release workflows run from an approved version tag or explicit dispatch, build the tagged commit and pass the full release gate. Prefer OIDC Trusted Publishers; use narrowly installed GitHub Apps if cross-repository automation is unavoidable. Generate applicable checksums, provenance, SBOMs and notices. Do not enable inherited push-triggered publication inadvertently. Leave actual release/publication pending separate authorization.

## Optional branding and Pages

Use canonical editable branding in infra and promote rendered assets; do not create independently editable logo copies. For an explicitly requested organization profile/site, follow the `monorepo-to-org` public-surfaces reference. Public `.github` content lives in `profile/README.md` and `profile/assets/`; inheritance and owner-only avatar steps require explicit verification.

For requested Astro Pages work, consult current official Astro/GitHub Pages documentation. Use static output, correct site URL, a base path only for project sites that require it, committed lockfile, dev/build/preview commands, accessible semantic UI, metadata/canonical URLs, OG image, appropriate sitemap/robots/manifest/favicon and 404. No secret-dependent runtime. Use the official pinned Actions approach with a Pages environment, concurrency and minimal `contents: read`, `pages: write`, `id-token: write` deployment permissions. Obtain approval for Pages/public visibility and DNS with rollback. Verify deployed links/assets/404/responsive behavior and DNS/HTTPS where applicable.

## Acceptance and handoff evidence

Verify from a clean checkout that dependency installation, `just check`, `just test`, production build and applicable safe release dry run pass. Scan tracked files and imported history with redacted findings. Confirm license/notices, URLs/metadata, explicit dependency versions or documented development links, and a clean working tree after the prepared commits. Verify the private remote, default branch, allowed merge methods, real team access, supported protection and CI results after the approved push. Verify applicable secrets through authorized operator checks without logging plaintext, and confirm infra convergence with an empty plan.

An empty creation, local build alone, or configured-but-unrun CI is not completion. Report pending checks and manual owner actions honestly. Handoff includes actual URL/visibility, infra and source revisions, added files/configuration, commands/results, optional Dependabot status, release/publication status and relevant security/recovery notes.
