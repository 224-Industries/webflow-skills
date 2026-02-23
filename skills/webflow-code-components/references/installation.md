---
name: "Installation & Configuration"
description: "Setup requirements for code components: installing the Webflow CLI and dependencies, configuring webflow.json, authentication, and workspace API tokens."
tags: [installation, setup, webflow-cli, webflow-json, configuration, authentication, workspace-token, npm]
---

# Installation & Configuration

This reference describes the configuration requirements to set up DevLink in a React project for component imports.

---

## Setup Requirements

### Webflow CLI

Install the Webflow CLI and the necessary dependencies to import React components into Webflow:

```bash
# Install the Webflow CLI globally
npm install -g @webflow/webflow-cli

# Install dependencies in your project
npm i --save-dev @webflow/data-types @webflow/react
```

**What you get:**

- `@webflow/webflow-cli` — CLI used to publish components to Webflow (installed globally)
- `@webflow/data-types` — TypeScript definitions for Webflow props
- `@webflow/react` — React utilities for code components

### `webflow.json`

The `webflow.json` file is used to configure DevLink for component imports. Use this file to define the name of your library and the components that should be included in the library. Additionally, you can specify a custom webpack configuration file to use for bundling your components.

Create or update `webflow.json` in the root of your project with the following configuration:

```json
{
  "library": {
    "name": "<Your Library Name>",
    "components": ["./src/**/*.webflow.@(js|jsx|mjs|ts|tsx)"],
    "bundleConfig": "./webpack.webflow.js",
    "globals": "./src/globals.webflow.ts"
  }
}
```

| Field | Description | Required |
|-------|-------------|----------|
| `library.name` | The name of your component library as it appears in Webflow | Yes |
| `library.components` | Glob pattern matching your component files | Yes |
| `library.bundleConfig` | Path to a custom webpack configuration file | No |
| `library.globals` | Path to a component decorators file | No |

## Authentication

When importing your component library to Webflow using the `npx webflow library share` command, the Webflow CLI will prompt you to authenticate with Webflow. Once authenticated, DevLink will save the token to your `.env` file.

### Manual Authentication

To manually authenticate with Webflow, run the `webflow library share` command with the `--api-token` option and include a Workspace API token in the command. This is useful when sharing your component library to a different workspace.

```bash
npx webflow library share --api-token <your-api-token>
```

### Workspace API Token

DevLink publishes your component library to a Webflow workspace. To publish to the correct workspace, you must provide a workspace API token for authentication.

> **Warning:** You must be a Workspace Admin to create a Workspace token.

To get your workspace API token:

1. Open your workspace and navigate to **Apps & Integrations.**
2. In the left sidebar, click **Manage**
3. Scroll to the bottom section labeled **Workspace API Access**
4. Click **Generate API Token** and copy the token.
5. Add the token to your `.env` file.

> **Warning:** Never commit your `.env` file to version control. Be sure to add `.env` to your `.gitignore` file.

## Next Steps

After configuration, you can:

- [Define a code component](define-code-component.md)
- [Bundle and import your library](bundling-and-import.md)

## Best Practices

- Always add `.env` to `.gitignore` to prevent leaking workspace tokens
- Use the `--api-token` flag in CI/CD instead of interactive authentication
- Keep `webflow.json` in the project root so the CLI can discover it automatically
