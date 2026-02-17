---
name: "Authentication Commands"
description: "OAuth authentication reference for Memberstack CLI login, logout, and status workflows with local token handling details."
tags: [auth, authentication, oauth, login, logout, status, tokens, pkce]
---

```
memberstack auth <subcommand>
```

The CLI supports OAuth authentication with your Memberstack account.

auth login [#auth-login]

Authenticate with Memberstack via the browser-based OAuth flow.

```bash
memberstack auth login
```

Description [#description]

Opens your default browser to the Memberstack authorization page. After you grant permission, the CLI receives an authorization code and exchanges it for access and refresh tokens using the PKCE flow.

Tokens are stored locally at `~/.memberstack/auth.json` with secure file permissions. The access token is used for authenticated requests directly to the Memberstack API, your credentials are never sent to third-party services.

Example [#example]

```bash
$ memberstack auth login
Opening browser for authentication...
✔ Authentication successful
```

auth logout [#auth-logout]

Remove stored authentication tokens.

```bash
memberstack auth logout
```

Description [#description-1]

Revokes the current refresh token (best-effort) and deletes the local token file at `~/.memberstack/auth.json`.

Example [#example-1]

```bash
$ memberstack auth logout
✔ Logged out successfully
```

auth status [#auth-status]

Show current authentication status.

```bash
memberstack auth status
```

Description [#description-2]

Displays whether you are currently authenticated, your app ID, token expiration time, refresh token availability, and token validity.

Example [#example-2]

```bash
$ memberstack auth status
Authentication Status
  Status:         Logged in
  App ID:         app_abc123
  Access Token:   Expires in 45 minutes
  Refresh Token:  Available
  Token Valid:    Yes
```
