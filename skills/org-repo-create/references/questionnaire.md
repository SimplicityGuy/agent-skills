# Staged new-repository questions

Use small batches with useful options and a free-text route. Record answers, separate preferences from execution approval, and skip known information. Questions describe decisions; discover credentials status, manifests, remote settings and plan features directly with redacted read-only checks.

## 1. Identity and existing organization

- Which existing GitHub organization, repository name and purpose/description should be used?
- Who maintains it, which teams/collaborators need access, and where should the local checkout be prepared?
- Where is the organization's private infra source of truth? Is the task local preparation only or preparation followed by separately approved provisioning?

Confirm identifiers, workspace path and infra ownership. Check for an existing repository/name collision without modifying it. If no infra is available, explain the dependency and continue local specification/scaffolding.

## 2. Product and source boundaries

- Is this a fresh project, an approved template, or existing source? What language/framework and package manager are intended? Offer stack choices only if the operator has not specified one.
- What license/distribution terms and security/access boundaries apply? Will it consume other private repositories or produce shared schemas/generated clients?
- Should it remain private (default) or eventually become public? If public, who reviews source, history, secrets and licensing before the transition?

For existing source, inspect ownership/history and scan secrets first. Copy/import only authorized material without modifying the source. If the task becomes decomposition of a monorepo, route to `monorepo-to-org` rather than approximating its inventory/history workflow. For templates, review inherited workflows, tokens, licenses and URLs; do not execute an unreviewed template installer automatically.

## 3. Developer and release interface

Present a stack-appropriate scaffold and ask:

- Which setup, test/build, development and deployment behaviors should the initial repository support? What expensive/signing/platform gates must be separate from fast `just check`?
- Does it own a versioned artifact (package, binary, image or product), and what version authority, registry/release channel and tag format apply? Or should it be unversioned?
- What required checks and merge workflow apply: organization defaults, squash/rebase, preserved merge commits, or documented overrides?

Discover the plan's protection support and explain limitations. Do not offer publication as part of setup. Use existing approved organization standards where answers already exist.

## 4. Optional automation and secrets

- Would you like standardized Dependabot through `agent-skills:dependabot-setup`, or skip it? If yes, confirm/update the default assignee, schedule and timezone.
- Does CI/deployment need any secrets or external identities? Prefer OIDC where supported; collect names/purpose/access requirements, never values.
- Are branding, documentation or Pages needed for this repository? Use existing infra assets; if Pages/custom DNS is requested, confirm intended URL and DNS owner.

Reuse the existing SOPS recipients and approved state/security design. Do not generate a new identity for every repository. If recipients, recovery or CI decryption need changes, prepare a separate reviewed proposal. Do not require Astro or Pages for a library or service.

## 5. Review and approval

Show the complete repository specification and local acceptance results. Then present the infra diff and protected plan summary, identifying any unrelated changes that prevent safe application. Request approval for exact provisioning actions only after preparation. Later present the verified initial push and any separately reviewed public/Pages/DNS actions. Explicit authorization may cover named batches; reuse it without broadening the scope. Leave publishing/releases as separate actions.
