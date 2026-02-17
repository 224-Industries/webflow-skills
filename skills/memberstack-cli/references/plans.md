---
name: "Plans Commands"
description: "Reference for managing Memberstack plans, including listing, creation, updates, deletion, and plan priority ordering."
tags: [plans, list, get, create, update, delete, order, priority, permissions, domains]
---

```
memberstack plans <subcommand>
```

Requires OAuth authentication (`memberstack auth login`).

plans list [#plans-list]

List all plans.

```bash
memberstack plans list [options]
```

Options [#options]

| Option               | Description                                   |
| -------------------- | --------------------------------------------- |
| `--status <status>`  | Filter by status: `ALL`, `ACTIVE`, `INACTIVE` |
| `--order-by <field>` | Order by field: `PRIORITY`, `CREATED_AT`      |

plans get [#plans-get]

Get a plan by ID.

```bash
memberstack plans get <id>
```

Arguments [#arguments]

| Argument | Description |
| -------- | ----------- |
| `id`     | Plan ID     |

plans create [#plans-create]

Create a new plan.

```bash
memberstack plans create [options]
```

Options [#options-1]

| Option                                    | Description                     |
| ----------------------------------------- | ------------------------------- |
| `--name <name>`                           | Plan name                       |
| `--description <description>`             | Plan description                |
| `--icon <icon>`                           | Plan icon                       |
| `--is-paid`                               | Mark plan as paid               |
| `--team-accounts-enabled`                 | Enable team accounts            |
| `--team-account-invite-signup-link <url>` | Team account invite signup link |
| `--team-account-upgrade-link <url>`       | Team account upgrade link       |

Example [#example]

```bash
memberstack plans create --name "Pro" --description "Professional tier" --is-paid
```

plans update [#plans-update]

Update a plan.

```bash
memberstack plans update <id> [options]
```

Arguments [#arguments-1]

| Argument | Description |
| -------- | ----------- |
| `id`     | Plan ID     |

Options [#options-2]

| Option                                    | Description                                                                                                                                             |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--name <name>`                           | Plan name                                                                                                                                               |
| `--description <description>`             | Plan description                                                                                                                                        |
| `--icon <icon>`                           | Plan icon                                                                                                                                               |
| `--status <status>`                       | Plan status: `ACTIVE`, `INACTIVE`                                                                                                                       |
| `--limit-members`                         | Enable member limit                                                                                                                                     |
| `--no-limit-members`                      | Disable member limit                                                                                                                                    |
| `--member-limit <number>`                 | Maximum number of members                                                                                                                               |
| `--team-account-upgrade-link <url>`       | Team account upgrade link                                                                                                                               |
| `--team-account-invite-signup-link <url>` | Team account invite signup link                                                                                                                         |
| `--restrict-to-admin`                     | Restrict plan to admin                                                                                                                                  |
| `--no-restrict-to-admin`                  | Remove admin restriction                                                                                                                                |
| `--redirect <key=url>`                    | Set redirect URL (repeatable). Keys: `afterSignup`, `afterLogin`, `afterLogout`, `afterPurchase`, `afterCancel`, `afterReplace`, `verificationRequired` |
| `--permission-id <id>`                    | Permission ID (repeatable; replaces all permissions)                                                                                                    |
| `--allowed-domain <email>`                | Allowed email domain (repeatable; replaces all domains)                                                                                                 |

Example [#example-1]

```bash
memberstack plans update pln_abc123 --status ACTIVE --restrict-to-admin
```

plans delete [#plans-delete]

Delete a plan.

```bash
memberstack plans delete <id>
```

Arguments [#arguments-2]

| Argument | Description |
| -------- | ----------- |
| `id`     | Plan ID     |

plans order [#plans-order]

Reorder plans by priority.

```bash
memberstack plans order --plan <planId:priority> [--plan <planId:priority> ...]
```

Options [#options-3]

| Option                     | Description                                                       |
| -------------------------- | ----------------------------------------------------------------- |
| `--plan <planId:priority>` | Plan ID and priority (repeatable), for example `--plan pln_abc:1` |

Example [#example-2]

```bash
memberstack plans order --plan pln_basic:1 --plan pln_pro:2 --plan pln_enterprise:3
```
