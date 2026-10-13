---
name: "Choosing an Architecture"
description: "The three ways to ship JSON-LD on a Webflow site (bind CMS fields, a client-side DOM-reading script, or Cloudflare edge injection), when to use each, and the attribute contracts for the ready-made scripts."
tags: [architecture, binding, client-side, script, dom, faqpage, itemlist, cloudflare, worker, htmlrewriter, data-attributes, custom-code, aeo]
---

# Choosing an Architecture

## Table of Contents

- [Orient first](#orient-first)
- [A: bind schema-only CMS fields](#a-bind-schema-only-cms-fields)
- [B: client-side script reads the page](#b-client-side-script-reads-the-page)
- [C: edge injection with a Cloudflare Worker](#c-edge-injection-with-a-cloudflare-worker)
- [Best Practices](#best-practices)

---

## Orient first

Never start editing schema without knowing which architecture the site is on. Getting it wrong produces either empty schema or schema crawlers cannot see.

1. **Identify the site and the canonical host.** Get the `site_id`. Check which custom domain is attached and where `www` resolves. Every URL in schema must be absolute and use that host.
2. **List the pages** (`list_pages`) and identify the Collection templates. Template-bound schema lives on the template, not on individual items.
3. **Read what is already there**, both the template's JSON-LD field and a live rendered page.
4. **Decide whether the content you want in schema is rendered on the page.** This picks the architecture.
5. **Check whether a Cloudflare Worker fronts the site.** If one does, edge injection is available.

## A: bind schema-only CMS fields

The content exists only to feed schema. For example, FAQ and key takeaway fields on a Blog collection that never display on the page.

- Server-rendered, so AI crawlers see it. This is the main reason to prefer it.
- Needs PlainText fields and safe characters (see [platform-limits.md](platform-limits.md)).
- Needs an editorial standard for item counts, because the JSON-LD field has no conditional logic (see [writing-via-api.md](writing-via-api.md#variable-item-counts)).

**Use A whenever you can.** If the content is only there for schema, make the fields PlainText and bind them.

## B: client-side script reads the page

The content is rendered on the page as real rich text, for example an FAQ accordion. It cannot be bound, so a script reads the DOM and injects the JSON-LD.

Why it works where binding fails:

- `JSON.stringify` escapes correctly, so apostrophes and quotes survive.
- Rich text survives, because the script reads the rendered element.
- Variable item counts are handled for free. The script only emits what it finds.

> **The weakness, stated plainly:** the script injects on `DOMContentLoaded`. Google renders pages before indexing and picks it up. Most AI crawlers do not run JavaScript, so for answer engines this schema is effectively invisible. If AEO is the goal, treat B as a compromise.

### The FAQ script

File: `assets/faq-schema.html`. It builds one `FAQPage` from every FAQ item on the page.

| Element | Attribute |
|---|---|
| Each FAQ item wrapper | `data-faq-item="true"` |
| The question text inside it | `data-faq-question="true"` |
| The answer rich text inside it | `data-faq-answer="true"` |

- All three must be set or that item is skipped.
- The answer is read as `innerHTML`, so inline links survive. Google accepts limited HTML in `acceptedAnswer.text`.
- Several FAQ accordions on one page merge into a single `FAQPage`, which is correct.
- On a component-built accordion, set the attributes through component overrides rather than on the main component.

### The key takeaways script

File: `assets/takeaways-schema.html`. It builds one `ItemList` from every element marked as a takeaway.

| Element | Attribute |
|---|---|
| Each individual takeaway | `data-takeaway="true"` |

- Put the attribute on each item, never on a wrapper holding several.
- Text is read with `textContent`, so formatting is flattened, which is right for `ItemList`.
- `position` counts up in page order.
- The list name comes from `document.title` up to the first `|`. Adjust that line if the site's titles use a different separator.
- If nothing is marked, the script exits without injecting anything.

### Installing them

Both go in the page's before-`</body>` custom code, or a site-wide footer embed. Through the API, read the current block with `get_page_freeform_code` first, then write with `set_page_freeform_code`.

> **`set_page_freeform_code` replaces the entire block.** Always read first and keep whatever is already there.

If you use B for a type, do not also bind the same type in the template. You will ship two competing `FAQPage` blocks.

## C: edge injection with a Cloudflare Worker

Where a Worker already fronts the site, the same DOM-reading logic can run in `HTMLRewriter` at the edge. You get rich text and server-rendered output, with no client-side JavaScript.

This only applies where a Worker already exists, which most Webflow sites do not have. Recommend it where it is available. Do not propose adding a Worker just for schema.

## Best Practices

1. **Default to A.** Server-rendered schema is what AI crawlers can read.
2. **Use B only for content that is genuinely displayed** and cannot be duplicated into PlainText fields.
3. **Never run A and B for the same schema type** on one page.
4. **Read custom code before writing it**, because the write replaces the whole block.
5. **State the AEO trade-off** whenever you recommend B.
