# Webflow Agent Skills

Open-source Agent Skills for Webflow, by 224 Industries. They give Claude and other AI agents the know-how to work on Webflow sites, from llms.txt and schema to the Designer API and webhooks.

Browse them at [224industries.com.au/webflow-skills](https://224industries.com.au/webflow-skills). Questions go to [support@224industries.com.au](mailto:support@224industries.com.au).

## Available skills

<!-- START:Available-Skills -->
| Skill | Description | Download |
| ----- | ----------- | -------- |
| [webflow-browser-api](./skills/webflow-browser-api) | Control Webflow Analyze and Optimize from JavaScript via the Browser API. Use... | [Download](https://github.com/224-Industries/webflow-skills/releases/latest/download/webflow-browser-api.skill) |
| [webflow-code-components](./skills/webflow-code-components) | Build, define, and import React code components into Webflow via DevLink. Use... | [Download](https://github.com/224-Industries/webflow-skills/releases/latest/download/webflow-code-components.skill) |
| [webflow-designer-api](./skills/webflow-designer-api) | Work with the Webflow Designer API — either by building Designer Extensions (... | [Download](https://github.com/224-Industries/webflow-skills/releases/latest/download/webflow-designer-api.skill) |
| [webflow-enterprise-api](./skills/webflow-enterprise-api) | Webflow Enterprise API endpoints for workspace management, audit logs, site a... | [Download](https://github.com/224-Industries/webflow-skills/releases/latest/download/webflow-enterprise-api.skill) |
| [webflow-insights](./skills/webflow-insights) | Answer questions about how a Webflow site is performing from Webflow's own da... | [Download](https://github.com/224-Industries/webflow-skills/releases/latest/download/webflow-insights.skill) |
| [webflow-llms-txt](./skills/webflow-llms-txt) | Generate, audit and maintain an llms.txt file for a Webflow site. Use when cr... | [Download](https://github.com/224-Industries/webflow-skills/releases/latest/download/webflow-llms-txt.skill) |
| [webflow-schema](./skills/webflow-schema) | Build, fix and audit JSON-LD structured data on Webflow sites. Use when addin... | [Download](https://github.com/224-Industries/webflow-skills/releases/latest/download/webflow-schema.skill) |
| [webflow-webhooks](./skills/webflow-webhooks) | Receive and verify Webflow webhooks. Use when setting up Webflow webhook hand... | [Download](https://github.com/224-Industries/webflow-skills/releases/latest/download/webflow-webhooks.skill) |
<!-- END:Available-Skills -->

## Install

```bash
npx skills add 224-industries/webflow-skills
```

Or download a `.skill` file from the table above and upload it in Claude under Customize > Skills.

In Claude Code:

```bash
/plugin add 224-industries/webflow-skills
```

## License

[MIT](LICENSE)
