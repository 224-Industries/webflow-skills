---
name: "Apps Commands"
description: "Command reference for managing Memberstack apps, including create, update, delete, restore, and current app inspection."
tags: [apps, current, create, update, delete, restore, stack, wordpress, settings]
---

```
memberstack apps <subcommand>
```

Requires OAuth authentication (`memberstack auth login`).

apps current [#apps-current]

Show the current app.

```bash
memberstack apps current
```

apps create [#apps-create]

Create a new app.

```bash
memberstack apps create [options]
```

Options [#options]

| Option                               | Description                                                                                                  |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| `--name <name>`                      | App name                                                                                                     |
| `--stack <stack>`                    | Tech stack: `REACT`, `WEBFLOW`, `VANILLA`, `WORDPRESS`                                                       |
| `--wordpress-page-builder <builder>` | WordPress page builder: `GUTENBERG`, `ELEMENTOR`, `DIVI`, `BEAVER_BUILDER`, `BRICKS`, `CORNERSTONE`, `OTHER` |
| `--template-id <templateId>`         | Template ID to use                                                                                           |

Example [#example]

```bash
memberstack apps create --name "My App" --stack REACT
```

apps update [#apps-update]

Update the current app.

```bash
memberstack apps update [options]
```

Options [#options-1]

| Option                                  | Description                                            |
| --------------------------------------- | ------------------------------------------------------ |
| `--name <name>`                         | App name                                               |
| `--stack <stack>`                       | Tech stack: `REACT`, `WEBFLOW`, `VANILLA`, `WORDPRESS` |
| `--status <status>`                     | App status: `ACTIVE`, `DELETED`                        |
| `--wordpress-page-builder <builder>`    | WordPress page builder                                 |
| `--business-entity-name <name>`         | Business entity name                                   |
| `--terms-of-service-url <url>`          | Terms of service URL                                   |
| `--privacy-policy-url <url>`            | Privacy policy URL                                     |
| `--prevent-disposable-emails`           | Prevent disposable emails                              |
| `--no-prevent-disposable-emails`        | Allow disposable emails                                |
| `--captcha-enabled`                     | Enable captcha                                         |
| `--no-captcha-enabled`                  | Disable captcha                                        |
| `--require-user-2fa`                    | Require user 2FA                                       |
| `--no-require-user-2fa`                 | Disable required 2FA                                   |
| `--disable-concurrent-logins`           | Disable concurrent logins                              |
| `--no-disable-concurrent-logins`        | Allow concurrent logins                                |
| `--member-session-duration-days <days>` | Member session duration in days                        |
| `--allow-member-self-delete`            | Allow members to self-delete                           |
| `--no-allow-member-self-delete`         | Prevent member self-deletion                           |

Example [#example-1]

```bash
memberstack apps update --name "Acme App" --captcha-enabled --require-user-2fa
```

apps delete [#apps-delete]

Delete an app.

```bash
memberstack apps delete --app-id <appId>
```

Options [#options-2]

| Option             | Description      |
| ------------------ | ---------------- |
| `--app-id <appId>` | App ID to delete |

apps restore [#apps-restore]

Restore a deleted app.

```bash
memberstack apps restore --app-id <appId>
```

Options [#options-3]

| Option             | Description       |
| ------------------ | ----------------- |
| `--app-id <appId>` | App ID to restore |
