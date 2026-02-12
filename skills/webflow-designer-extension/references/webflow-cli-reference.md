---
name: "Webflow CLI Reference"
description: "Webflow CLI commands for serving, bundling, and managing Designer Extensions during development."
tags: [cli, webflow-cli, serve, bundle, list, development-workflow, hot-reload, deployment, localhost, webflow-extension]
---

# Webflow CLI Reference

The Webflow CLI (`@webflow/webflow-cli`) provides commands for developing and bundling Designer Extensions. For scaffolding new projects, use [`create-webflow-extension`](create-webflow-extension-reference.md).

## Table of Contents

- [Installation](#installation)
- [Commands](#commands)
- [Development Workflow](#development-workflow)
- [Dependencies](#dependencies)

---

## Installation

```bash
npm install -g @webflow/webflow-cli
# or
pnpm add -g @webflow/webflow-cli
```

## Commands

### serve

Serve extension locally for development.

```bash
webflow extension serve [--port PORT]
```

**Options:**
- `--port`: Custom port (default: 1337)

**Example:**
```bash
webflow extension serve --port 3000
```

> **Note:** Projects scaffolded with `create-webflow-extension` wrap this via `pnpm dev` (or `npm run dev` / `yarn dev` / `bun dev`).

### bundle

Bundle extension for deployment.

```bash
webflow extension bundle
```

Creates `bundle.zip` in the project root. Projects scaffolded with `create-webflow-extension` also expose this via `pnpm build`.

### list

List available project templates.

```bash
webflow extension list
```

## Development Workflow

1. Start dev server: `pnpm dev` (runs `webflow extension serve` under the hood)
2. Serves at localhost:1337
3. Install app on test site via Workspace Settings > Apps & Integrations > Develop
4. Open Designer, press **E** for app panel
5. Launch development app
6. Changes hot-reload automatically

## Dependencies

Keep updated:
- `@webflow/webflow-cli`
- `@webflow/designer-extension-typings`

```bash
pnpm update @webflow/webflow-cli @webflow/designer-extension-typings
```
