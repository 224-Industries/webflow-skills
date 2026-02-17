---
name: "Whoami Command"
description: "Reference for showing the currently authenticated Memberstack identity and environment context from the CLI."
tags: [whoami, identity, auth, environment, sandbox, live, json]
---

```bash
memberstack whoami
```

Run `memberstack auth login` first if you are not authenticated yet.

By default the CLI targets sandbox. Add `--live` for live mode, and `--json` for raw JSON output.

Example [#example]

```bash
$ memberstack auth login
$ memberstack whoami
Email:        user@example.com
App:          app_abc123
Environment:  sandbox

$ memberstack whoami --live
Email:        user@example.com
App:          app_live456
Environment:  live
```
