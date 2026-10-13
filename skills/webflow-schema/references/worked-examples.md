---
name: "Worked Examples"
description: "Complete @graph patterns for a blog post (BreadcrumbList, Article, FAQPage, ItemList), a case study, and a blog or work index page, with the decisions behind each binding."
tags: [examples, graph, article, blogposting, faqpage, itemlist, breadcrumblist, collectionpage, blog, case-study, creativework, ispartof, hub]
---

# Worked Examples

## Table of Contents

- [Blog post](#blog-post)
- [Case study](#case-study)
- [Blog or work index page](#blog-or-work-index-page)
- [Best Practices](#best-practices)

---

All examples use `https://www.example.com` as the canonical host and example field slugs. **Read the real slugs for the site you are working on.** They vary per site and per collection.

## Blog post

Four nodes: `BreadcrumbList`, `Article`, `FAQPage`, `ItemList`. Only the first FAQ and first takeaway are shown. Repeat the pattern for each slot.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.example.com" },
        { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://www.example.com/blog" },
        { "@type": "ListItem", "position": 3,
          "name": "{{wf {&quot;path&quot;:&quot;seo-title&quot;,&quot;type&quot;:&quot;PlainText&quot;} }}",
          "item": "https://www.example.com/blog/{{wf {&quot;path&quot;:&quot;slug&quot;,&quot;type&quot;:&quot;PlainText&quot;} }}" }
      ]
    },
    {
      "@type": "Article",
      "headline": "{{wf {&quot;path&quot;:&quot;seo-title&quot;,&quot;type&quot;:&quot;PlainText&quot;} }}",
      "description": "{{wf {&quot;path&quot;:&quot;seo-description&quot;,&quot;type&quot;:&quot;PlainText&quot;} }}",
      "url": "https://www.example.com/blog/{{wf {&quot;path&quot;:&quot;slug&quot;,&quot;type&quot;:&quot;PlainText&quot;} }}",
      "image": "{{wf {&quot;path&quot;:&quot;main-image&quot;,&quot;type&quot;:&quot;ImageRef&quot;} }}",
      "datePublished": "{{wf {&quot;path&quot;:&quot;date-published&quot;,&quot;type&quot;:&quot;Date&quot;} }}",
      "dateModified": "{{wf {&quot;path&quot;:&quot;last-updated&quot;,&quot;type&quot;:&quot;Date&quot;} }}",
      "timeRequired": "{{wf {&quot;path&quot;:&quot;read-time&quot;,&quot;type&quot;:&quot;PlainText&quot;} }}",
      "inLanguage": "en",
      "isPartOf": { "@type": "Blog", "name": "Example Co Blog", "url": "https://www.example.com/blog" },
      "author": { "@type": "Person",
        "name": "{{wf {&quot;path&quot;:&quot;author:name&quot;,&quot;type&quot;:&quot;PlainText&quot;} }}" },
      "publisher": { "@type": "Organization", "name": "Example Co", "url": "https://www.example.com" },
      "mainEntityOfPage": { "@type": "WebPage",
        "@id": "https://www.example.com/blog/{{wf {&quot;path&quot;:&quot;slug&quot;,&quot;type&quot;:&quot;PlainText&quot;} }}" }
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        { "@type": "Question",
          "name": "{{wf {&quot;path&quot;:&quot;faq-question-1&quot;,&quot;type&quot;:&quot;PlainText&quot;} }}",
          "acceptedAnswer": { "@type": "Answer",
            "text": "{{wf {&quot;path&quot;:&quot;faq-answer-1&quot;,&quot;type&quot;:&quot;PlainText&quot;} }}" } }
      ]
    },
    {
      "@type": "ItemList",
      "name": "Key Takeaways",
      "itemListElement": [
        { "@type": "ListItem", "position": 1,
          "name": "{{wf {&quot;path&quot;:&quot;takeaway-1&quot;,&quot;type&quot;:&quot;PlainText&quot;} }}" }
      ]
    }
  ]
}
```

Decisions worth understanding rather than copying:

- **`headline` binds to the SEO title field, not the item Name.** The Name feeds the H1, which should keep natural punctuation. A separate title field can be written schema-safe. If the collection has no separate title field, add one before binding.
- **`datePublished` binds to a real date field the editor controls**, never to `published-on`. See [auto-generate-pitfalls.md](auto-generate-pitfalls.md).
- **`timeRequired` must be an ISO 8601 duration** such as `PT10M`, not "10 min". The field holds an ISO string, so this is an editorial rule for whoever fills the CMS.
- **`inLanguage`** should be the site's real language tag, for example `en-AU` or `en-US`.

## Case study

Two nodes: `BreadcrumbList` and `Article` (or `CreativeWork`).

**Do not use `Service` for past project work.** `Service` describes something you sell, not work you delivered, and Google produces no rich results from it. If the case study needs to point at the client's live site, use an `about` node:

```json
"about": {
  "@type": "CreativeWork",
  "name": "{{wf {&quot;path&quot;:&quot;name&quot;,&quot;type&quot;:&quot;PlainText&quot;} }}",
  "url": "{{wf {&quot;path&quot;:&quot;project-url&quot;,&quot;type&quot;:&quot;Link&quot;} }}"
}
```

For case studies the `author` and `publisher` are both the business (`Organization`), and `isPartOf` points at the work index page as a `CollectionPage`.

## Blog or work index page

An index page is a hub. Its items already declare `isPartOf` pointing at it, so the hub has to claim the same identity or the two never join up.

Two nodes: `BreadcrumbList` and the hub itself.

```json
{
  "@type": ["CollectionPage", "Blog"],
  "@id": "https://www.example.com/blog",
  "url": "https://www.example.com/blog",
  "name": "Example Co Blog",
  "alternateName": "Blog",
  "publisher": { "@type": "Organization", "name": "Example Co", "url": "https://www.example.com" }
}
```

- **Multi-type the hub** as `["CollectionPage", "Blog"]`. It is both, and multi-typing is valid.
- **Give it an `@id`** equal to its URL, and make its `name` match the exact string the items use in `isPartOf`. Keep the short label as `alternateName`.
- **Do not hard-code a list of child items.** A static `hasPart` array on a page whose contents change goes stale. The children already point up.

Verify the join after publishing: fetch one item and the hub, and check the item's `isPartOf` name and URL match the hub's `name` and `@id` exactly.

## Best Practices

1. **Bind dates to real Date fields** the editor controls.
2. **Keep `isPartOf` names identical** across items and the hub.
3. **Use `Article` or `CreativeWork` for past work**, never `Service`.
4. **Use the site's real language tag** in `inLanguage`.
5. **Check several items per collection** after publishing, including ones with empty optional fields.
