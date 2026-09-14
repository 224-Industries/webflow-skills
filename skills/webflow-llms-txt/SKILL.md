---
name: webflow-llms-txt
description: Generate, audit and maintain an llms.txt file for a Webflow site. Use when creating an llms.txt for the first time, refreshing a stale one, checking which pages are missing from it, writing the descriptions inside it, or diffing this month's file against last month's. Works with or without a Webflow API token.
license: MIT
metadata:
  author: "Ben Sabic"
  repository: "https://github.com/224-industries/webflow-skills"
  url: "https://github.com/224-Industries/webflow-skills/releases/latest/download/webflow-llms-txt.skill"
  version: "1.0.0"
  keywords: "ai, agent, skill, webflow, llms-txt, aeo, geo, seo, structured content, site audit, crawlers, ai search, content inventory, sitemap"
---

# Webflow llms.txt

`llms.txt` is a plain-text map of a site that AI crawlers read to work out what lives where. Webflow serves it from a file you upload in Site settings, which means it does not update itself: new blog posts ship, pages get renamed, slugs change, and the file silently keeps describing last quarter's site.

This skill reads a Webflow site as it actually is today and produces a fresh `llms.txt`, plus a changelog of what moved since the last run.

## What this produces

| Output | Purpose |
|--------|---------|
| `llms.txt` | The file a human uploads to Webflow. Overwrite it each run so the next run has something to diff against. |
| `descriptions.md` | Curated description overrides, keyed by URL. Persistent, updated in place, never dated. |
| `YYYY-MM-DD-changelog.md` | What changed since the last run. Written to be read by a site owner, not a developer. |

## Hard rules

These are the reason this skill is safe to run unattended. Hold them firmly.

1. **Read-only.** Never publish a site, never write to the CMS, never change page settings. If a run seems to need a write, stop and say so. There is no path from this skill to a live site.
2. **Never invent a fact.** Every claim in a description must be evidenced on the page being described. If a page has no readable content and no usable description, leave it out of the file and list it in the changelog. A fabricated description is worse than an absent one, because it gets crawled and believed.
3. **Never reuse a meta description verbatim.** This is the single biggest quality problem in generated llms.txt files, and Webflow explicitly warns against it. See [references/writing-descriptions.md](references/writing-descriptions.md).
4. **A human uploads the file.** There is no API for it. Every run ends by naming the path: **Site settings > SEO > LLMs.txt > Upload file**.

## Before you start

Establish four things, in this order:

1. **The canonical host.** Not the `.webflow.io` staging domain, which never serves this file. If both `www` and non-`www` resolve, HEAD-check both and use whichever does *not* redirect.
2. **Which inventory path is available.** With a Webflow API token or the Webflow MCP, use the Data API for an accurate inventory including draft and archived state. Without one, fall back to `sitemap.xml`. See [references/data-api-inventory.md](references/data-api-inventory.md) and [references/sitemap-fallback.md](references/sitemap-fallback.md).
3. **A source for the overview block.** Ask for the site owner's brand, positioning or messaging document. Do not substitute the homepage hero. See [references/overview-block.md](references/overview-block.md).
4. **Whether a previous `llms.txt` exists.** If not, this is a first run: say so plainly and write a baseline summary rather than manufacturing a diff against nothing.

## Workflow

### 1. Read the site

Build an inventory of every public page and CMS item. Two paths, same output shape.

**With API access** (preferred, more accurate): list pages, list collections, list items in each collection that represents real pages. Read [references/data-api-inventory.md](references/data-api-inventory.md) first — it documents a context-window trap that will kill the run if you batch collection requests, and a set of field behaviours that differ from what you would reasonably assume.

**Without API access**: fetch `sitemap.xml` and read each page. Read [references/sitemap-fallback.md](references/sitemap-fallback.md) — draft and archived state are invisible on this path, so the exclusion logic changes.

### 2. Decide what is in and what is out

