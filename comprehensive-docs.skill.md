---
name: comprehensive-docs
description: Create and maintain a comprehensive end-user documentation suite in a docs/ directory — index page, categorized guides, consistent formatting, role-based navigation, and documentation standards. Use when setting up project docs from scratch or auditing/expanding existing docs.
---

# Comprehensive Docs Skill

Create and maintain a `docs/` directory with a full suite of end-user documentation. This is a **flexible** skill — adapt the specific doc categories and guides to the project, but follow the structural patterns exactly.

## Docs Directory Structure

```
docs/
  README.md              # Documentation index (required)
  quick-start.md         # Getting started guide (required)
  architecture.md        # System architecture (required for multi-component projects)
  configuration.md       # Environment variables and settings reference
  development.md         # Developer setup and workflow
  contributing.md        # How to contribute
  testing-guide.md       # Testing strategies and patterns
  troubleshooting.md     # Common issues and solutions
  monitoring.md          # Observability and debugging
  maintenance.md         # Keeping the system healthy
  performance-guide.md   # Optimization strategies
  ...                    # Additional guides as needed
```

Rules:
- **Lowercase filenames with hyphens**: `database-schema.md`, not `DatabaseSchema.md` or `db_schema.md`.
- **Descriptive names**: `database-backup-procedures.md` not `db-backup.md`. Avoid abbreviations unless widely known (`api`, `sql`, `ci`).
- **No subdirectories** for user-facing docs — keep them flat in `docs/`. Subdirectories are acceptable for internal/planning docs only (e.g., `docs/superpowers/`, `docs/planning/`).

## docs/README.md — The Documentation Index

The index is the entry point to all documentation. Structure it as follows:

### Header

```markdown
# Emoji Project Documentation

<div align="center">

**Brief tagline describing the documentation**

[Back-emoji Back to Main](../README.md) | [AI-emoji Claude Guide](../CLAUDE.md) | [Reference-emoji Key Reference](key-reference.md)

</div>
```

### Documentation Index (tables by category)

```markdown
## Emoji Documentation Index

### Emoji Category Name

| Document | Description |
| --- | --- |
| **[Display Name](filename.md)** | Emoji Brief description |
```

Rules:
- Group docs into **5-8 categories**. Common groupings:
  - **Getting Started**: quick-start, configuration, architecture
  - **Core Guides**: database schema, usage examples, monitoring, admin guide, troubleshooting
  - **Development**: development guide, contributing, testing, logging, language/version management
  - **Operations & Infrastructure**: Docker security, Dockerfile standards, database resilience, performance, maintenance
  - **Workflow & Automation**: CI/CD guide, task automation, monorepo guide
  - **Reference**: state management, indexing strategies, platform targeting, changelog/improvements
- Each doc entry: bold link + emoji-prefixed description.
- Keep descriptions under 80 characters.

### Role-Based Navigation

After the index tables, add a "Documentation by Role" section with ordered reading paths:

```markdown
## Emoji Documentation by Role

### For New Users

Start here to get up and running quickly:

1. **[Quick Start Guide](quick-start.md)** - Get running
1. **[Architecture Overview](architecture.md)** - Understand the system
1. **[Usage Examples](usage-examples.md)** - Try some queries
1. **[Configuration Guide](configuration.md)** - Customize settings

### For Developers

1. **[Development Guide](development.md)** - Set up your dev environment
1. **[Contributing Guide](contributing.md)** - Learn how to contribute
1. **[Testing Guide](testing-guide.md)** - Write and run tests
...

### For DevOps Engineers

1. **[Docker Security](docker-security.md)** - Secure containers
...

### For Troubleshooting

1. **[Troubleshooting Guide](troubleshooting.md)** - Common issues
...
```

Rules:
- 3-5 roles/personas. Common ones: New Users, Developers, DevOps Engineers, Data Engineers, Troubleshooting.
- Each role gets a numbered reading order (use `1.` for all items — markdown auto-numbers).
- 3-6 docs per role, ordered from foundational to advanced.

### Documentation Standards Section

Include a standards section covering:
- File naming convention
- Required structure for each doc (header, overview, sections, examples, related docs, last updated)
- Content guidelines (clear/concise, code examples, exact commands, Mermaid diagrams)
- Mermaid diagram conventions (consistent styling, meaningful colors, simplicity)

### Documentation Checklist

Include a checklist for doc contributions:

```markdown
### Documentation Checklist

Before submitting documentation changes:

- [ ] File name follows convention (lowercase-with-hyphens)
- [ ] Header includes title, description, and navigation
- [ ] Overview section explains the purpose
- [ ] Code examples are tested and work
- [ ] All links are valid
- [ ] Mermaid diagrams render correctly
- [ ] "Last Updated" date is current
- [ ] Added to docs/README.md index
- [ ] Updated main README.md if needed
```

### Search Tips Section

Add a "Finding Documentation" section organized by topic, by service/component, and by use case.

### Footer

```markdown
---

<div align="center">

**Last Updated**: YYYY-MM-DD

Made with heart-emoji by the ProjectName community

</div>
```

## Individual Doc Structure

Every doc in `docs/` follows this template:

### Header Block

