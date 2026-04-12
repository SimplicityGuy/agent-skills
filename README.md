# Skills

A collection of Claude Code skills (`.skill.md` files) for common workflows.

## Available Skills

| Skill | Description |
|-------|-------------|
| [brand-asset-audit](brand-asset-audit.skill.md) | Audit and generate brand assets (logos, favicons, OG images, design system docs) |
| [comprehensive-docs](comprehensive-docs.skill.md) | Build a full `docs/` suite — index, categorized guides, role-based navigation, consistent formatting |
| [readme](readme.skill.md) | Create or restructure a project's root README with the standard section layout and emoji-prefixed headers |

## Setup

Add this directory to your Claude Code settings so all skills are automatically discovered.

**Project-level** (`.claude/settings.json` in your repo):

```json
{
  "skills": [
    "/path/to/skills/*.skill.md"
  ]
}
```

**User-level** (`~/.claude/settings.json`):

```json
{
  "skills": [
    "/path/to/skills/*.skill.md"
  ]
}
```

Replace `/path/to/skills` with the absolute path to this directory.

## Adding a New Skill

1. Create a `your-skill-name.skill.md` file in this directory
2. Include YAML frontmatter with `name` and `description` fields
3. The `description` field controls when Claude will suggest using the skill -- include trigger keywords

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

## License

See [LICENSE](LICENSE).
