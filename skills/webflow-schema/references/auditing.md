---
name: "Auditing Live Schema"
description: "How to audit the JSON-LD a Webflow page actually ships, what to report, how to read Search Console URL Inspection verdicts, and the steps to finish and verify a schema change."
tags: [audit, live-page, search-console, url-inspection, rich-results, invalid-object-type, review, duplicates, entities, unresolved-tokens, verification, publish_collection_items]
---

# Auditing Live Schema

## Table of Contents

- [Read the live page, not the template](#read-the-live-page-not-the-template)
- [What to report](#what-to-report)
- [Reading Search Console verdicts](#reading-search-console-verdicts)
- [Finishing a piece of work](#finishing-a-piece-of-work)
- [Best Practices](#best-practices)

---

## Read the live page, not the template

The template shows what was intended. The live page shows what shipped. Fetch the rendered HTML and parse every `application/ld+json` block:

```bash
python scripts/audit_jsonld.py https://www.example.com/blog/post-one https://www.example.com/blog/post-two
```

Run it across several items per collection, not one. A binding can look perfect on the item someone filled properly and fall apart on the one where slots four and five are empty.

## What to report

| Finding | Usual cause |
|---|---|
| **Parse failure** | The block is not valid JSON |
| **Unresolved `{{wf` tokens** | Wrong field slug, or a field type that cannot bind |
| **HTML entities** (`&#39;`, `&quot;`, `&amp;`) | Limit 1. Report the exact string so the copy can be fixed |
| **Empty required values** | Limit 2 (a RichText field was bound), or an empty CMS slot |
| **Relative URLs** in `url`, `item`, `@id` or `image` | Missing canonical host |
| **Non-ISO dates** in `datePublished` or `dateModified`, or a non-ISO `timeRequired` | A PlainText date, or an editorial slip |
| **Self-serving reviews** (`review` or `aggregateRating` about the site's own business) | Usually auto-generate |
| **Duplicate blocks** of the same `@type` | A template binding plus a hand-embedded block in the post body |
| **Host mismatch** (`www` against non-www, or an old domain) | Copied from another site or an old setup |
| **Orphaned hubs** | An item's `isPartOf` names a hub that no page declares itself to be |

A different type embedded in one post, such as a `Table` for a comparison table, is legitimate. Do not flag it as a duplicate.

### The "Invalid object type for field" error

The Search Console error `Invalid object type for field "<parent_node>"` is almost always a self-serving review. `<parent_node>` is the object holding the `review`. Only a narrow set of types (Product, LocalBusiness, Organization and a few others) may host review snippets, so a `review` on an `AboutPage`, `CollectionPage` or `WebPage` fails outright.

Confirm it by comparing a page carrying `review` with a similar page without one. **Delete the review block rather than moving it.** Re-typing the parent to `Organization` clears the error but still earns nothing, because Google has excluded self-serving reviews since 2019.

Finish an audit with a short prioritised list: what is broken, what it costs, and the fix. Not a dump of every block.

## Reading Search Console verdicts

URL Inspection reports the **last crawled version**, not the live page. A page fixed after its last crawl still returns the old verdict.

- Report the last crawl date alongside any failure, and compare it with when the fix shipped.
- A failure that predates a known fix is stale data, not a regression.
- No rich results detected is not an error. On most pages it is expected.
- To confirm a fix before Google recrawls, run the audit script on the live page, use **Test Live URL** in Search Console, then click **Validate Fix** to queue a recrawl.

## Finishing a piece of work

1. Write the change: the template's JSON-LD field, the page's custom code, or an Embed.
2. Confirm the write succeeded.
3. Tell the site owner plainly that the change is unpublished and needs publishing.
   - For a change to **CMS field values** (not the template), `publish_collection_items` pushes just those items live without publishing the whole site. Offer it. Do not run it unasked.
   - Publishing an item whose `isDraft` is `true` returns `ValidationError: Validation Failure`. That is expected: the field update is staged and goes live when the item does.
4. **After publishing, run the audit on the live URL.** Confirm every token resolved, no entities appeared, and dates and URLs are right. Only then call it done.

## Best Practices

1. **Audit the rendered page**, never only the template.
2. **Sample several items per collection**, including sparse ones.
3. **Delete self-serving reviews** rather than re-parenting them.
4. **Always quote the last crawl date** with a Search Console verdict.
5. **Do not call work done** until the live check passes.
