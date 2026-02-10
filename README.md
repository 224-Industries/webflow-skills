# 224 Industries - Webflow Agent Skills

![224 Industries OSS](https://img.shields.io/badge/224_Industries-OSS-111212?style=for-the-badge&labelColor=6AFFDC)
![MIT License](https://img.shields.io/badge/License-MIT-111212?style=for-the-badge&labelColor=6AFFDC)
[![Webflow Premium Partner](https://img.shields.io/badge/Premium_Partner-146EF5?style=for-the-badge&logo=webflow&logoColor=white)](https://webflow.com/@224-industries)

This repository contains a collection of Webflow Agent Skills by 224 Industries. These skills are designed to enhance the capabilities of agents by providing them with specialized functionalities.

## What are Agent Skills?

Agent Skills are folders of instructions, scripts, and resources that agents can discover and use to do things more accurately and efficiently. They work across any AI agent that supports the [open Agent Skills standard](https://agentskills.io).

## Available Skills
<!-- START:Available-Skills -->
| Skill | Description |
| ----- | ----------- |
| [webflow-designer-extension](./skills/webflow-designer-extension) | Build Webflow Designer Extensions that run inside the Webflow Designer. Use w... |
<!-- END:Available-Skills -->

## Installation

### Option 1: Skills (Recommended)

Use the [Vercel Skills CLI](https://skills.sh/) to install skills directly:

```bash
# Install all skills
npx skills add 224-industries/webflow-skills

# Install specific skills
npx skills add 224-industries/webflow-skills --skill webflow-designer-extension

# List available skills
npx skills add 224-industries/webflow-skills --list
```

### Option 2: Claude Code Plugin

Install via Claude Code's plugin system:

```bash
# Add the marketplace
/plugin marketplace add 224-industries/webflow-skills

# Install specific skill
/plugin install webflow-designer-extension-skill
```

## Adding New Skills

Use the included script to add new skills:

```bash
node scripts/add-skill.js <skill-name> "<description>"
```

Example:

```bash
node scripts/add-skill.js webflow-designer-extension "Build Webflow Designer Extensions that run inside the Webflow Designer. Use when creating, debugging, or modifying Designer Extensions (iframes that interact with Webflow's Designer API). Covers CLI usage, element manipulation, styles, components, pages, variables, assets, error handling, and UI design patterns for Webflow's design system."
```

This will create the skill structure and automatically update this README and the marketplace.json.

## Scripts

| Script | Description |
| ------ | ----------- |
| `node scripts/add-skill.js` | Add a new skill to the repository |
| `node scripts/sync-skills.js` | Sync README and marketplace.json with skills directory |

## Resources

- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Skills directory](https://skills.sh/)

## License

[MIT License](LICENSE)

## Creator

[Ben Sabic](https://bensabic.dev) (Fractional CTO) at [224 Industries](https://224industries.com.au)