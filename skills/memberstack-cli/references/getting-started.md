---
name: "Getting Started"
description: "Quick-start guide for installing the Memberstack CLI, authenticating, and running core member, table, and record commands."
tags: [getting-started, installation, auth, quick-start, environment, json, pagination, import, export]
---

Installation [#installation]

```bash
npm install -g memberstack-cli
```

Authentication [#authentication]

Authenticate once with OAuth:

```bash
memberstack auth login
```

This opens your browser, authenticates with Memberstack, and stores tokens locally at `~/.memberstack/auth.json`.

See the [Authentication](/docs/auth) page for full details.

Use `memberstack whoami` to confirm your current authenticated identity.

Quick Start [#quick-start]

Check your identity [#check-your-identity]

```bash
memberstack whoami
```

List members [#list-members]

```bash
memberstack members list
memberstack members list --all --order DESC
```

Create a member [#create-a-member]

```bash
memberstack members create --email user@example.com --password secure123
```

View member statistics [#view-member-statistics]

```bash
memberstack members stats
```

Work with data tables [#work-with-data-tables]

```bash
memberstack tables list
memberstack tables describe my_table
memberstack records find my_table --where "status equals active"
```

Export and import [#export-and-import]

```bash
memberstack members export --format csv --output backup.csv
memberstack members import --file backup.csv
```

Command Reference [#command-reference]

| Command                              | Description                                                 |
| ------------------------------------ | ----------------------------------------------------------- |
| [apps](/docs/apps)                   | Manage apps (current, create, update, delete, restore)      |
| [auth](/docs/auth)                   | Manage OAuth authentication (login, logout, status)         |
| [whoami](/docs/whoami)               | Show current authenticated identity                         |
| [members](/docs/members)             | Manage members (CRUD, plans, import/export, bulk ops)       |
| [plans](/docs/plans)                 | Manage plans (list, get, create, update, delete, reorder)   |
| [tables](/docs/tables)               | Manage data tables (CRUD, describe)                         |
| [records](/docs/records)             | Manage table records (CRUD, query, import/export, bulk ops) |
| [custom-fields](/docs/custom-fields) | Manage custom fields (CRUD)                                 |

Global Behavior [#global-behavior]

* **Environment selection** — Commands run against sandbox by default. Add `--live` to target your live environment.
* **JSON output** — Add `--json` to print raw JSON instead of formatted output.
* **Pagination** — List commands use cursor-based pagination. Pass `--after <cursor>` to page through results, or use `--all` to auto-paginate.
* **Rate limiting** — Bulk operations insert a 100ms delay between API calls to avoid rate limits.
* **Dry-run mode** — Bulk commands support `--dry-run` to preview changes without applying them.
* **Key-value options** — Options like `--custom-fields` and `--data` accept repeatable `key=value` pairs.
* **File formats** — Import and export commands support both CSV and JSON formats.
