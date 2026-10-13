---
name: "Writing Schema via the API"
description: "Reading and writing a page's JSON-LD field through the Webflow Data API, the backslash binding token gotcha that rejects the whole payload, token rules, and how to handle variable item counts."
tags: [api, query_pages_schema_markup, bulk_update_pages_schema_markup, binding, token, wf-token, graph, field-slugs, conditional-visibility, embeds, item-counts]
---

# Writing Schema via the API

## Table of Contents

- [Read and write calls](#read-and-write-calls)
- [The binding token gotcha](#the-binding-token-gotcha)
- [Token rules](#token-rules)
- [Variable item counts](#variable-item-counts)
- [Best Practices](#best-practices)

---

## Read and write calls

| Action | Call | Limit |
|---|---|---|
| Read a page's JSON-LD field | `query_pages_schema_markup` | Up to 100 pages per call |
| Write a page's JSON-LD field | `bulk_update_pages_schema_markup` | Up to 25 pages per call |

Collection templates are pages too. Write the template, not individual items.

## The binding token gotcha

Webflow's own UI writes binding tokens containing `\}`:

```text
{{wf {&quot;path&quot;:&quot;slug&quot;,&quot;type&quot;:&quot;PlainText&quot;\} }}
```

`\}` is not a valid JSON escape. If you copy that form into an API write, Webflow rejects the whole payload with:

> The provided schema markup must be valid JSON.

Write the token **without the backslash**. This form saves through the API and resolves on the live page:

```text
{{wf {&quot;path&quot;:&quot;field-slug&quot;,&quot;type&quot;:&quot;PlainText&quot;} }}
```

Keep the space before the closing `}}`.

If you read SEO title or description fields back from `list_pages`, you will see the `\}` form, because the UI wrote them. That is expected. Do not "fix" those.

## Token rules

- **Confirmed `type` values:** `PlainText`, `Number`, `Date`, `ImageRef`, `Link`.
- **Fields on a referenced item use a colon:** `author:name` reads the `name` field of the item the `author` reference points at.
- **Field slugs vary per site and per collection.** Never assume `main-image` or `post-body`. Read the collection schema and confirm each slug before binding.
- **Use a single `@graph` array**, not several sibling script blocks. One block, one `@context`, every node inside `@graph`. It is easier to audit and the nodes are treated as connected.
- **Write every URL absolute** on the canonical host, with the bound slug appended: `https://www.example.com/blog/{{wf ...slug... }}`.

## Variable item counts

The JSON-LD field has no conditional logic. Five bound FAQ slots always emit five `Question` entries, even when only three are filled, so you get two questions with empty names and answers.

There are two fixes:

### 1. Require every slot filled

Make it an editorial standard: every post fills all five FAQs and all five takeaways. Simple, no extra build. Put it on the content checklist rather than in the template.

### 2. Conditional visibility Embeds

Build the JSON-LD from several Embed elements in the Collection template, each with Conditional Visibility set to "FAQ Title 2 is set", and so on.

> **The trailing comma trap:** put the comma at the **start** of items two onward, never at the end. Item one then always closes cleanly however many later items are hidden.

Prefer option 1 unless the site owner cannot guarantee filled slots.

## Best Practices

1. **Read before you write.** Record what the field held before changing it.
2. **Strip the backslash** from any token copied out of the UI.
3. **Confirm slugs from the collection schema**, never from another site.
4. **One `@graph` per page.**
5. **Confirm the write succeeded.** A rejected write is usually the `\}` gotcha or a JSON syntax error.
