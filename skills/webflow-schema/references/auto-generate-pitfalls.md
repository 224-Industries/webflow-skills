---
name: "What Auto-Generate Gets Wrong"
description: "Problems observed in Webflow's built-in schema generation (relative URLs, wrong publisher domain, self-serving reviews, published-on dates, non-ISO dates, mis-mapped fields, replaced breadcrumbs) and the fix for each."
tags: [auto-generate, generated-schema, relative-urls, published-on, datepublished, review, aggregaterating, iso-8601, breadcrumblist, audit]
---

# What Auto-Generate Gets Wrong

## Table of Contents

- [Observed problems](#observed-problems)
- [Default position](#default-position)
- [Best Practices](#best-practices)

---

## Observed problems

Webflow's "generate schema" feature is a starting point at best. Every problem below was seen on a real site.

| Problem | Why it matters | Fix |
|---|---|---|
| **Relative URLs** (`/work/slug`) | Schema needs absolute URLs. Relative ones are ignored or misread. | Write the canonical host in front of every bound slug. |
| **Wrong publisher domain** | It pulled a domain that was not the site's live custom domain. | Confirm the real canonical host and write it literally. |
| **A self-serving `review` block** | Google excludes reviews about the entity hosting them. Ineligible for rich results, and it looks like manipulation. | Remove it. Do not replace it. |
| **`datePublished` bound to `published-on`** | `published-on` resets on every **site** publish, so every item claims it was published today. This wipes out freshness signals across the collection. | Bind `created-on`, or better, a real Date field the editor controls. |
| **Free-text dates** such as `Mar 10, 2026` or `20260709T120000+1000` | Not ISO 8601, so parsers drop them. | Bind a real Date field with `"type":"Date"`. Never a PlainText date. |
| **Fields mapped to the wrong source**, such as a hover-text field used as `description` | Nonsense descriptions in search and AI answers. | Read the collection schema and map each property on purpose. |
| **It replaces existing BreadcrumbList markup** instead of adding to it | Silently destroys working schema. | Never run auto-generate on a template that already has hand-written schema. Read first. |

## Default position

Hand-write the `@graph`. If auto-generate has already been run, treat its output as a draft to check line by line, not a base to extend.

## Best Practices

1. **Read the template's JSON-LD field before running anything** that could overwrite it.
2. **Search the generated output for `review` and `aggregateRating`** and remove any about the site's own business.
3. **Check every date property** binds to a Date field.
4. **Check every URL property** is absolute on the canonical host.