Exclude system pages (`404`, the password page), drafts, archived items, CMS *template* pages as distinct from the items they render, and anything with no usable description and no readable content. Full exclusion logic for each path is in the two inventory references.

### 3. Write the overview block

The free-text block between the `>` summary line and the first `##` section. Most generated files skip it. It is the highest-value part of the file, because it is the only place a model gets the business in its own words rather than inferring it from a list of page titles. Always write one. See [references/overview-block.md](references/overview-block.md).

### 4. Write the descriptions

Resolution order for each URL:

1. The curated line in `descriptions.md` for that exact URL.
2. Failing that, the page or item meta description, as a stopgap only.
3. Flag every URL that fell through to (2) in the changelog, so the file converges over time.

Rules for writing a good one, and the per-page-type patterns, are in [references/writing-descriptions.md](references/writing-descriptions.md).

### 5. Assemble and validate

Emit in the exact format in [references/file-format.md](references/file-format.md). Then run both checks:

```bash
python scripts/validate_llms_txt.py llms.txt
python scripts/check_urls.py llms.txt
```

The validator enforces UTF-8, the 100 KB ceiling, and character hygiene. The URL checker HEAD-checks every link. Anything that is not a `200` goes in the changelog: follow a `301` and emit its destination instead, drop a `404`. Never ship a URL you know is broken.

### 6. Diff against the previous file

```bash
python scripts/diff_llms_txt.py previous-llms.txt llms.txt
```

Re-pair slug changes before reporting: a changed slug surfaces as one addition plus one removal, and reporting it that way is misleading. See [references/monthly-audit.md](references/monthly-audit.md).

### 7. Hand off

Close every run with the path to the generated file, the upload path verbatim (**Site settings > SEO > LLMs.txt > Upload file**), a reminder that the file will not appear on the `.webflow.io` staging domain, and anything needing a human decision. Never offer to publish it.

## Reference documentation

Each reference file includes YAML frontmatter with `name`, `description`, and `tags` for searchability. Use the search script in `scripts/search_references.py` to find relevant references.

### Platform

- **[references/webflow-constraints.md](references/webflow-constraints.md)**: What Webflow itself specifies — upload location, size and encoding limits, staging domain behaviour, why `.md` variants are not supported, and Webflow's own content guidance

### Reading the site

- **[references/data-api-inventory.md](references/data-api-inventory.md)**: Building an inventory via the Webflow Data API — endpoints, the rich-text context trap, and field behaviours that differ from expectation
- **[references/sitemap-fallback.md](references/sitemap-fallback.md)**: Building an inventory with no API token, from `sitemap.xml` and live page fetches

### Writing the file

- **[references/overview-block.md](references/overview-block.md)**: The free-text block — what it covers, where to source it, and why the homepage hero is the wrong input
- **[references/writing-descriptions.md](references/writing-descriptions.md)**: Why meta descriptions fail as llms.txt descriptions, per-page-type patterns, and the `descriptions.md` overrides file
- **[references/file-format.md](references/file-format.md)**: The exact output format, section ordering, and the spec's `## Optional` convention

### Maintaining it

- **[references/monthly-audit.md](references/monthly-audit.md)**: Re-running against a previous file — what to diff, how to re-pair slug changes, and the changelog format

### Searching references

```bash
# List all references with metadata
python scripts/search_references.py --list

# Search by tag (exact match)
python scripts/search_references.py --tag <tag>

# Search by keyword (across name, description, tags, and content)
python scripts/search_references.py --search <query>
```

## Scripts

- **`scripts/validate_llms_txt.py`**: Check encoding, byte size, character hygiene and structural validity
- **`scripts/check_urls.py`**: HEAD-check every URL in the file and report non-200 responses
- **`scripts/diff_llms_txt.py`**: Parse two `llms.txt` files and report additions, removals, and title, description and URL changes
- **`scripts/search_references.py`**: Search reference files by tag, keyword, or list all with metadata
