# Skills

A collection of Claude Code skills (`.skill.md` files) for common workflows.

## Available Skills

| Skill | Description |
|-------|-------------|
| [brand-asset-audit](brand-asset-audit.skill.md) | Audit and generate brand assets (logos, favicons, OG images, design system docs) |
| [comprehensive-docs](comprehensive-docs.skill.md) | Build a full `docs/` suite — index, categorized guides, role-based navigation, consistent formatting |
| [project-baseline](project-baseline/SKILL.md) | Bootstrap a new repo or audit an existing one against the standard kit — SHA-locked pre-commit, SHA-pinned workflows, dependabot, `update-project.sh`, justfile as command source-of-truth, Dockerfile OCI labels, Mermaid diagrams, ruff/mypy/bandit config, ≥85% coverage. Python + Rust + Node. |
| [readme](readme.skill.md) | Create or restructure a project's root README with the standard section layout and emoji-prefixed headers |

## Setup

Add this directory to your Claude Code settings so all skills are automatically discovered.

**Project-level** (`.claude/settings.json` in your repo):

```json
{
  "skills": [
    "/path/to/skills/*.skill.md",
    "/path/to/skills/*/SKILL.md"
  ]
}
```

**User-level** (`~/.claude/settings.json`):

```json
{
  "skills": [
    "/path/to/skills/*.skill.md",
    "/path/to/skills/*/SKILL.md"
  ]
}
```

Replace `/path/to/skills` with the absolute path to this directory. The two glob patterns cover both flat single-file skills (`*.skill.md`) and folder-based skills with bundled assets (`<name>/SKILL.md`).

## Adding a New Skill

Two layouts are supported:

- **Flat** — `your-skill-name.skill.md` at the repo root. Use when the skill is text-only.
- **Folder** — `your-skill-name/SKILL.md` plus an `assets/` subdirectory. Use when the skill bundles template files, scripts, or other artifacts that the skill instructions reference by path.

Steps:

1. Create the file (flat or folder)
2. Include YAML frontmatter with `name` and `description` fields
3. The `description` field controls when Claude will suggest using the skill -- include trigger keywords
4. For folder skills, reference bundled assets with relative paths (e.g. `assets/foo.yml`)

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
