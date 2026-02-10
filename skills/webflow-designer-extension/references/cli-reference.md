---
name: "CLI Reference"
description: "Webflow CLI commands for initializing, developing, and bundling Designer Extensions."
tags: [cli, webflow-cli, init, serve, bundle, list, npm, development-workflow, hot-reload, templates, react, typescript, webflow-extension, project-setup, deployment]
---

# Webflow CLI Reference

## Installation

```bash
npm install -g @webflow/webflow-cli
# or yarn add global @webflow/webflow-cli
# or pnpm add -g @webflow/webflow-cli
```

## Commands

### init

Initialize a new Designer Extension project.

```bash
webflow extension init <project-name> [template]
```

**Arguments:**
- `project-name` (required): Project directory name
- `template` (optional): Framework template

**Available templates:**
```bash
webflow extension list  # View all templates
```

Common templates: `react`, `typescript`

**Example:**
```bash
webflow extension init my-extension react
cd my-extension
npm install
```

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

### bundle

Bundle extension for deployment.

```bash
webflow extension bundle
```

Creates `bundle.zip` in project root. Also available via:
```bash
npm run build
```

### list

List available project templates.

```bash
webflow extension list
```

## Development Workflow

1. Start dev server: `npm run dev`
2. Opens localhost:1337
3. Install app on test site (Workspace Settings > Apps & Integrations > Develop)
4. Open Designer, press "E" for app panel
5. Launch development app
6. Changes hot-reload automatically

## Dependencies

Keep updated:
- `@webflow/webflow-cli`
- `@webflow/designer-extension-typings`

```bash
npm update @webflow/webflow-cli @webflow/designer-extension-typings
```
