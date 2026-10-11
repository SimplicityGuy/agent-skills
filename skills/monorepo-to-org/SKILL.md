---
name: monorepo-to-org
description: Guide an existing monorepo into a private-first GitHub organization with an interactive decision questionnaire, history-preserving extraction, OpenTofu-managed infra, SOPS, independent release gates, branding, and an Astro Pages site. Use for monorepo decomposition or multi-repository organization migrations, not product installation.
---

# Monorepo to Organization

Act as a senior platform engineer. Produce independently buildable repositories with explicit ownership, security, licensing, and release boundaries. A private, manually bootstrapped `infra` repository becomes the source of truth for organization resources, encrypted secrets, canonical branding, and registry manifests. OpenTofu manages supported GitHub resources. Public profile and site repositories begin private.

## Start with questions and evidence

Read [references/questionnaire.md](references/questionnaire.md) first. Guide the operator through its decision stages; do not dump the entire questionnaire or execute the migration before gathering answers. Ask small batches, reuse answers already given, and discover technical facts rather than asking the operator to inventory the code. Continue independent read-only discovery while waiting for answers. Never request secret values in chat.

Before work, inspect applicable `AGENTS.md`, `CLAUDE.md`, repository instructions, and available skills. Apply directly relevant GitHub/IaC, security, decomposition, release, frontend, testing, and verification guidance. Do not choose a product-installation skill because its name resembles this task. If Beads is used, run `bd prime` and use `bd` for durable tracking; do not blindly copy its shared database into destinations.

Resolve `<ORG>`, `<MONOREPO>`, `<PRIMARY_MAINTAINER>`, `<WORKSPACE>`, and optional `<ORG_DOMAIN>` before external changes. Maintain a recoverable local migration record with answers, evidence, repository map, decisions, pending questions, approvals, exact extraction commands, and verification results. Keep it outside the original monorepo until an intended destination is agreed. Do not record credentials or secret-bearing plans. On resume, read the record, recheck changing facts, and continue from the last verified gate.

## Authorization and invariants

Proceed autonomously with read-only discovery and local recoverable preparation. Obtain explicit approval of concrete actions before organization/repository creation, visibility changes, OpenTofu apply, DNS or Pages configuration, branch/tag pushes, source deletion, package publication, or artifact releases. Existing explicit authorization may cover a named batch; record its scope and do not ask again for the same unchanged action. Approval of the repository map is design approval, not blanket permission to execute every phase. Prepare reviewable files, plans, and exposure checks before requesting execution approval. Explain which action and this skill's rule require approval.

- Preserve the original monorepo and history. Extract from disposable clones; never delete or rewrite the original during the initial split. Cleanup is a separate approved change after all destinations and consumers are verified.
- Ordinary repositories default to private. `.github` and `<ORG>.github.io` also start private; their public transition requires a separate content and exposure review and approval.
- Real repository access and licensing boundaries govern decomposition. A restricted-looking subdirectory provides no isolation.
- Never commit or log plaintext secrets, private age identities, credentials, signing material, tokens, generated authentication files, OpenTofu state, or secret-bearing plans. Secret scans report filenames/categories with redacted findings, not values. Scan current files and retained history before staging or publishing destinations.
- Obtain `GITHUB_TOKEN` from `gh auth token` at execution time; do not persist a PAT or echo the token. Avoid shell tracing and secret-bearing command output.
- Create empty repositories with `auto_init = false`; do not generate a README when prepared history will be pushed.
- Verify the organization's current GitHub plan and feature support. Never claim unsupported private rulesets, protection, or Pages exist.
- Pin dependencies and commit applicable lockfiles. Keep real plan/apply operator-local until an explicit CI identity, decryption, state-security, and approval design is approved.
- Do not publish packages or releases as a side effect of migration. Review inherited workflows for push/tag triggers before any push.

## Workflow and gates

1. **Inventory and design:** read [references/extraction.md](references/extraction.md). Inventory source, dependencies, history, licensing, ownership, automation, and excluded artifacts. Secret-scan before staging. Resolve cycles and generated-code ownership. Present an evidence-based repository map and unresolved decisions for approval before external resources.
2. **Infra and secrets:** read [references/infrastructure.md](references/infrastructure.md). Prepare the private bootstrap, local state, Secure Enclave/recovery design, encrypted dummy example, and canonical OpenTofu map. Verify upstream behavior before implementation. Obtain approval before manual bootstrap, import/live-state changes as applicable, and apply; review the full plan.
3. **Extraction and developer experience:** follow the extraction reference. Prepare disposable history-preserving clones, repair dependencies, establish `just` gates, scoped ecosystem tooling, validate-only infra CI, and safe release configuration. Validate locally before approved pushes.
4. **Optional Dependabot:** ask the questionnaire's opt-in question. If selected, read the available `agent-skills:dependabot-setup` skill (standalone name `dependabot-setup`; bundled source at `../dependabot-setup/SKILL.md`) and use its standardized configuration for the chosen repositories only. Prepare local configuration first. Record its labels/settings in infra. Its PR, merge, fleet, and secret-store operations do not bypass this skill's approval boundaries. Do not copy Actions secrets into Dependabot automatically; decide necessity and least privilege. If unavailable, report that and keep the optional work pending rather than inventing the standard.
5. **Branding and public surfaces:** read [references/public-surfaces.md](references/public-surfaces.md). Keep editable sources in infra, promote reproducible rendered assets, prepare profile and Astro site, review exposure, and obtain explicit approval before public transitions, Pages, or DNS changes.
6. **Verification and handoff:** use the extraction reference's evidence checklist. An existing empty repository is not complete. Track each repository as prepared, created, populated, locally verified, CI verified, or blocked; claim migration completion only when independent builds, automation, access boundaries, and an empty post-apply plan are demonstrated.

At each gate present what was verified, remaining decisions, the exact proposed action and targets, and rollback/recovery considerations. If authorization or capability is missing, continue unaffected local work and leave the dependent action pending. Do not substitute elapsed time or questionnaire preferences for execution approval.

## Credits

Thanks to [@briancripe](https://github.com/briancripe) for the initial prompt and the inspiration to adapt it into this skill.
