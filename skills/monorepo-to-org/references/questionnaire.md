# Staged decision questionnaire

Ask two or three related questions per batch using the environment's question tool when appropriate, or ordinary chat. Offer useful options with tradeoffs and a free-text route. Each stage is a conversation, not a form that must be answered in one turn. Skip known answers, distinguish preferences from authorization, and record confirmed answers. Discover plan capabilities, manifests, tags, ownership, and dependency edges from evidence. Never ask for secrets.

## 1. Locate and scope

Ask first:

- Which monorepo (absolute path or URL) should be split, and which GitHub organization should receive it? Does the organization already exist?
- Who is the initial GitHub maintainer, and what parent workspace should hold prepared repositories?
- Is this design/local preparation only, or preparation followed by separately approved execution?

Confirm the resolved paths and identifiers. Discover local clones and auth status without displaying tokens. If the organization does not exist, prepare its creation proposal but wait for explicit creation approval.

## 2. Ownership and boundaries, after initial inventory

Show the discovered components and dependency graph, then ask:

- Who owns each product/service, and which teams or collaborators need access? Which components require restricted access or different distribution/license terms?
- Which components ship together, and which must release/deploy independently? Are any package names, registry locations, release channels, or consumers contractual constraints?
- Which history strategy is preferred: relevant history preserved (recommended), full history where justified, or an explicitly accepted snapshot? Which tags must survive?

Do not ask the operator to pick repository names before showing the source evidence. Propose cohesive boundaries and alternatives for cycles, shared schemas, and generated code. Clarify only decisions evidence cannot resolve. Existing secrets in history require a remediation decision before extraction/push; deletion from the new working tree alone is insufficient.

## 3. Organization policy and infrastructure

After discovering the GitHub plan and current rules, ask:

- Which merge workflow must survive: squash, rebase, preserved merge commits, or repository-specific policies? What required checks and review rules are desired where supported?
- Should state remain local and untracked initially (default), or is there an existing approved secure remote backend? Who may operate infra and recover it?
- Is this a compatible Mac for Secure Enclave encryption? What Touch ID and password/passcode fallback policy is desired, and what separate recovery recipient/offline recovery arrangement is acceptable?

Do not offer unsupported private protection as an implemented option. Explain state can contain provider secrets despite SOPS-encrypted inputs. Inspect actual keygen help before mapping the operator's policy to flags. Defer real secrets until a usable recovery design is in place.

## 4. Developer experience and dependency automation

Propose tooling based on detected ecosystems, then ask:

- Which versioned artifacts and registries are intended, and what is the version authority? Which repositories should remain unversioned?
- Are there existing signing, cross-platform, license, or expensive release gates that must be preserved separately from fast `just check`?
- Would you like the standardized Dependabot configuration using `agent-skills:dependabot-setup`: all applicable destination repositories, selected repositories, or skip?

Explain the standard briefly: detected ecosystems only, grouped version/security update PRs, existing directories and labels, and CI compatibility. If selected, establish scope, update assignee, and schedule/timezone; propose the existing skill's defaults where suitable. The choice authorizes preparation, not unreviewed secret copying, pushes, PR merges, or fleet operations.

## 5. Branding and public surfaces

Ask:

- What organization name, purpose, primary products, documentation links, and existing artwork should the public profile/site use?
- Should the Astro site use the default organization URL or an optional custom domain? Who controls DNS, and what existing service must remain available?
- Who reviews content, license obligations, retained history, and exposure before `.github` and the site become public?

Use existing branding if present; gather creative preferences only when new sources are needed. Public intent is not public-transition approval. Record any owner-only avatar/settings action.

## 6. Concrete approval checkpoints

Present the repository map for design approval. Later, request approval only for prepared actions with explicit targets: organization/manual infra creation; reviewed OpenTofu plan/apply; verified branch/tag pushes; reviewed public visibility and Pages; DNS with rollback; separately requested publication/release. Group related actions only when their exact scope and effects are clear. Do not force a predefined bundle of permissions.

For each checkpoint record the operator's answer, targets, plan/source revision, effects, and remaining pending actions. Re-review material changes to an approved plan. Keep cleanup of the original monorepo out of the initial migration authorization.
