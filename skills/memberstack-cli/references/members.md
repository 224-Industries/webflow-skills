---
name: "Members Commands"
description: "Comprehensive command reference for Memberstack member management, including CRUD, plans, search, stats, and bulk workflows."
tags: [members, list, get, create, update, delete, plans, find, stats, import, export, bulk]
---

```
memberstack members <subcommand>
```

Requires OAuth authentication (`memberstack auth login`).

members list [#members-list]

List members with optional pagination and sorting.

```bash
memberstack members list [options]
```

Options [#options]

| Option             | Description                                   | Default |
| ------------------ | --------------------------------------------- | ------- |
| `--after <cursor>` | Pagination cursor (from previous `endCursor`) | —       |
| `--order <order>`  | Sort order: `ASC` or `DESC`                   | `ASC`   |
| `--limit <number>` | Maximum members to return (max 200)           | `50`    |
| `--all`            | Auto-paginate and fetch all members           | —       |

Examples [#examples]

```bash
memberstack members list
memberstack members list --limit 100 --order DESC
memberstack members list --all
```

Results are written to `members.json` in the current directory.

members get [#members-get]

Get a member by ID or email.

```bash
memberstack members get <id_or_email>
```

Arguments [#arguments]

| Argument      | Description                            | Required |
| ------------- | -------------------------------------- | -------- |
| `id_or_email` | Member ID (`mem_...`) or email address | Yes      |

Examples [#examples-1]

```bash
memberstack members get mem_abc123
memberstack members get user@example.com
```

members create [#members-create]

Create a new member.

```bash
memberstack members create [options]
```

Options [#options-1]

| Option                        | Description                       | Required |
| ----------------------------- | --------------------------------- | -------- |
| `--email <email>`             | Member email address              | Yes      |
| `--password <password>`       | Member password                   | Yes      |
| `--plans <planId>`            | Plan ID to connect (repeatable)   | No       |
| `--custom-fields <key=value>` | Custom field value (repeatable)   | No       |
| `--meta-data <key=value>`     | Metadata field value (repeatable) | No       |
| `--login-redirect <url>`      | Login redirect URL                | No       |

Examples [#examples-2]

```bash
memberstack members create --email user@example.com --password secure123

memberstack members create \
  --email user@example.com \
  --password secure123 \
  --plans pln_abc123 \
  --custom-fields tier=premium \
  --meta-data ref=partner
```

members update [#members-update]

Update an existing member.

```bash
memberstack members update <id> [options]
```

Arguments [#arguments-1]

| Argument | Description           | Required |
| -------- | --------------------- | -------- |
| `id`     | Member ID (`mem_...`) | Yes      |

Options [#options-2]

| Option                        | Description                       |
| ----------------------------- | --------------------------------- |
| `--email <email>`             | Update email address              |
| `--custom-fields <key=value>` | Custom field value (repeatable)   |
| `--meta-data <key=value>`     | Metadata field value (repeatable) |
| `--json <json>`               | Additional JSON data as a string  |
| `--login-redirect <url>`      | Login redirect URL                |

Examples [#examples-3]

```bash
memberstack members update mem_abc123 --email newemail@example.com
memberstack members update mem_abc123 --custom-fields tier=gold
```

members delete [#members-delete]

Delete a member.

```bash
memberstack members delete <id>
```

Arguments [#arguments-2]

| Argument | Description           | Required |
| -------- | --------------------- | -------- |
| `id`     | Member ID (`mem_...`) | Yes      |

Examples [#examples-4]

```bash
memberstack members delete mem_abc123
```

members add-plan [#members-add-plan]

Add a free plan to a member.

```bash
memberstack members add-plan <id> --plan-id <planId>
```

Arguments [#arguments-3]

| Argument | Description           | Required |
| -------- | --------------------- | -------- |
| `id`     | Member ID (`mem_...`) | Yes      |

Options [#options-3]

| Option               | Description                | Required |
| -------------------- | -------------------------- | -------- |
| `--plan-id <planId>` | Plan ID to add (`pln_...`) | Yes      |

Example [#example]

```bash
memberstack members add-plan mem_abc123 --plan-id pln_xyz789
```

members remove-plan [#members-remove-plan]

Remove a free plan from a member.

```bash
memberstack members remove-plan <id> --plan-id <planId>
```

Arguments [#arguments-4]

| Argument | Description           | Required |
| -------- | --------------------- | -------- |
| `id`     | Member ID (`mem_...`) | Yes      |

Options [#options-4]

| Option               | Description                   | Required |
| -------------------- | ----------------------------- | -------- |
| `--plan-id <planId>` | Plan ID to remove (`pln_...`) | Yes      |

Example [#example-1]

```bash
memberstack members remove-plan mem_abc123 --plan-id pln_xyz789
```

members count [#members-count]

Show total member count.

```bash
memberstack members count
```

Example [#example-2]

```bash
$ memberstack members count
Total members: 1,234
```

members find [#members-find]

Find members by custom field values or plan.

```bash
memberstack members find [options]
```

Options [#options-5]

| Option                | Description                         |
| --------------------- | ----------------------------------- |
| `--field <key=value>` | Filter by custom field (repeatable) |
| `--plan <planId>`     | Filter by plan ID                   |

Examples [#examples-5]

```bash
memberstack members find --plan pln_abc123
memberstack members find --field tier=premium --field status=active
```

members stats [#members-stats]

Show member statistics.

```bash
memberstack members stats
```

Description [#description]

Displays an overview of member activity including total count, active vs inactive members, recent signups, and a breakdown by plan.

Example [#example-3]

```bash
$ memberstack members stats
Member Statistics
  Total members:       1,234
  Active members:      1,100
  Inactive members:    134
  Signups (7 days):    42
  Signups (30 days):   187

Members by Plan:
  Free Plan:           800
  Pro Plan:            300
  Enterprise:          100
  No Plan:             34
```

members export [#members-export]

Export all members to CSV or JSON.

```bash
memberstack members export [options]
```

Options [#options-6]

| Option              | Description                    | Default                         |
| ------------------- | ------------------------------ | ------------------------------- |
| `--format <format>` | Output format: `csv` or `json` | `json`                          |
| `--output <path>`   | Output file path               | `members.json` or `members.csv` |

Examples [#examples-6]

```bash
memberstack members export
memberstack members export --format csv --output members-backup.csv
```

Exported CSV files flatten nested fields with `customFields.*` and `metaData.*` prefixes.

members import [#members-import]

Import members from a CSV or JSON file.

```bash
memberstack members import --file <path>
```

Options [#options-7]

| Option          | Description                   | Required |
| --------------- | ----------------------------- | -------- |
| `--file <path>` | Input file path (CSV or JSON) | Yes      |

File Format [#file-format]

**Required fields:** `email`, `password`

**Optional fields:** `plans` (comma-separated plan IDs), `loginRedirect`, `customFields.*`, `metaData.*`

Examples [#examples-7]

```bash
memberstack members import --file members.csv
memberstack members import --file members.json
```

members bulk-update [#members-bulk-update]

Bulk update members from a CSV or JSON file.

```bash
memberstack members bulk-update --file <path> [options]
```

Options [#options-8]

| Option          | Description                           | Required |
| --------------- | ------------------------------------- | -------- |
| `--file <path>` | Input file with member updates        | Yes      |
| `--dry-run`     | Preview changes without applying them | No       |

File Format [#file-format-1]

**Required fields:** `id`

**Optional fields:** `email`, `loginRedirect`, `customFields.*`, `metaData.*`

Examples [#examples-8]

```bash
memberstack members bulk-update --file updates.csv
memberstack members bulk-update --file updates.csv --dry-run
```

members bulk-add-plan [#members-bulk-add-plan]

Add a plan to multiple members at once.

```bash
memberstack members bulk-add-plan --plan <planId> --filter <filter> [options]
```

Options [#options-9]

| Option              | Description                       | Required |
| ------------------- | --------------------------------- | -------- |
| `--plan <planId>`   | Plan ID to add (`pln_...`)        | Yes      |
| `--filter <filter>` | Member filter: `no-plan` or `all` | Yes      |
| `--dry-run`         | Preview without applying changes  | No       |

Examples [#examples-9]

```bash
memberstack members bulk-add-plan --plan pln_abc123 --filter no-plan
memberstack members bulk-add-plan --plan pln_abc123 --filter all --dry-run
```
