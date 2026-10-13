---
name: "Building an Inventory via the Webflow Data API"
description: "Reading a site's pages and CMS items through the Webflow Data API, including the rich-text context trap and field behaviours that differ from expectation."
tags: [webflow, data-api, pages, cms, collections, inventory, pagination, rich-text, drafts]
---

# Building an Inventory via the Webflow Data API

The preferred path when an API token or the Webflow MCP is available. It is more accurate than the sitemap fallback because it exposes draft and archived state, distinguishes CMS template pages from the items they render, and gives access to arbitrary CMS fields for description fallbacks.

## Table of Contents

- [Required scopes](#required-scopes)
- [The context window trap](#the-context-window-trap)
- [Call sequence](#call-sequence)
- [Deciding what is in and what is out](#deciding-what-is-in-and-what-is-out)
- [Field behaviours that differ from expectation](#field-behaviours-that-differ-from-expectation)
- [Mapping collections to sections](#mapping-collections-to-sections)
- [Best Practices](#best-practices)

---

## Required scopes

Read-only throughout. `sites:read`, `pages:read`, `cms:read`.

Never request or use write scopes for this work. If a run appears to need one, the answer is to hand the task to a human, not to escalate permissions.

## The context window trap

**Read this before making a single collection call.**

`list_collection_items` returns the **full rich-text body of every item**. On a content-heavy blog collection this is routinely 15 to 20 KB per item. Three posts can come back at 50 KB. A whole collection requested at `limit: 100` can exceed 1 MB, and fetching several collections in one batch will exhaust the context window and kill the run before a single line of output is written.

The discipline:

- **One collection per call.** Never batch collection requests.
- **`limit` of 25 or lower.** Page with `offset` when `pagination.total` exceeds your limit.
- **Extract immediately.** The moment a response lands, pull out only the fields you need — typically `name`, `slug`, `isDraft`, `isArchived`, the date field you will sort by, and the description field. Discard the rest.
- **Never re-request a collection you have already extracted.**

This single behaviour is the difference between a run that completes and a run that does not.

## Call sequence

### 1. Site metadata

Fetch the site. Take its display name for the file header and its custom domain for the canonical host.

The custom domains field is an **array of objects**, not an array of strings. Each entry carries `id`, `url`, `lastPublished` and related fields, and `url` has **no scheme** — prepend `https://` yourself.

If a site has several custom domains, do not guess. HEAD-check the candidates and use whichever does not redirect. A site with `www` and non-`www` variants will 301 one to the other; emit the destination.

### 2. Pages

List pages with a limit of 100. The response is shaped `{pages: [...], pagination: {limit, offset, total}}`. Page through if `total` exceeds the limit.

### 3. Collections

List collections first only if you need to confirm IDs. Note that the collection list returns names and IDs but **not field schemas**, despite what its description may imply. Use the collection details call if you genuinely need to verify a field slug.

Then call for items, one collection at a time, under the discipline above.

## Deciding what is in and what is out

### Pages

Exclude a page if any of these hold:

| Condition | Why |
|-----------|-----|
| It has a `collectionId` field | It is a CMS collection *template*, not a page. The items it renders are inventoried separately. |
| `draft` is `true` | Not public. |
| `archived` is `true` | Not public. |
| Slug is `404` | System page. |
| Slug is `401` | The password page. Note the slug is `401`, not `password`, even though its title is usually "Password". |
| It is a search results page | No stable content to describe. |
| No usable description and no readable content | Nothing truthful to say about it. Record it in the changelog instead. |

The `collectionId` field is the reliable signal for a template page. A `detail_` slug prefix correlates with it, but that is a naming convention a site owner can break; `collectionId` is an actual API field.

Template pages also carry HTML-escaped Webflow binding tokens in their SEO title and description fields — strings containing `{{wf` and `&quot;path&quot;`. Never emit those as real text. If you see one, you are looking at a template page you should have excluded.

### CMS items

Exclude an item if `isDraft` is `true`, `isArchived` is `true`, or nothing resolves to a description and the live page cannot be read.

**One caveat worth surfacing to the site owner.** `isDraft` is not a reliable "is this live" test. An item that was published and then reverted to draft will report `isDraft: true` while still carrying a `lastPublished` date and still being live on the site.

When an item is `isDraft: true` **and** has a `lastPublished` value, exclude it from the file, because the CMS says it should not be live, but call it out in the changelog under a "needs a decision" heading. It is a stale live page the owner should either republish properly or unpublish properly.

## Field behaviours that differ from expectation

These are the things that break naive code. Check here before debugging.

| Behaviour | Detail |
|-----------|--------|
| **Home has no `slug` key** | Not an empty string. Absent. Any code that reaches for `page.slug` unguarded will throw on the home page. |
| **Use `publishedPath`, not `slug`** | `publishedPath` accounts for folder nesting. The pages call does not return parent-folder information at all, so the slug alone cannot reconstruct a nested URL. |
| **`publishedPath` is not unique** | A static page and the CMS template that renders items of the same type commonly report the same path. Never key a map on `publishedPath`. Key on `id`. |
| **Home's `publishedPath` is `/`** | Its URL is the bare host with no trailing slash. |
| **`seo` may be empty** | It can be an empty object, or carry a title with no description. Do not assume `seo.description` exists. |
| **Unset CMS fields are inconsistent** | Some collections omit an unset key entirely; others return an explicit `null`. Treat absent, `null` and empty string identically. |
| **Rich text arrives as HTML** | Short-description and summary fields of type RichText come back wrapped in paragraph tags, sometimes with an `id` attribute. Strip tags, decode entities, collapse whitespace. |
| **`lastPublished` is absent on never-published drafts** | Its presence is what distinguishes a never-published draft from a reverted one. |

### Titles

Prefer the SEO title, falling back to the page title. If the SEO title ends with a brand suffix (` | Brand Name`, ` - Brand Name`), trim it — the file header already names the site.

Trimming a suffix is fine. Substituting a nicer title you invented is not.

The home page entry is titled with the site name.

## Mapping collections to sections

Not every collection represents pages. Before the first run, establish for each collection:

- Whether it represents real, addressable pages at all
- Which `##` section of the file it feeds
- Its URL pattern, for example `/blog/{slug}`
- The ordered list of field slugs to try for the description fallback

Field slugs vary per site and per collection within a site. Never assume they match another site's. Read them from the collection details call.

**Exclude supporting collections outright.** Team members, image libraries, Open Graph images, testimonials, FAQ entries and similar are data that other pages render, not pages in their own right. Querying them wastes context for nothing and, given the rich-text trap above, the waste is not trivial.

## Best Practices

- One collection per call, limit 25 or lower, extract immediately, never re-request.
- Key every map on `id`, never on `publishedPath` or title.
- Guard every access to `slug`. The home page will find the one place you did not.
- Treat absent, `null` and empty string as the same thing when resolving description fallbacks.
- Record the collection-to-section mapping somewhere durable after the first run. Re-deriving it each month is wasted effort and invites inconsistency.
- Read-only scopes only. A write scope on this task is a bug, not a convenience.
