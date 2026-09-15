# Architecture

A living document for understanding how this repository is structured and how its parts fit together. Update as the codebase evolves.

## Project Structure

```
./
├── manifest.json                       # Source of truth — global config, keywords, skills array
├── skills/
│   ├── index.json                      # Generated — agent-skills-discovery RFC index
│   └── <skill-name>/
│       ├── SKILL.md                    # Entry point — frontmatter + instructions + reference index
│       ├── references/                 # Detailed reference docs (API guides, guidelines, etc.)
│       ├── scripts/                    # Helper scripts for the skill
│       └── assets/                     # Static assets (CSS, images, etc.)
├── scripts/
│   ├── sync-skills.js                  # Syncs manifest.json → plugin files, marketplace, index.json, README
│   └── add-skill.js                    # Scaffolds a new skill directory with SKILL.md
├── .claude-plugin/
│   ├── plugin.json                     # Generated — Claude Code plugin manifest
│   ├── plugin.schema.json              # JSON Schema for Claude Code plugin.json validation
│   └── marketplace.json                # Claude Code marketplace (single plugin entry)
├── .cursor-plugin/
│   ├── plugin.json                     # Generated — Cursor plugin manifest
│   └── plugin.schema.json              # JSON Schema for Cursor plugin.json validation
├── .github/
│   ├── workflows/validate-and-sync.yml # CI — validate skills, validate plugins, sync on main
│   └── CONTRIBUTING.md                 # Contribution guidelines
├── assets/                             # Shared static assets (logo, etc.)
├── CLAUDE.md                           # Project instructions for Claude Code
├── AGENTS.md                           # Project instructions for other AI coding agents
├── README.md                           # Public-facing documentation
└── LICENSE                             # MIT
```

## Data Flow

```
manifest.json ──────────────────────────────────────► SKILL.md (writes repository; author only if unset)
      │                                                  │
      │                                    reads frontmatter
      │                                                  │
      ▼                                                  ▼
  sync-skills.js ──updates──► manifest.json (preserves global fields, updates skills array)
        │
        ├──generates──► .claude-plugin/plugin.json      (from manifest global fields + keywords)
        ├──generates──► .claude-plugin/marketplace.json  (single plugin entry)
        ├──generates──► .cursor-plugin/plugin.json      (from manifest global fields + keywords + logo)
        ├──generates──► skills/index.json               (agent-skills-discovery RFC index)
        └──generates──► README.md                       (updates skills table)
```

### What lives where

| Data | Source of truth | Flows to |
|------|----------------|----------|
| Plugin name, description, author, homepage, repo, license | `manifest.json` (global fields) | Both plugin.json files, marketplace.json |
| Plugin keywords | `manifest.json` → `keywords` | Both plugin.json files, marketplace.json |
| Logo | `manifest.json` → `logo` | `.cursor-plugin/plugin.json` only |
| Repository | `manifest.json` (global fields) | `SKILL.md` → `metadata.repository` |
| Author (default) | `manifest.json` (global fields) | `SKILL.md` → `metadata.author`, only where the skill has not declared its own |
| Author (per skill) | `SKILL.md` → `metadata.author` | Preserved as-is; sync never overwrites it |
| Skill name, description, version, license | `SKILL.md` frontmatter | `manifest.json` → `skills[]`, `skills/index.json` |
| Skill keywords | `SKILL.md` → `metadata.keywords` | `manifest.json` → `skills[].keywords` |
| Skill file listing | Filesystem (skill directory contents) | `skills/index.json` → `skills[].files` |
| Plugin version | `manifest.json` → `version` | Both plugin.json files, marketplace.json |
| Skill version | `SKILL.md` → `metadata.version` | `manifest.json` → `skills[].version` |

## CI/CD Pipeline

**Workflow:** `.github/workflows/validate-and-sync.yml`

**Triggers:** Changes to `**/SKILL.md`, `manifest.json`, `.claude-plugin/**`, `.cursor-plugin/**` on `main` or PRs to `main`.

```
detect-changes
    ├──► validate-skills (matrix per changed skill, uses Flash-Brew-Digital/validate-skill@v1)
    ├──► validate-plugins (ajv against JSON schemas, only if plugin files changed)
    └──► sync (runs on main only, after both validation jobs pass or are skipped)
              ├── node scripts/sync-skills.js
              └── auto-commit generated files
```

The `sync` job uses `always() && !failure() && !cancelled()` so that skipped validation jobs (e.g. no plugin files changed) don't block it.

## Scripts

| Script | Purpose | Reads | Writes |
|--------|---------|-------|--------|
| `sync-skills.js` | Discover skills from `skills/*/SKILL.md`, update manifest and generated files | `SKILL.md` frontmatter, `manifest.json` | `manifest.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.cursor-plugin/plugin.json`, `skills/index.json`, `README.md` |
| `add-skill.js` | Scaffold a new skill | `manifest.json` | `skills/<name>/SKILL.md`, then calls `sync-skills.js` |

## Platform Differences

| Field | Claude Code | Cursor |
|-------|-------------|--------|
| `logo` | Not supported | Supported |
| `rules` | Not supported | Supported |
| `lspServers` | Supported | Not documented |
| `outputStyles` | Supported | Not documented |

Both platforms support: `name`, `description`, `version`, `author`, `homepage`, `repository`, `license`, `keywords`, `skills`, `commands`, `agents`, `hooks`, `mcpServers`.

## Project Identification

- **Project:** Webflow Agent Skills
- **Repository:** https://github.com/224-industries/webflow-skills
- **Maintainer:** [Ben Sabic](https://bensabic.dev) at [224 Industries](https://224industries.com.au)
- **License:** MIT
- **Last Updated:** 2026-09-15
