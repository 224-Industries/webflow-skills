---
name: "CLI Reference"
description: "Reference for the Webflow CLI: commands for sharing, bundling, and debugging code component libraries via DevLink."
tags: [cli, webflow-cli, library-share, library-bundle, library-log, devlink, cicd, flags, debugging]
---

# CLI Reference

A command-line tool for managing DevLink — handles authentication, bundling, and importing code component libraries.

---

## Installation

```bash
npm install -g @webflow/webflow-cli
```

## Commands

### `webflow library share`

Shares your component library to your Workspace. This is the primary command for importing components to Webflow.

The CLI will:

1. Check `.env` for a Workspace auth token (prompts browser login if missing)
2. Bundle the library and request component confirmation
3. Upload the library to your Workspace

```bash
npx webflow library share
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `--manifest` | Path to `webflow.json` | Scans current directory |
| `--api-token` | Pass a Workspace API token directly | Uses `WEBFLOW_WORKSPACE_API_TOKEN` from `.env` |
| `--no-input` | Skips all interactive prompts (for CI/CD) | Off |
| `--verbose` | Extra debug output | Off |
| `--dev` | Disables minification and source maps | Off |

### `webflow library bundle`

Bundles the library locally for testing without uploading to Webflow.

```bash
npx webflow library bundle --public-path http://localhost:4000/
```

**Options:**

| Flag | Description |
|------|-------------|
| `--public-path` | URL where the library will be served (required) |
| `--force` | Continues compilation even with warnings |
| `--dev` | Development mode — disables minification and source maps |
| `--debug-bundler` | Prints the final webpack configuration |

### `webflow library log`

Retrieves debug logs from the most recent library import.

```bash
npx webflow library log
```

## CI/CD Usage

Append `--no-input` to prevent interactive prompts in automated pipelines:

```bash
npx webflow library share --no-input
```

> **Warning:** Implement change detection before sharing in CI/CD to avoid accidentally removing components. Only share when components have actually changed.

## Troubleshooting

### Authentication issues

- Confirm `.env` contains `WEBFLOW_WORKSPACE_API_TOKEN` (must be a Workspace token, not a Site token)
- Run with `--verbose` for additional output
- Pass the token directly via `--api-token <your-token>`

### Component removal warnings

The CLI compares the current library state against the previous import. Renaming a `.webflow.tsx` file causes the old component to be removed and a new one created in its place — existing instances on sites will break.

## Best Practices

- Use `--no-input` and `--api-token` in CI/CD pipelines for non-interactive authentication
- Always test bundles locally with `webflow library bundle` before sharing to production
- Use `--debug-bundler` to inspect the final webpack configuration when troubleshooting build issues
- Use `webflow library log` to diagnose import failures
- Add change detection in automated workflows to prevent accidental component removal
