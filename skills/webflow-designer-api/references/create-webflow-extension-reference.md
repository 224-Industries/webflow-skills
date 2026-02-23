---
name: "create-webflow-extension Reference"
description: "create-webflow-extension CLI for scaffolding new Webflow Designer Extension projects."
tags: [cli, create-webflow-extension, scaffold, npx, react, typescript, rspack, designer-extension, project-setup, pnpm, npm, yarn, bun, oxlint, biome, eslint, linter, formatter, interactive, ci, non-interactive]
---

# create-webflow-extension CLI Reference

Scaffold a new Webflow Designer Extension project with a built-in template. The CLI sets up a fully configured project using React 19, TypeScript, Rspack, custom Designer API hooks, and a configurable linter/formatter.

## Table of Contents

- [Usage](#usage)
- [Options](#options)
- [Interactive Mode](#interactive-mode)
- [Non-Interactive / CI Mode](#non-interactive--ci-mode)
- [Project Name Sanitization](#project-name-sanitization)
- [Generated Project Stack](#generated-project-stack)
- [Development Workflow](#development-workflow)

---

## Usage

```bash
npx create-webflow-extension@latest [name] [options]
```

**Arguments:**
- `name` (optional): Project name. If omitted, the CLI prompts for it interactively (or defaults to `my-webflow-extension` in quiet mode).

## Options

| Flag | Description |
|---|---|
| `-n, --name <name>` | Project name (alternative to positional argument) |
| `--pm <manager>` | Package manager: `pnpm` (recommended), `npm`, `yarn`, or `bun` |
| `-l, --linter <linter>` | Linter and formatter: `oxlint` (recommended), `biome`, or `eslint` |
| `--sg, --skip-git` | Skip initializing a git repository |
| `--si, --skip-install` | Skip installing dependencies |
| `-q, --quiet` | Non-interactive mode; suppresses prompts and visual output |
| `-V, --version` | Show version number |
| `-h, --help` | Show help |

## Interactive Mode

By default the CLI runs interactively, prompting for any options not provided on the command line.

```bash
npx create-webflow-extension@latest
```

The interactive prompts ask for:

1. **Project name** - defaults to "My Webflow Extension"
2. **Package manager** - select from pnpm (recommended), npm, yarn, or bun
3. **Linter and formatter** - select from Oxlint/Oxfmt (recommended), Biome, or ESLint/Prettier/Stylelint
4. **Skip git init** - confirm whether to skip git repository initialization

You can pre-fill some options and let the CLI prompt for the rest:

```bash
npx create-webflow-extension@latest my-extension --pm pnpm
# Only prompts for linter and git init
```

## Non-Interactive / CI Mode

Pass `-q, --quiet` along with all required options to run without prompts. This is useful for CI pipelines and automated workflows.

```bash
npx create-webflow-extension@latest \
  -n my-extension \
  --pm pnpm \
  -l oxlint \
  --skip-git \
  --skip-install \
  -q
```

Minimal quiet invocation (uses defaults: pnpm, oxlint, git enabled):

```bash
npx create-webflow-extension@latest my-extension -q
```

In quiet mode, if the target directory already exists the CLI exits with an error instead of prompting to overwrite.

## Project Name Sanitization

The provided project name is automatically sanitized:

- Converted to lowercase
- Spaces replaced with hyphens
- Special characters (anything not `a-z`, `0-9`, or `-`) removed
- Consecutive hyphens collapsed into one
- Leading and trailing hyphens stripped
- Truncated to 214 characters
- Falls back to `my-webflow-extension` if the result is empty

**Examples:**

| Input | Sanitized |
|---|---|
| `My Webflow Extension` | `my-webflow-extension` |
| `Hello World!!!` | `hello-world` |
| `--cool--project--` | `cool-project` |

## Generated Project Stack

The scaffolded project includes:

- **React 19** with TypeScript
- **Rspack** for bundling and dev server
- **Custom Designer API hooks** for interacting with the Webflow Designer
- **Configurable linting** via Oxlint/Oxfmt, Biome, or ESLint/Prettier/Stylelint (set up by [ultracite](https://github.com/Flash-Brew-Digital/ultracite))
- **VS Code** editor configuration
- Pre-configured `package.json` with author info pulled from your git config

## Development Workflow

After scaffolding, start developing:

```bash
cd <project-name>
pnpm dev
```

Then in Webflow:

1. Open your Webflow workspace settings
2. Navigate to **Apps & Integrations** > **Develop**
3. Click **Create an App** and configure it accordingly
4. Open a project in the Designer
5. Press **E** to open the apps panel and launch your extension

Changes hot-reload automatically while the dev server is running.