```markdown
# Emoji Document Title

<div align="center">

**Brief description of what this document covers**

[Back-emoji Back to Main](../README.md) | [Docs-emoji Documentation Index](README.md) | [Related-emoji Related Doc](related-doc.md)

</div>
```

Rules:
- `# H1` with emoji prefix.
- Centered div with bold one-line description.
- Navigation bar with 2-4 pipe-separated links. Always include back-to-main and docs-index.
- Third link should be the most relevant related doc.

### Overview Section

```markdown
## Overview

Brief introduction to the topic — what it covers, why it matters, and who it's for. 2-4 sentences max.
```

### Body Sections

Use `##` for major sections and `###` for subsections. Each major section gets an emoji prefix.

**Content patterns to use throughout:**

**Tables** for structured reference data:
```markdown
| Column | Column | Column |
| --- | --- | --- |
| Data | Data | Data |
```

**Code blocks** with language fencing and comments:
```markdown
\```bash
# Brief explanation of what this does
command --with-flags
\```
```

**Step-by-step instructions** with numbered lists:
```markdown
### Step 1: Action Name

\```bash
command here
\```

Description of what happens and what to expect.
```

**Symptom/solution blocks** for troubleshooting:
```markdown
### Problem-emoji Problem Title

**Symptoms**:
- Observable symptom 1
- Observable symptom 2

**Diagnostic Steps**:
\```bash
diagnostic command
\```

**Solutions**:
1. **Check-emoji First thing to try**
   \```bash
   fix command
   \```
```

**Mermaid diagrams** for architecture and flows:
```markdown
\```mermaid
graph TD
    A[Component] --> B[Component]
    style A fill:#color,stroke:#color,stroke-width:2px
\```
```

Rules for Mermaid:
- Use `style` directives for color coding.
- Use descriptive labels with emoji prefixes and `<br/>` for multi-line.
- Keep focused — one concept per diagram.
- Use subgraphs to group related components.

### Related Documentation Section

```markdown
## Emoji Additional Resources / Related Documentation

- [Doc Name](filename.md) - Brief description
- [Doc Name](filename.md) - Brief description
```

Rules:
- 3-6 related docs.
- Always include the most logical "next step" doc.

### Footer

```markdown
---

**Last Updated**: YYYY-MM-DD
```

Rules:
- Horizontal rule above.
- Bold "Last Updated" with date.
- No centered div needed for individual docs (unlike docs/README.md and main README.md).

## Doc Categories and What to Include

### Required Docs (every project)

| Doc | Covers |
| --- | --- |
| `quick-start.md` | Prerequisites, system requirements table, minimal setup steps (clone + run), service URLs table with credentials, link to full config guide |
| `configuration.md` | Every environment variable with description, type, default, and required/optional. Group by service or concern. Include `_FILE` variants for secrets if applicable |
| `architecture.md` | Service/component table (name, purpose, tech, ports), Mermaid architecture diagram, data flow description, infrastructure components |

### Recommended Docs (most projects)

| Doc | Covers |
| --- | --- |
| `development.md` | Project structure, tooling, dev workflow, local setup beyond Docker |
| `contributing.md` | PR process, code standards, commit conventions, review expectations |
| `testing-guide.md` | Test structure, testing pyramid, coverage goals, how to run tests, patterns and fixtures |
| `troubleshooting.md` | Symptom-based organization, diagnostic commands, solutions with code |
| `monitoring.md` | Dashboards, metrics, health checks, debug utilities |

### Optional Docs (as complexity warrants)

| Doc | Covers |
| --- | --- |
| `database-schema.md` | Full schema reference for all databases |
| `performance-guide.md` | Tuning, benchmarks, hardware recommendations |
| `maintenance.md` | Dependency updates, backup procedures, cleanup |
| `logging-guide.md` | Log format standards, levels, structured logging |
| `docker-security.md` | Container hardening, non-root users, read-only FS |
| `*-guide.md` | Domain-specific guides as needed |

## Keeping Docs in Sync

When creating or updating docs:

1. **Add to docs/README.md** — every doc must appear in the index under the right category.
2. **Add to main README.md** — major guides should also appear in the root README's documentation section.
3. **Cross-link related docs** — each doc's "Related Documentation" section should link to 3-6 related docs.
4. **Update "Last Updated" dates** — set to today when making substantive changes.
5. **Test all code examples** — every command and code block should be verified working.
6. **Validate all links** — internal links are relative, external links are full URLs.

## General Rules

1. **Emoji usage**: `##` headers get emoji prefixes. Use emojis in table description columns. Don't overdo it in body text.
2. **Tables**: Use for any structured listing of 3+ items. Align columns.
3. **Code blocks**: Always use language-specific fencing. Include brief comments explaining non-obvious commands.
4. **Mermaid**: Use for architecture, data flow, and decision trees. Include `style` directives. Keep diagrams focused.
5. **Line length**: No hard wrap.
6. **Lists**: Use `1.` for all ordered list items (markdown auto-numbers). Use `-` for unordered lists.
7. **Bold for emphasis**: Use `**bold**` for key terms, tool names, and important callouts. Don't bold entire sentences.
8. **Links**: Relative for internal (`filename.md`), full URL for external. Bold the link text in tables.
9. **No trailing whitespace**.
10. **Single blank line** between sections.
