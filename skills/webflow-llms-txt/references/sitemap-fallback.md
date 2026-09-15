---
name: "Building an Inventory Without an API Token"
description: "Generating an llms.txt from sitemap.xml and live page fetches when no Webflow API token or MCP connection is available."
tags: [webflow, sitemap, fallback, no-token, crawling, inventory, public-web]
---

# Building an Inventory Without an API Token

The path for a site owner who wants to generate their own file, or for anyone working on a site they do not hold credentials for. Everything is read from the public web.

The output is the same shape as the API path. What changes is what you can see, and therefore how you decide what to exclude.

## Table of Contents

- [What you lose without a token](#what-you-lose-without-a-token)
- [Finding the sitemap](#finding-the-sitemap)
- [Reading the sitemap](#reading-the-sitemap)
- [Grouping URLs into sections](#grouping-urls-into-sections)
- [Reading page content](#reading-page-content)
- [Deciding what is in and what is out](#deciding-what-is-in-and-what-is-out)
- [Best Practices](#best-practices)

---

## What you lose without a token

| Not visible | Consequence |
|-------------|-------------|
| Draft and archived state | You cannot detect the stale-live-page case where an item is reverted to draft but still served. |
| CMS field data | Description fallbacks must come from the page's own meta description or its rendered content. |
| The page/template distinction | You infer collection membership from URL shape rather than reading it from a field. |
| Folder structure | Not a real loss. Sitemap URLs are already fully resolved. |

None of these prevent a good file. They mean the exclusion logic leans on the sitemap's own judgement, which is generally sound: Webflow omits drafts and unpublished pages from the sitemap it generates.

## Finding the sitemap

Try in order:

1. `https://{host}/sitemap.xml` — Webflow's default.
2. The `Sitemap:` directive in `https://{host}/robots.txt`, which is where a custom sitemap will be declared.

Use the canonical host. If `www` and non-`www` both resolve, HEAD-check both and use whichever does not redirect, because the sitemap will be written in terms of one of them and mixing hosts produces a file full of 301s.

A Webflow site with a custom sitemap configured in Site settings will serve that instead of the generated one. It may be narrower than the real site. If the page count looks implausibly small, say so rather than silently shipping a thin file.

## Reading the sitemap

Webflow generates a flat `<urlset>` rather than a sitemap index, so one fetch is usually enough. Handle the index case anyway — a large site or a custom sitemap may use one.

```bash
curl -sS "https://example.com/sitemap.xml" \
  | grep -oE '<loc>[^<]+</loc>' \
  | sed -E 's|</?loc>||g'
```

Take `<loc>` for the URL and `<lastmod>`, where present, as a sort key for recency. Ignore `<priority>` and `<changefreq>`; Webflow emits them as constants and they carry no information.

## Grouping URLs into sections

Without collection metadata, infer structure from URL shape. Path prefixes on a Webflow site map to collections reliably, because CMS template pages live under a folder.

```
/                      -> Standard Pages (the home entry)
/about, /contact, ...  -> Standard Pages
/blog/{slug}           -> a Blog section
/work/{slug}           -> a Case Studies section
/legal/{slug}          -> Optional > Legal
```

Derive the groups from what is actually present rather than assuming a fixed set. A prefix with a single URL under it is usually an index page, not a collection; a prefix with many is a collection.

Confirm the grouping with the site owner before the first run if one is available. Getting it wrong is cosmetic rather than fatal, but the file reads better when its sections match how the site owner thinks about their own site.

## Reading page content

You will need page content to write honest descriptions, since the meta description alone is rarely enough and must not be reused verbatim.

Fetch each page and extract the title, the meta description, the H1, and the first substantive paragraph or the section headings. That is normally sufficient to say what a page *is* and what it covers.

Two practical notes:

- Many sites return `text/markdown` to non-browser user agents through content negotiation, which makes reading page content much cheaper than parsing HTML. Try it. It is not the same as a `.md` variant and does not change the rule that the file must contain plain HTML URLs.
- Be polite. Fetch sequentially with a small delay rather than hammering the site in parallel, and stop if you start seeing rate-limit responses.

## Deciding what is in and what is out

Exclude a URL if any of these hold:

| Condition | Why |
|-----------|-----|
| It 301s | Emit the destination instead, and record the change. |
| It 404s | Gone. Drop it and record it. |
| It is a system or utility page | `/404`, the password page, search results, thank-you and confirmation pages. |
| It is a paginated duplicate | `?page=2` and similar add nothing. |
| It has no readable content | Nothing truthful to say about it. |
| It is a CMS template preview | Rare in a sitemap, but if a URL renders binding tokens rather than content, drop it. |

Trust the sitemap on draft state. Webflow excludes unpublished pages from the sitemap it generates, so a URL's presence is reasonable evidence it is live. The one case this misses — an item reverted to draft after publishing — is invisible on this path. If the site owner has API access, that case is worth a separate check; if not, note the limitation rather than implying the audit was exhaustive.

## Best Practices

- Resolve the canonical host before fetching anything else. Mixing `www` and non-`www` is the most common cause of a file full of redirects.
- Fetch sequentially and politely. This is someone's production site.
- Derive sections from the URL prefixes actually present, not from a template.
- Say plainly which checks this path cannot perform, rather than presenting the result as equivalent to a token-backed audit.
- If the sitemap looks implausibly thin, investigate before shipping. A custom sitemap set in Site settings will override the generated one.
