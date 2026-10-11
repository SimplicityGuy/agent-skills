# Agent Skills

A collection of [Agent Skills](https://agentskills.io) for Claude Code, Codex, and other compatible agents. Each skill lives in `skills/<name>/SKILL.md`, with optional `references/` and other supporting files alongside it.

## Available Skills

| Skill | Description |
|-------|-------------|
| [brand-asset-audit](skills/brand-asset-audit/SKILL.md) | Audit and generate brand assets (logos, favicons, OG images, design system docs) |
| [comprehensive-docs](skills/comprehensive-docs/SKILL.md) | Build a full `docs/` suite — index, categorized guides, role-based navigation, consistent formatting |
| [deep-bug-hunt](skills/deep-bug-hunt/SKILL.md) | Multi-agent bug-hunt expedition: lens-based finders, adversarial verification, dedup, and filing of verified defects |
| [readme](skills/readme/SKILL.md) | Create or restructure a project's root README with the standard section layout and emoji-prefixed headers |
| [dependabot-setup](skills/dependabot-setup/SKILL.md) | Configure Dependabot on one repo, audit and fix an existing repo, or sweep a whole fleet |
| [monorepo-to-org](skills/monorepo-to-org/SKILL.md) | Guided private-first monorepo split with OpenTofu, SOPS, release gates, branding, Astro Pages, and optional standardized Dependabot |
| [org-repo-create](skills/org-repo-create/SKILL.md) | Create a private-first repository in an existing organization using infra-managed settings, developer gates, CI, and optional Dependabot |
| [repo-ci-setup](skills/repo-ci-setup/SKILL.md) | SHA-pinned workflows and required checks that block PRs |
| [homelab-github-settings](skills/homelab-github-settings/SKILL.md) | Adopt live SimplicityGuy repo settings (rulesets, labels, merge methods) into the homelab OpenTofu github module |
| [sudo-l7](skills/sudo-l7/SKILL.md) | Staff-engineer working mode: check the premise, surface unmentioned risks, push back, verify, report truthfully |

## Install

This repo is both a Claude Code plugin marketplace and a Codex plugin marketplace, serving one plugin, `agent-skills`, that contains every skill.

### Claude Code

```bash
claude plugin marketplace add SimplicityGuy/agent-skills
claude plugin install agent-skills@simplicityguy
```

Or inside a session: `/plugin marketplace add SimplicityGuy/agent-skills`, then `/plugin install agent-skills@simplicityguy`. Skills are namespaced by plugin, e.g. `/agent-skills:readme`.

### Codex

```bash
codex plugin marketplace add SimplicityGuy/agent-skills
```

Then install `agent-skills` from the Plugins directory. Update later with `codex plugin marketplace upgrade simplicityguy`.

### Standalone skills (no plugin)

Any tool that follows the [Agent Skills](https://agentskills.io) layout can load the skill folders directly:

Run from the root of a clone of this repo:

```bash
# Claude Code (user-level)
mkdir -p ~/.claude/skills
ln -s "$PWD"/skills/* ~/.claude/skills/

# Codex (user-level)
mkdir -p ~/.agents/skills
ln -s "$PWD"/skills/* ~/.agents/skills/
```

For a single project, link into that project's `.claude/skills/` or `.agents/skills/` instead.

## Adding a New Skill

1. Create `skills/your-skill-name/SKILL.md` (the directory name must match `name`)
2. Include YAML frontmatter with `name` and `description` fields
3. The `description` controls when the skill triggers -- include trigger keywords
4. Put long material in `references/` and link to it from `SKILL.md`

Template:

```markdown
---
name: your-skill-name
description: Use when [trigger conditions]. Triggers on "keyword1", "keyword2".
---

# Skill Title

## Overview
What this skill does.

## When to Use
- Condition 1
- Condition 2

## Process
Step-by-step instructions for Claude to follow.
```

## CI

The `Skill Lint` workflow (`.github/workflows/skill-lint.yml`) runs two linters over `skills/` on every pull request and on pushes to `main`:

- [agnix](https://github.com/agent-sh/agnix) (`agnix` job), configured for Claude Code
- [skill-check](https://github.com/thedaviddias/skill-check) (`skill-check` job)

The `Skill Security` workflow (`.github/workflows/skill-security.yml`) scans `skills/` with two static security scanners and uploads SARIF to Code Scanning:

- [Cisco skill-scanner](https://github.com/cisco-ai-defense/skill-scanner) (`skill-scanner` job), failing on HIGH or above
- [NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector) (`skillspector` job), failing when the risk score exceeds 50

Both run without the LLM judge, so no secrets are needed. Accepted skillspector findings are recorded with reasons in `.skillspector-baseline.yaml`.

Both lint jobs are required status checks on `main` via a `protect-main` ruleset, managed in the [homelab](https://github.com/SimplicityGuy/homelab) OpenTofu config. Changes to `main` go through a pull request.

## License

See [LICENSE](LICENSE).
