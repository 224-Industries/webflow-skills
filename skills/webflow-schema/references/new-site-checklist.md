---
name: "New Site Checklist"
description: "The seven things to capture before doing schema work on a Webflow site you have not worked on, since field slugs and setup differ per site and per collection."
tags: [onboarding, checklist, site_id, canonical-host, collections, field-slugs, plaintext, richtext, worker, existing-schema]
---

# New Site Checklist

## Table of Contents

- [Capture before you start](#capture-before-you-start)
- [Best Practices](#best-practices)

---

## Capture before you start

Field slugs vary per site and per collection within a site, so nothing can be assumed from previous work.

1. **Webflow `site_id`.**
2. **Canonical host:** the custom domain actually attached, including the `www` or non-www decision. Every absolute URL in schema uses it.
3. **Which collections map to which schema type**, for example Blog → `Article`, Work → `Article` or `CreativeWork`, Services → `Service`, Team → `Person`.
4. **Field slugs per collection.** Read them, do not guess. Note which are PlainText and which are RichText, because that decides what can be bound.
5. **Whether FAQ or takeaway content is rendered on the page or schema-only.** This picks Architecture A or B.
6. **Whether a Cloudflare Worker fronts the site.** If one does, Architecture C is available.
7. **What schema already exists:** template level, per-post embeds and anything auto-generated. Record it before changing anything.

Save the answers wherever the site's project notes live, so the next session does not have to work them out again.

## Best Practices

1. **Read the collection schema** for slugs and field types before writing a single binding.
2. **Record existing schema first**, so any change can be compared or rolled back.
3. **Confirm the canonical host from the live site**, not from memory or an old document.
