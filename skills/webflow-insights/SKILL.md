---
name: webflow-insights
description: Answer questions about how a Webflow site is performing from Webflow's own data, through the Webflow MCP server. Covers Analyze (traffic, pages, sources, goals, engagement), Optimize (A/B test, AI-optimised and personalisation results) and AEO Analytics (AI crawler traffic, tracked prompts, AI visibility and citations). Use for "how's the site going", "which pages get the most traffic", "has my test got a winner", "which pages are AI crawlers reading", a monthly check-up, or working out why traffic changed. Works with whichever of the three products the site has. Read-only.
license: MIT
metadata:
  author: "Kirk Land"
  repository: "https://github.com/224-industries/webflow-skills"
  url: "https://github.com/224-Industries/webflow-skills/releases/latest/download/webflow-insights.skill"
  version: "1.0.0"
  keywords: "ai, agent, skill, webflow, analytics, webflow analyze, webflow optimize, aeo, ai search, ab testing, experiments, traffic, conversions, goals, llm crawlers, ai visibility, citations, mcp"
---

# Webflow Insights

Webflow's MCP server reads three of its products: **Analyze**, **Optimize** and **AEO Analytics**. Not every site has all three. Many have Analyze only, some have none, and AEO Analytics is mostly found on enterprise plans.

This skill checks which products a site has, runs the right reads, interprets the results honestly and answers in plain language. A product the site doesn't have is treated as a normal state, never as an error.

## Hard rules

1. **Read-only.** Use only `data_sites_tool` (`list_sites`, `get_site`), the read actions of `data_pages_tool` and `data_cms_tool`, `data_analyze_tool`, `data_optimize_tool` and `data_aeo_tool`. Never publish, edit, create or delete anything.
2. **A missing product is not an error.** Never show a status code, an error name or raw JSON, and never describe a product as blocked, forbidden, failed or denied. Use the wording in [references/availability.md](references/availability.md).
3. **Never invent a number.** Report only fields that came back. Label any figure you calculated, such as a conversion rate or a percentage change, and say what it's calculated from.
4. **A crawler visit is not a citation.** Webflow says so too. Citations and mentions come only from the prompt-tracking reports.
5. **Don't call a test early.** No winner below 0.95 significance on an A/B test, and none at all for personalisation.
6. **Always state the date window** you used, in the site's local dates.

## Before you start

1. **Find the site.** `data_sites_tool > list_sites`. If there are several and the person hasn't said which, ask. Then call `get_site` for the site's `timeZone`.
2. **Check what's available.** Run the light probes in [references/availability.md](references/availability.md) for the products the question needs. A check-up probes all three. Record each as available, not on the plan, not set up, or no access, and reuse the result for the rest of the conversation.
3. **Resolve the date window** in the site's time zone. See [references/analyze.md](references/analyze.md) > Date windows.

## Three ways in

| Request | What to do |
|---|---|
| **A question** ("which pages get the most traffic?") | Run the fewest reads that answer it, using the reference for that product |
| **A monthly check-up** | Last complete month against the one before, across every available product. Layout in [references/reports.md](references/reports.md) |
| **Diagnosing a change** ("why did traffic drop?") | Confirm the change, find where it happened, check what changed on the site, then conclude with a confidence level. Steps in [references/reports.md](references/reports.md) |

## Answer format

1. **The answer**, in one or two sentences, first.
2. **The numbers behind it**, with the date window.
3. **What to do next**, up to three points, each tied to a number.
4. **What the data can't tell you**, when it matters to the question.
5. **One availability line**, only when a missing product is relevant.

Use plain words ("visits", not "sessions"), give counts alongside percentages, and leave out ids, field names and raw JSON.

## Reference Documentation

| File | Read when |
|---|---|
| [references/availability.md](references/availability.md) | Every run, before the first real query. Detecting each product and the exact wording for anything missing |
| [references/analyze.md](references/analyze.md) | Traffic, pages, sources, goals, engagement, scroll depth or page flow |
| [references/optimize.md](references/optimize.md) | Tests, experiments, variations or personalisation |
| [references/aeo.md](references/aeo.md) | AI crawlers, AI search, tracked prompts, visibility or citations |
| [references/reports.md](references/reports.md) | A check-up, a diagnosis, or a question that spans products. Also holds the answer layout |

## Requirements

- The [Webflow MCP server](https://developers.webflow.com/mcp/reference/overview) connected to your AI agent, authorised for the site's workspace.
- Access in Webflow to whichever of Analyze, Optimize and AEO Analytics the site has. The agent can only see what the person using it can see.

## License

MIT
