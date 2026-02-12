# 224 Industries Skills Repository

This repo contains Webflow Agent Skills — folders of instructions, references, scripts, and assets that AI agents use to work more accurately with the Webflow ecosystem.

## Repo Structure

```
skills/<skill-name>/
├── SKILL.md                    # Entry point — frontmatter + overview + reference index
├── references/                 # Detailed reference docs (API guides, guidelines, etc.)
├── scripts/                    # Helper scripts for the skill
├── assets/                     # Static assets (CSS, images, etc.)
└── .claude-plugin/plugin.json  # Plugin metadata (auto-synced from SKILL.md frontmatter)
```

## Reference File Conventions

Every file in `references/` must have YAML frontmatter with three fields:

```yaml
---
name: "Human-Readable Title"
description: "One-line summary of the file's contents."
tags: [tag1, tag2, tag3]
---
```

- **name**: Descriptive title (e.g., "Elements API", "Marketplace Guidelines")
- **description**: Single sentence summarizing what the file covers
- **tags**: Array of searchable keywords — include API method names, category terms, and key concepts

### Content style

- Plain markdown only — no JSX components (`<Tabs>`, `<Steps>`, `<Note>`, `<Frame>`, etc.)
- Use fenced code blocks with language identifiers (e.g., ` ```typescript `)
- Use markdown tables for structured data
- Use blockquotes (`>`) for callouts and notes
- End each reference with a "Best Practices" section where applicable
- Keep references focused on one API domain or topic per file

### When adding references from external docs

Source documentation (e.g., Webflow's official docs) often uses JSX/HTML components. Strip these when converting:

| Source component | Convert to |
|---|---|
| `<Tabs>` / `<Tab>` | Separate sections with `###` headings |
| `<Note>` / `<Warning>` | Blockquote (`>`) |
| `<Steps>` / `<Step>` | Numbered list with `###` sub-headings |
| `<Accordion>` | Standard markdown table or section |
| `<Frame>` / `<img>` | Remove (image URLs won't resolve in this context) |
| `<Button>` / `<a>` | Inline markdown link |

## SKILL.md Frontmatter

```yaml
---
name: skill-name
description: One-line description used for discovery and matching.
license: MIT
metadata:
  author: "Author Name"
  version: "1.0.0"
---
```

The SKILL.md should include:
- Quick start workflow
- Core API patterns with code examples
- Reference Documentation section linking to all files in `references/`
- Scripts and assets 
- License information (must be an OSI-approved license)

## Scripts

- `node scripts/add-skill.js <name> "<description>"` — Scaffold a new skill
- `node scripts/sync-skills.js` — Sync README.md and marketplace.json with skills directory

## Workflow

1. Add or edit reference files in `skills/<name>/references/`
2. Update `SKILL.md` reference links if files were added/removed/renamed
3. Run `node scripts/sync-skills.js` if SKILL.md frontmatter changed
