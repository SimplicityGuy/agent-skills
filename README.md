# Agent Skills

A collection of [Agent Skills](https://agentskills.io) for Claude Code and other compatible agents. Each skill lives in `skills/<name>/SKILL.md`, with optional `references/` and other supporting files alongside it.

## Available Skills

| Skill | Description |
|-------|-------------|
| [brand-asset-audit](skills/brand-asset-audit/SKILL.md) | Audit and generate brand assets (logos, favicons, OG images, design system docs) |
| [comprehensive-docs](skills/comprehensive-docs/SKILL.md) | Build a full `docs/` suite — index, categorized guides, role-based navigation, consistent formatting |
| [deep-bug-hunt](skills/deep-bug-hunt/SKILL.md) | Multi-agent bug-hunt expedition: lens-based finders, adversarial verification, dedup, and filing of verified defects |
| [readme](skills/readme/SKILL.md) | Create or restructure a project's root README with the standard section layout and emoji-prefixed headers |
| [sudo-l7](skills/sudo-l7/SKILL.md) | Staff-engineer working mode: check the premise, surface unmentioned risks, push back, verify, report truthfully |

## Setup

Copy or symlink the skills you want into your skills directory:

```bash
# User-level (all projects)
ln -s "$PWD"/skills/* ~/.claude/skills/

# Project-level
ln -s "$PWD"/skills/* /path/to/project/.claude/skills/
```

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

Pull requests are checked by skill linters (see `.github/workflows/`); the check is required to merge.

## License

See [LICENSE](LICENSE).
