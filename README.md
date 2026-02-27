# 224 Industries - Webflow Agent Skills

![224 Industries OSS](https://img.shields.io/badge/224_Industries-OSS-111212?style=for-the-badge&labelColor=6AFFDC)
![MIT License](https://img.shields.io/badge/License-MIT-111212?style=for-the-badge&labelColor=6AFFDC)
[![Webflow Premium Partner](https://img.shields.io/badge/Premium_Partner-146EF5?style=for-the-badge&logo=webflow&logoColor=white)](https://webflow.com/@224-industries)

This repository contains a collection of Webflow Agent Skills by 224 Industries. These skills are designed to enhance the capabilities of agents by providing them with specialized functionalities.

<img width="1200" height="630" alt="224-industries-webflow-agent-skills-vercel-skills-cli" alt="Vercel Skills CLI output from installing the Webflow Agent Skills by 224 Industries" src="https://github.com/user-attachments/assets/896d2eed-1f2c-4a46-9bae-0f0899f7cb52" />

## What are Agent Skills?

Agent Skills are folders of instructions, scripts, and resources that agents can discover and use to do things more accurately and efficiently. They work across any AI agent that supports the [open Agent Skills standard](https://agentskills.io).

## Available Skills
<!-- START:Available-Skills -->
| Skill | Description | Download |
| ----- | ----------- | -------- |
| [webflow-browser-api](./skills/webflow-browser-api) | Control Webflow Analyze and Optimize from JavaScript via the Browser API. Use... | [Download](https://skills.224ai.au/webflow-browser-api.skill) |
| [webflow-code-components](./skills/webflow-code-components) | Build, define, and import React code components into Webflow via DevLink. Use... | [Download](https://skills.224ai.au/webflow-code-components.skill) |
| [webflow-designer-api](./skills/webflow-designer-api) | Work with the Webflow Designer API — either by building Designer Extensions (... | [Download](https://skills.224ai.au/webflow-designer-api.skill) |
| [webflow-enterprise-api](./skills/webflow-enterprise-api) | Webflow Enterprise API endpoints for workspace management, audit logs, site a... | [Download](https://skills.224ai.au/webflow-enterprise-api.skill) |
| [webflow-webhooks](./skills/webflow-webhooks) | Receive and verify Webflow webhooks. Use when setting up Webflow webhook hand... | [Download](https://skills.224ai.au/webflow-webhooks.skill) |
<!-- END:Available-Skills -->

### Webflow Skills Kit

Looking for more? The [Webflow Skills Kit](https://flashbrew.digital/webflow-skills-kit) is a bundle of premium Agent Skills for Webflow professionals, including strategy report generation, discovery workflows, client roleplay, and more. Built for and by Webflow professionals, the Skills Kit is designed to help you get the most out of AI agents in your Webflow projects, while saving you money and time.

## Installation

### Skills

Use [skills](https://skills.sh/) to install skills directly:

```bash

███████╗██╗  ██╗██╗██╗     ██╗     ███████╗
██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝
███████╗█████╔╝ ██║██║     ██║     ███████╗
╚════██║██╔═██╗ ██║██║     ██║     ╚════██║
███████║██║  ██╗██║███████╗███████╗███████║
╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝

# Install all skills
npx skills add 224-industries/webflow-skills

# Install specific skills
npx skills add 224-industries/webflow-skills --skill webflow-designer-api

# List available skills
npx skills add 224-industries/webflow-skills --list
```

### Claude Code Plugin

Install via Claude Code's plugin system:

```bash
# Add the plugin (includes all skills)
/plugin add 224-industries/webflow-skills
```

> Claude Code plugins are also supported in Factory's [Droid](https://docs.factory.ai/cli/configuration/plugins#claude-code-compatibility).

### Other Installation Methods

Agent skills can also be installed by using the below commands from [Playbooks](https://playbooks.com/skills) or [Context7](https://context7.com/docs/skills):

```bash
# Playbooks
npx playbooks add skill 224-industries/webflow-skills

# Context7
npx ctx7 skills install /224-industries/webflow-skills
```

## Adding New Skills

Use the included script to add new skills:

```bash
node scripts/add-skill.js <skill-name> "<description>"
```

Example:

```bash
node scripts/add-skill.js webflow-designer-api "Build Webflow Designer Extensions..."
```

This will create the skill structure and automatically update manifest.json, platform plugin files, skills/index.json, and this README.

## Scripts

| Script | Description |
| ------ | ----------- |
| `node scripts/add-skill.js` | Add a new skill to the repository |
| `node scripts/sync-skills.js` | Sync manifest.json, platform plugin files, skills/index.json, and README with skills directory |

## Resources

- [Agent Skills Specification](https://agentskills.io/specification)
- [npx skills](https://skills.sh/)
- [Validate Agent Skill](https://github.com/marketplace/actions/validate-skill)
- [Playbooks](https://playbooks.com/skills)
- [Context7 Skills](https://context7.com/docs/skills)

## Contributing

Contributions are welcome! Please read our [Contributing Guide](.github/CONTRIBUTING.md) for more information.

## License

[MIT License](LICENSE)

## Creator

[Ben Sabic](https://bensabic.dev) (Fractional CTO) at [224 Industries](https://224industries.com.au)
