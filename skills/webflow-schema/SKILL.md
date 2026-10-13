---
name: webflow-schema
description: Build, fix and audit JSON-LD structured data on Webflow sites. Use when adding schema to a Collection template, binding schema to CMS fields, checking why rich results or FAQ snippets are not showing, cleaning up Webflow's auto-generated schema, fixing wrong published dates in Search Console, or auditing the live JSON-LD on any Webflow page.
license: MIT
metadata:
  author: "Kirk Land"
  repository: "https://github.com/224-industries/webflow-skills"
  url: "https://github.com/224-Industries/webflow-skills/releases/latest/download/webflow-schema.skill"
  version: "1.0.0"
  keywords: "ai, agent, skill, webflow, schema, json-ld, structured data, rich results, faq schema, article schema, breadcrumb, itemlist, cms binding, seo, aeo, search console"
---

# Webflow Schema (JSON-LD)

Build and audit structured data on Webflow sites.

Webflow's page-level **JSON-LD field** (Page Settings, also writable through the Data API) is the right home for schema on a Webflow site. It lands in the served HTML, which matters because most AI crawlers do not run JavaScript. The field has two platform limits that were found by testing against live sites, and nearly every decision in this skill follows from them. Read [references/platform-limits.md](references/platform-limits.md) before you write anything.

## Hard rules

These keep schema work safe on a live site. Hold them on every task.

- **Leave publishing to a person.** Stage changes unpublished and say clearly that they are waiting for a publish. Only publish when the site owner tells you to in the conversation.
- **Do not edit body content.** Schema work should never touch a post's main rich text field. Ask first if a task seems to need it.
- **Never invent a fact, date, author, rating or claim** to fill a schema property. Bind it to a real field or leave the property out. Made-up structured data risks a manual action and is worse than none.
- **Never trust a binding until you have seen it resolve on the live page.** After a publish, fetch the URL and read the rendered JSON-LD.

## Quick start workflow

1. **Orient.** Get the Webflow `site_id`, confirm the canonical host (the custom domain actually attached, and whether `www` redirects), list pages and find the Collection templates. Read the schema already on the template and on one live page.
2. **Pick the architecture.** Is the content you want in schema rendered on the page, or does it exist only to feed schema? See the table below.
3. **Check the content.** Bound CMS values must be PlainText (or Number, Date, ImageRef, Link) and free of straight apostrophes, straight double quotes and ampersands. Run [scripts/check_bindable_text.py](scripts/check_bindable_text.py) over the field values.
4. **Write one `@graph`.** One script block, one `@context`, every node inside `@graph`, every URL absolute on the canonical host.
5. **Write it through the API** with the binding token written without the backslash. See [references/writing-via-api.md](references/writing-via-api.md).
6. **Hand off for publishing**, then **audit the live page** with [scripts/audit_jsonld.py](scripts/audit_jsonld.py) across several items, not just one.

## Choosing the architecture

| Situation | Architecture | Server-rendered | Rich text | Notes |
|---|---|---|---|---|
| Content exists only to feed schema (FAQ or takeaway fields that never display) | **A. Bind CMS fields in the JSON-LD field** | Yes | No | The default. Use whenever you can. |
| Content is rendered on the page (FAQ accordions, visible takeaways) | **B. Client-side script reads the DOM** | No | Yes | Google renders it. Most AI crawlers will not see it. |
| A Cloudflare Worker already fronts the site | **C. Edge injection with HTMLRewriter** | Yes | Yes | Best of both, only where a Worker already exists. |

Full detail, including the attribute contracts for the scripts, is in [references/architectures.md](references/architectures.md).

## The two limits, in brief

1. **Webflow HTML-escapes every CMS value bound into the JSON-LD field.** A straight apostrophe renders as `&#39;`, a double quote as `&quot;`, an ampersand as `&amp;`, and crawlers read those codes as literal text. Typographic punctuation is the fix: a smart apostrophe (`’`) passes through unescaped. Spell `&` as "and".
2. **RichText fields bound into the JSON-LD field come back as an empty string.** Not stripped, empty. Rich text can never be template-bound.

Literal text typed into a static page's JSON-LD field is not escaped. The limits apply to `{{wf ...}}` bindings.

## Reference documentation

### Platform

- [Platform limits](references/platform-limits.md): the escaping and RichText limits, which field types bind, and what is safe to write
- [Choosing an architecture](references/architectures.md): bind, client-side script or edge injection, with the ready-made scripts

### Building

- [Writing schema via the API](references/writing-via-api.md): read and write calls, the binding token gotcha, token rules and variable item counts
- [Worked examples](references/worked-examples.md): a blog post `@graph`, a case study and a blog or work index page
- [What auto-generate gets wrong](references/auto-generate-pitfalls.md): the problems in Webflow's generated schema and how to fix each one

### Checking

- [Auditing live schema](references/auditing.md): what to report, how to read Search Console verdicts, and how to finish a piece of work
- [New site checklist](references/new-site-checklist.md): what to capture before any schema work on a site you have not worked on

### Searching references

```bash
# List all references with metadata
python scripts/search_references.py --list

# Search by tag (exact match)
python scripts/search_references.py --tag binding

# Search by keyword (across name, description, tags, and content)
python scripts/search_references.py --search "search console"
```

## Scripts

- `scripts/audit_jsonld.py`: fetch one or more live URLs and report parse failures, unresolved tokens, HTML entities, empty values, relative URLs, non-ISO dates, self-serving reviews and duplicate types
- `scripts/check_bindable_text.py`: check text (a CSV export, a file or stdin) for characters that will break once bound into the JSON-LD field
- `scripts/search_references.py`: search the reference files by tag or keyword

## Assets

- `assets/faq-schema.html`: FAQPage builder for Architecture B, driven by `data-faq-item`, `data-faq-question` and `data-faq-answer` attributes
- `assets/takeaways-schema.html`: ItemList builder for Architecture B, driven by `data-takeaway` on each item

## License

MIT
