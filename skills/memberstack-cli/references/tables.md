---
name: "Tables Commands"
description: "Reference for managing Memberstack data tables, including list, get, describe, create, update, and delete operations."
tags: [tables, list, get, describe, create, update, delete, schema, access-rules]
---

```
memberstack tables <subcommand>
```

Requires OAuth authentication (`memberstack auth login`).

tables list [#tables-list]

List all data tables.

```bash
memberstack tables list
```

Example [#example]

```bash
$ memberstack tables list
[
  {
    "id": "tbl_abc123",
    "name": "Products",
    "key": "products",
    ...
  }
]
```

tables get [#tables-get]

Get a data table by key or ID.

```bash
memberstack tables get <table_key>
```

Arguments [#arguments]

| Argument    | Description     | Required |
| ----------- | --------------- | -------- |
| `table_key` | Table key or ID | Yes      |

Examples [#examples]

```bash
memberstack tables get products
memberstack tables get tbl_abc123
```

tables describe [#tables-describe]

Show detailed schema information for a table.

```bash
memberstack tables describe <table_key>
```

Arguments [#arguments-1]

| Argument    | Description     | Required |
| ----------- | --------------- | -------- |
| `table_key` | Table key or ID | Yes      |

Description [#description]

Displays the table name, key, ID, access rules (create, read, update, delete), and all fields with their type, required status, and references.

Example [#example-1]

```bash
$ memberstack tables describe products
Table: Products
  Key:  products
  ID:   tbl_abc123

Access Rules:
  Create:  ADMIN
  Read:    PUBLIC
  Update:  ADMIN
  Delete:  ADMIN

Fields:
  name        String    required
  price       Number    required
  category    String
  owner       Relation  → members
```

tables create [#tables-create]

Create a new data table.

```bash
memberstack tables create [options]
```

Options [#options]

| Option                 | Description                      | Required |
| ---------------------- | -------------------------------- | -------- |
| `--name <name>`        | Table name                       | Yes      |
| `--key <key>`          | Table key (unique identifier)    | Yes      |
| `--create-rule <rule>` | Access rule for creating records | No       |
| `--read-rule <rule>`   | Access rule for reading records  | No       |
| `--update-rule <rule>` | Access rule for updating records | No       |
| `--delete-rule <rule>` | Access rule for deleting records | No       |

Access rule values: `PUBLIC`, `AUTHENTICATED`, `AUTHENTICATED_OWN`, `ADMIN_ONLY`

Examples [#examples-1]

```bash
memberstack tables create --name "Products" --key products
memberstack tables create --name "Orders" --key orders --create-rule AUTHENTICATED --read-rule PUBLIC
```

tables update [#tables-update]

Update a data table.

```bash
memberstack tables update <id> [options]
```

Arguments [#arguments-2]

| Argument | Description | Required |
| -------- | ----------- | -------- |
| `id`     | Table ID    | Yes      |

Options [#options-1]

| Option                 | Description                      |
| ---------------------- | -------------------------------- |
| `--name <name>`        | Table name                       |
| `--create-rule <rule>` | Access rule for creating records |
| `--read-rule <rule>`   | Access rule for reading records  |
| `--update-rule <rule>` | Access rule for updating records |
| `--delete-rule <rule>` | Access rule for deleting records |

Access rule values: `PUBLIC`, `AUTHENTICATED`, `AUTHENTICATED_OWN`, `ADMIN_ONLY`

Examples [#examples-2]

```bash
memberstack tables update tbl_abc123 --name "Updated Products"
memberstack tables update tbl_abc123 --delete-rule ADMIN_ONLY --read-rule PUBLIC
```

tables delete [#tables-delete]

Delete a data table.

```bash
memberstack tables delete <id>
```

Arguments [#arguments-3]

| Argument | Description | Required |
| -------- | ----------- | -------- |
| `id`     | Table ID    | Yes      |

Example [#example-2]

```bash
memberstack tables delete tbl_abc123
```
