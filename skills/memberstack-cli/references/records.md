---
name: "Records Commands"
description: "Reference for working with Memberstack table records, including CRUD, query, filtering, count, import/export, and bulk updates."
tags: [records, create, update, delete, query, find, count, import, export, bulk-update, tables]
---

```
memberstack records <subcommand>
```

Requires OAuth authentication (`memberstack auth login`).

records create [#records-create]

Create a new record in a data table.

```bash
memberstack records create <table_key> --data <key=value> [options]
```

Arguments [#arguments]

| Argument    | Description     | Required |
| ----------- | --------------- | -------- |
| `table_key` | Table key or ID | Yes      |

Options [#options]

| Option               | Description                    | Required |
| -------------------- | ------------------------------ | -------- |
| `--data <key=value>` | Record field data (repeatable) | Yes      |

Example [#example]

```bash
memberstack records create products --data name=Widget --data price=29.99
```

records update [#records-update]

Update a record in a data table.

```bash
memberstack records update <table_key> <record_id> --data <key=value> [options]
```

Arguments [#arguments-1]

| Argument    | Description     | Required |
| ----------- | --------------- | -------- |
| `table_key` | Table key or ID | Yes      |
| `record_id` | Record ID       | Yes      |

Options [#options-1]

| Option               | Description                    | Required |
| -------------------- | ------------------------------ | -------- |
| `--data <key=value>` | Record field data (repeatable) | Yes      |

Example [#example-1]

```bash
memberstack records update products rec_abc123 --data price=39.99 --data status=active
```

records delete [#records-delete]

Delete a record from a data table.

```bash
memberstack records delete <table_key> <record_id>
```

Arguments [#arguments-2]

| Argument    | Description     | Required |
| ----------- | --------------- | -------- |
| `table_key` | Table key or ID | Yes      |
| `record_id` | Record ID       | Yes      |

Example [#example-2]

```bash
memberstack records delete products rec_abc123
```

records query [#records-query]

Query records using a JSON query body.

```bash
memberstack records query <table_key> --query <json>
```

Arguments [#arguments-3]

| Argument    | Description     | Required |
| ----------- | --------------- | -------- |
| `table_key` | Table key or ID | Yes      |

Options [#options-2]

| Option           | Description                 | Required |
| ---------------- | --------------------------- | -------- |
| `--query <json>` | Query body as a JSON string | Yes      |

Examples [#examples]

```bash
# Fetch first 10 records
memberstack records query products --query '{"pagination":{"first":10}}'

# Filter records by field value
memberstack records query products --query '{"filter":{"fieldFilters":{"status":{"equals":"active"}}}}'

# Paginate with cursor
memberstack records query products --query '{"pagination":{"first":10,"after":"cursor_abc"}}'
```

records count [#records-count]

Count records in a data table.

```bash
memberstack records count <table_key>
```

Arguments [#arguments-4]

| Argument    | Description     | Required |
| ----------- | --------------- | -------- |
| `table_key` | Table key or ID | Yes      |

Example [#example-3]

```bash
$ memberstack records count products
Total records: 256
```

records find [#records-find]

Find records with a friendly filter syntax.

```bash
memberstack records find <table_key> [options]
```

Arguments [#arguments-5]

| Argument    | Description     | Required |
| ----------- | --------------- | -------- |
| `table_key` | Table key or ID | Yes      |

Options [#options-3]

| Option             | Description                                          |
| ------------------ | ---------------------------------------------------- |
| `--where <clause>` | Filter clause: `"field operator value"` (repeatable) |
| `--take <n>`       | Limit number of results                              |

Supported Operators [#supported-operators]

`equals`, `not`, `in`, `notIn`, `lt`, `lte`, `gt`, `gte`, `contains`, `startsWith`, `endsWith`

Examples [#examples-1]

```bash
memberstack records find products --where "status equals active" --take 10
memberstack records find products --where "price gte 20" --where "category equals electronics"
memberstack records find products --where "name contains widget" --take 20
```

records export [#records-export]

Export all records from a data table.

```bash
memberstack records export <table_key> [options]
```

Arguments [#arguments-6]

| Argument    | Description     | Required |
| ----------- | --------------- | -------- |
| `table_key` | Table key or ID | Yes      |

Options [#options-4]

| Option              | Description                    | Default                             |
| ------------------- | ------------------------------ | ----------------------------------- |
| `--format <format>` | Output format: `csv` or `json` | `json`                              |
| `--output <path>`   | Output file path               | `records-{tableKey}.json` or `.csv` |

Examples [#examples-2]

```bash
memberstack records export products
memberstack records export products --format csv --output products.csv
```

Exported CSV files flatten nested fields with `data.*` prefixes.

records import [#records-import]

Import records into a data table from a file.

```bash
memberstack records import <table_key> --file <path>
```

Arguments [#arguments-7]

| Argument    | Description     | Required |
| ----------- | --------------- | -------- |
| `table_key` | Table key or ID | Yes      |

Options [#options-5]

| Option          | Description                   | Required |
| --------------- | ----------------------------- | -------- |
| `--file <path>` | Input file path (CSV or JSON) | Yes      |

File Format [#file-format]

CSV column headers can optionally use the `data.*` prefix. Both `name` and `data.name` are accepted.

Examples [#examples-3]

```bash
memberstack records import products --file records.csv
memberstack records import products --file records.json
```

records bulk-update [#records-bulk-update]

Bulk update records from a CSV or JSON file.

```bash
memberstack records bulk-update --file <path> [options]
```

Options [#options-6]

| Option          | Description                           | Required |
| --------------- | ------------------------------------- | -------- |
| `--file <path>` | Input file with record updates        | Yes      |
| `--dry-run`     | Preview changes without applying them | No       |

File Format [#file-format-1]

**Required fields:** `id`

**Optional fields:** `data.*` fields

Examples [#examples-4]

```bash
memberstack records bulk-update --file updates.csv
memberstack records bulk-update --file updates.csv --dry-run
```

records bulk-delete [#records-bulk-delete]

Bulk delete records matching a filter.

```bash
memberstack records bulk-delete <table_key> [options]
```

Arguments [#arguments-8]

| Argument    | Description     | Required |
| ----------- | --------------- | -------- |
| `table_key` | Table key or ID | Yes      |

Options [#options-7]

| Option             | Description                                          |
| ------------------ | ---------------------------------------------------- |
| `--where <clause>` | Filter clause: `"field operator value"` (repeatable) |
| `--dry-run`        | Preview deletions without applying them              |

Examples [#examples-5]

```bash
memberstack records bulk-delete products --where "status equals archived"
memberstack records bulk-delete products --where "price lt 5" --dry-run
```
