---
name: memberstack-cli
description: Use the Memberstack CLI to manage Memberstack accounts from the terminal. Covers authentication, apps, members, plans, custom fields, data tables, and records. Trigger this skill whenever the user wants to interact with Memberstack — including managing members, plans, custom fields, data tables/records, or authenticating with Memberstack. Also trigger when the user mentions "memberstack", "memberstack-cli", membership management, or member data operations via CLI.
license: MIT
compatibility: "memberstack-cli"
metadata:
  author: "[Ben Sabic](https://bensabic.dev)"
  version: "1.0.0"
---

# Memberstack CLI Skill

Manage your Memberstack account from the terminal using `memberstack-cli`.

## Prerequisites

Install globally and authenticate before running any commands:

```bash
npm install -g memberstack-cli
memberstack auth login
```

Authentication opens a browser for OAuth and stores tokens at `~/.memberstack/auth.json` with restricted file permissions. Use `memberstack auth logout` to clear credentials.

## Global Flags

All commands support these flags:
- `--json` / `-j` — Output raw JSON instead of formatted tables
- `--live` — Use live environment instead of sandbox (defaults to sandbox)

## Command Reference

The CLI has the following top-level commands. Read the corresponding reference file for full usage, options, and examples:

| Command | Purpose | Reference |
|---------|---------|-----------|
| `auth` | Login, logout, check status | `references/auth.md` |
| `whoami` | Show current identity | `references/whoami.md` |
| `apps` | Create, update, delete, restore apps | `references/apps.md` |
| `members` | List, create, update, delete, import/export, bulk ops | `references/members.md` |
| `plans` | List, create, update, delete, reorder plans | `references/plans.md` |
| `custom-fields` | List, create, update, delete custom fields | `references/custom-fields.md` |
| `tables` | List, create, update, delete data tables | `references/tables.md` |
| `records` | CRUD, query, import/export, bulk ops on table records | `references/records.md` |

Read `references/getting-started.md` for an overview of installation, authentication, and environment switching.

## Workflow Tips

- Always authenticate first with `memberstack auth login`. Verify with `memberstack whoami`.
- Use `--json` when you need to parse output programmatically or pipe to other tools.
- Default environment is **sandbox**. Pass `--live` for production operations.
- For bulk member operations, use `members import`, `members bulk-update`, or `members bulk-add-plan` with CSV/JSON files.
- For bulk record operations, use `records import`, `records bulk-update`, or `records bulk-delete`.
- Use `members find` and `records find` for friendly filter-based searches.

## Reference Documentation

Each reference file includes YAML frontmatter with `name`, `description`, and `tags` for searchability. Use the search script available in `scripts/search_references.py` to quickly find relevant references by tag or keyword.

- [Getting Started](references/getting-started.md): Quick-start guide for installing the Memberstack CLI, authenticating, and running core member, table, and record commands.
- [Authentication Commands](references/auth.md): OAuth authentication reference for Memberstack CLI login, logout, and status workflows with local token handling details.
- [Whoami Command](references/whoami.md): Reference for showing the currently authenticated Memberstack identity and environment context from the CLI.
- [Apps Commands](references/apps.md): Command reference for managing Memberstack apps, including create, update, delete, restore, and current app inspection.
- [Members Commands](references/members.md): Comprehensive command reference for Memberstack member management, including CRUD, plans, search, stats, and bulk workflows.
- [Plans Commands](references/plans.md): Reference for managing Memberstack plans, including listing, creation, updates, deletion, and plan priority ordering.
- [Custom Fields Commands](references/custom-fields.md): Reference for listing, creating, updating, and deleting Memberstack custom fields, including visibility and admin restrictions.
- [Tables Commands](references/tables.md): Reference for managing Memberstack data tables, including list, get, describe, create, update, and delete operations.
- [Records Commands](references/records.md): Reference for working with Memberstack table records, including CRUD, query, filtering, count, import/export, and bulk updates.

### Searching References

```bash
# List all references with metadata
python scripts/search_references.py --list

# Search by tag (exact match)
python scripts/search_references.py --tag <tag>

# Search by keyword (across name, description, tags, and content)
python scripts/search_references.py --search <query>
```