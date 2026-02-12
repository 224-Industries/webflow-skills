# Contributing to Webflow Agent Skills by 224 Industries

Thank you for your interest in contributing to our Webflow Agent Skills! We welcome contributions of all kinds, whether it's fixing inaccuracies in Webflow API references, improving existing skills, adding new reference documentation, or proposing entirely new Webflow-related skills.

By contributing, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming and respectful community for all.

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Skill Structure](#skill-structure)
- [Reference File Conventions](#reference-file-conventions)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Need Help?](#need-help)

## Ways to Contribute

- **Fix inaccuracies**: Spot an outdated Webflow API method or incorrect example? Submit a fix
- **Improve references**: Make existing Webflow documentation clearer, more complete, or better structured
- **Add references**: Contribute new reference files for Webflow APIs or topics not yet covered
- **Propose new skills**: Have an idea for a new Webflow Agent Skill? Open an issue to discuss it
- **Report issues**: Found something broken or misleading? Let us know

## Getting Started

### Prerequisites

- Node.js 20+
- Familiarity with Markdown and YAML frontmatter
- Understanding of Webflow's ecosystem (Designer API, Data API, etc.)

### Setup

1. Fork the repository on GitHub

2. Clone your fork locally:

   ```bash
   git clone https://github.com/your-username/webflow-skills.git
   cd webflow-skills
   ```

3. Review the repo structure:

   ```
   skills/<skill-name>/
   ├── SKILL.md                    # Entry point with frontmatter + overview + reference index
   ├── references/                 # Detailed reference docs
   ├── scripts/                    # Helper scripts for the skill
   ├── assets/                     # Static assets (CSS, images, etc.)
   └── .claude-plugin/plugin.json  # Plugin metadata (auto-synced from SKILL.md frontmatter)
   ```

## Skill Structure

Each skill lives in `skills/<skill-name>/` and is anchored by a `SKILL.md` file with YAML frontmatter:

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

The `SKILL.md` should include a quick start workflow, core patterns, and a reference index linking to all files in `references/`.

To scaffold a new skill:

```bash
node scripts/add-skill.js <skill-name> "<description>"
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

### Content guidelines

- **Plain Markdown only** — no JSX components (`<Tabs>`, `<Steps>`, `<Note>`, `<Frame>`, etc.)
- Use fenced code blocks with language identifiers (e.g., ` ```typescript `)
- Use Markdown tables for structured data
- Use blockquotes (`>`) for callouts and notes
- Include a **Table of Contents** with a horizontal rule separator after it
- End each reference with a **Best Practices** section where applicable
- Keep references focused on one API domain or topic per file

### When adapting from Webflow docs

Webflow's official documentation often uses JSX/HTML components. Convert these to plain Markdown:

| Source component | Convert to |
|---|---|
| `<Tabs>` / `<Tab>` | Separate sections with `###` headings |
| `<Note>` / `<Warning>` | Blockquote (`>`) |
| `<Steps>` / `<Step>` | Numbered list with `###` sub-headings |
| `<Accordion>` | Standard Markdown table or section |
| `<Frame>` / `<img>` | Remove (image URLs won't resolve in this context) |
| `<Button>` / `<a>` | Inline Markdown link |

## Development Workflow

1. Create a new branch for your changes:

   ```bash
   git checkout -b feat/your-change-description
   ```

2. Make your changes following the conventions above

3. If you added or removed reference files, update the corresponding `SKILL.md` reference index

4. If you changed `SKILL.md` frontmatter, run:

   ```bash
   node scripts/sync-skills.js
   ```

5. Commit your changes and push to your fork

## Pull Request Process

### Before Submitting

- Reference files have valid YAML frontmatter (`name`, `description`, `tags`)
- `SKILL.md` reference index is up to date with any added/removed files
- Code examples are accurate and use correct Webflow API methods
- Content follows the Markdown-only convention (no JSX/HTML components from Webflow docs)

### PR Guidelines

1. **Clear title**: Describe what changed (e.g., "Update variables-api.md to match latest Webflow Designer API docs")
2. **Description**: Explain what changed and why
3. **Link issues**: Reference any related issues (e.g., "Fixes #123")

> Use common sense when drafting your pull request. The goal is to make it easy for maintainers to review and merge your changes. Include sufficient details but avoid unnecessary information.

---

## Need Help?

- **GitHub Issues**: For bug reports, inaccuracies, and feature requests
- **GitHub Discussions**: For questions and community support

Thank you for contributing!
