---
name: "Custom Fields Commands"
description: "Reference for listing, creating, updating, and deleting Memberstack custom fields, including visibility and admin restrictions."
tags: [custom-fields, list, create, update, delete, visibility, hidden, admin]
---

```
memberstack custom-fields <subcommand>
```

Requires OAuth authentication (`memberstack auth login`).

custom-fields list [#custom-fields-list]

List all custom fields.

```bash
memberstack custom-fields list
```

Example [#example]

```bash
$ memberstack custom-fields list
[
  {
    "id": "fld_abc123",
    "key": "tier",
    "label": "Member Tier",
    "visibility": "PUBLIC",
    "hidden": false
  }
]
```

custom-fields create [#custom-fields-create]

Create a new custom field.

```bash
memberstack custom-fields create --key <key> --label <label> [options]
```

Options [#options]

| Option                      | Description                             | Required |
| --------------------------- | --------------------------------------- | -------- |
| `--key <key>`               | Field key                               | Yes      |
| `--label <label>`           | Field label                             | Yes      |
| `--hidden`                  | Hide the field                          | No       |
| `--visibility <visibility>` | Field visibility: `PUBLIC` or `PRIVATE` | No       |
| `--restrict-to-admin`       | Restrict field to admin access          | No       |
| `--plan-ids <ids...>`       | Plan IDs to associate with the field    | No       |

Examples [#examples]

```bash
memberstack custom-fields create --key tier --label "Member Tier"

memberstack custom-fields create \
  --key vip \
  --label "VIP Status" \
  --visibility PRIVATE \
  --restrict-to-admin

memberstack custom-fields create --key type --label "Account Type" --hidden
```

custom-fields update [#custom-fields-update]

Update an existing custom field.

```bash
memberstack custom-fields update <id> [options]
```

Arguments [#arguments]

| Argument | Description     | Required |
| -------- | --------------- | -------- |
| `id`     | Custom field ID | Yes      |

Options [#options-1]

| Option                      | Description                             | Required |
| --------------------------- | --------------------------------------- | -------- |
| `--label <label>`           | Field label                             | Yes      |
| `--hidden`                  | Hide the field                          | No       |
| `--no-hidden`               | Show the field                          | No       |
| `--table-hidden`            | Hide the field from the table           | No       |
| `--no-table-hidden`         | Show the field in the table             | No       |
| `--visibility <visibility>` | Field visibility: `PUBLIC` or `PRIVATE` | No       |
| `--restrict-to-admin`       | Restrict field to admin access          | No       |
| `--no-restrict-to-admin`    | Remove admin restriction                | No       |

Examples [#examples-1]

```bash
memberstack custom-fields update fld_abc123 --label "Updated Tier" --hidden

memberstack custom-fields update fld_abc123 \
  --label "Member Status" \
  --no-hidden \
  --visibility PUBLIC
```

custom-fields delete [#custom-fields-delete]

Delete a custom field.

```bash
memberstack custom-fields delete <id>
```

Arguments [#arguments-1]

| Argument | Description     | Required |
| -------- | --------------- | -------- |
| `id`     | Custom field ID | Yes      |

Example [#example-1]

```bash
memberstack custom-fields delete fld_abc123
```
