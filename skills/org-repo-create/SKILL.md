---
name: org-repo-create
description: Create a new repository in an existing GitHub organization through a staged questionnaire and private-first, OpenTofu-managed provisioning, with just validation gates, CI, applicable Commitizen releases, and optional standardized Dependabot. Use for new organization repositories rather than monorepo decomposition or organization creation.
---

# Create an Organization Repository

Prepare an independently buildable repository in an existing GitHub organization using the operating standards of `monorepo-to-org`. The existing private `infra` repository owns supported GitHub settings, access, labels, visibility and encrypted secrets. Start private, keep secrets out of Git, and verify code and automation before claiming completion. Scope this workflow to the requested repository and necessary infra changes; do not initiate a monorepo split, organization-wide retrofit, branding redesign or public site by default.

## Gather decisions before provisioning

Read [references/questionnaire.md](references/questionnaire.md). Ask two or three related questions at a time, skip answers already known, and inspect technical facts rather than asking the operator to rediscover them. Continue independent read-only discovery and local recoverable preparation while answers are pending. Never ask for secret values in chat.

Inspect applicable `AGENTS.md`, `CLAUDE.md`, repository instructions and directly relevant available skills in both infra and the destination workspace. If Beads is in use, run `bd prime` and track work with `bd`; do not copy a shared issue database into the new repository. Maintain a local provisioning record with resolved identifiers, source revision, decisions, approvals, pending actions and verification results. Resume from this record and recheck changing external facts.

Resolve the organization, repository name, description/purpose, maintainer/team access, workspace, existing infra location, license, technology, initial/intended visibility, and versioned artifact ownership. Confirm the organization already exists and the repository name is available. If the name exists, inspect and report it; do not overwrite, reinitialize, delete or silently adopt it. If the organization is absent, leave provisioning pending and propose a separate organization setup.

## Preparation and execution boundaries

Proceed autonomously on read-only discovery and local recoverable preparation. Obtain explicit approval of concrete reviewed changes before remote repository creation, OpenTofu apply, visibility changes, branch/tag pushes, Pages/DNS configuration, permission or secret-store mutations, PR merges, package publication or releases. Record existing explicit authorization and reuse it for unchanged named actions; do not ask twice. Questionnaire preferences and design approval alone do not authorize every external operation. Explain which action and this skill's rule require approval, and finish its reviewable preparation first.

- Create repositories privately and empty (`auto_init = false`). Never request a generated README when prepared local history will be pushed. Public intent requires a later reviewed and explicitly approved transition, including `.github` and `<ORG>.github.io`.
- Repository access and licensing are real boundaries. Do not place restricted or differently licensed components together without resolving their distribution/access policy.
- Never commit/log plaintext secrets, private age identities, credentials, signing material, package tokens, generated auth files, state or secret-bearing plans. Obtain `GITHUB_TOKEN` from `gh auth token` at execution time without logging or storing it. Scan prepared files and any imported history with redacted output before staging/pushing.
- Pin tooling/dependencies/actions and commit applicable lockfiles. Check current official documentation/provider schemas before implementing commands or claiming supported GitHub features.
- Detect the organization's current GitHub plan; document unsupported private protection or Pages honestly. Preserve the actual merge protocol, including preserved merge commits where required.
- Keep real infra plan/apply operator-local unless an existing approved CI identity, decryption, state-security and approval design is present. Secrets can appear in state even when their source is SOPS-encrypted.
- Do not publish or release during setup without separate authorization. Inspect push/tag/dispatch workflow triggers before the first push.

## Provision and validate

Read [references/provisioning.md](references/provisioning.md) for the concrete preparation and acceptance gates.

1. Discover the existing infra repository, canonical map, teams, labels, merge defaults, state design, SOPS recipients and plan capabilities. Reuse approved conventions without changing unrelated resources. If infra is absent or inaccessible, prepare a local repository specification and leave declarative provisioning pending; do not bypass the source of truth with an ad hoc `gh repo create`. Offer a separately scoped infra bootstrap using the relevant `monorepo-to-org` infrastructure guidance when available.
2. Present a repository specification: source/template strategy, name/description, private initial state, intended visibility, owner/access, license, stack, dependency boundaries, artifact/version authority, developer commands, CI/required checks, Actions permissions/secrets, optional Dependabot and acceptance checks. Resolve missing decisions before provisioning.
3. Prepare the scaffold locally and the smallest canonical infra change. Format and validate infra without live state, run a protected local plan and review its complete effects. Obtain explicit approval before apply and verify an empty post-apply plan.
4. Validate the local repository, then obtain approval for its exact initial push. Verify CI and remote settings, including whether required-check names are real and actually run. Avoid circular bootstrap rules that make the initial push impossible; any temporary bootstrap exception must be explicit, approved and removed/verified afterward.
5. If requested, prepare content/history exposure review and a separate public transition; handle Pages/DNS only when relevant and approved. Do not create organization profile/site repositories merely because the standards mention them.

## Optional standardized Dependabot

Ask whether to use `agent-skills:dependabot-setup` (standalone name `dependabot-setup`). On opt-in, read that skill; bundled source is `../dependabot-setup/SKILL.md`. Apply its detected-ecosystem configuration, grouped version/security updates, directory checks, labels and CI compatibility to this repository only. Ask about assignee and schedule/timezone where not already known.

Prepare configuration locally and record managed labels/settings in infra. Do not automatically copy Actions secrets to Dependabot: assess which are needed and least privilege. Its create/push/PR/merge/fleet/secret operations remain subject to the approvals above; opt-in does not authorize a fleet sweep. If unavailable, report the missing skill and leave the optional standard pending.

## Handoff

Report the repository URL and actual visibility; infra files/resource changes and convergence result; local files/tooling/CI/release configuration; verification commands/results; outstanding owner actions or unsupported features; secret/state/recovery notes when relevant; and next steps. Distinguish prepared, created, pushed, locally verified and CI verified states. Completion requires a working repository and verified automation, not an empty GitHub repository. Keep unauthorized or failed checks explicitly pending.
