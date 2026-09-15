---
name: "Webflow Platform Constraints"
description: "What Webflow itself specifies about llms.txt — upload location, size and encoding limits, staging domain behaviour, markdown variants, and its own content guidance."
tags: [webflow, llms-txt, constraints, site-settings, seo, upload, encoding]
---

# Webflow Platform Constraints

These are platform behaviours, not preferences. They come from Webflow's official guidance on uploading an llms.txt file.

## Table of Contents

- [Upload location](#upload-location)
- [File requirements](#file-requirements)
- [Staging domain behaviour](#staging-domain-behaviour)
- [Markdown page variants are not supported](#markdown-page-variants-are-not-supported)
- [Webflow's content guidance](#webflows-content-guidance)
- [What this means for automation](#what-this-means-for-automation)
- [Best Practices](#best-practices)

---

## Upload location

**Site settings > SEO > LLMs.txt > Upload file**

It is a file upload, not a text field. There is no Data API endpoint for it and no Designer API surface. This is the single most important constraint on any tooling: an agent can *produce* the file, but a human has to put it on the site.

Do not confuse this with the Enterprise `well_known` endpoint, which writes to `/.well-known/` and is a different feature on a different plan tier.

## File requirements

| Requirement | Value |
|-------------|-------|
| Encoding | UTF-8 |
| Maximum size | Under 100 KB |
| Served at | `https://{custom-domain}/llms.txt` |

Check the byte size, not the character count, before handing the file over. A file that is comfortably under 100 KB in characters can exceed it in bytes once non-ASCII content is encoded, though if you are following the character hygiene rules in [writing-descriptions.md](writing-descriptions.md) the file should be close to pure ASCII anyway.

## Staging domain behaviour

The file is **not published to the Webflow staging domain**. It appears only on the custom domain.

`{site}.webflow.io/llms.txt` returning a 404 after a successful upload is expected behaviour and is not a fault to chase. Verify on the custom domain or not at all.

A corollary: a site that has not yet been connected to a custom domain cannot serve an llms.txt file at all. If a site owner asks why their uploaded file is not appearing, check the domain before checking the file.

## Markdown page variants are not supported

The llms.txt spec permits linking a markdown twin of each page, typically by appending `.md` to the URL. Webflow does not serve these. In Webflow's own words, its implementation is "intentionally scoped to the llms.txt file itself."

Practical consequences:

- Emit plain HTML URLs only.
- Never append `.md` to a URL in the file.
- Do not offer `.md` variants as an option to a site owner on Webflow.
- If an existing file contains `.md` URLs, strip the suffix and record the change in the changelog. They are dead links.

> A site may separately return `text/markdown` to non-browser user agents through content negotiation. That is a useful way to read page content cheaply when writing descriptions, but it is not the same thing as a `.md` variant and does not change the rule above.

## Webflow's content guidance

Webflow publishes specific guidance on how to write the file. Paraphrased, with its own emphasis preserved:

- **Structure clearly.** Use titles and sections, with a short description after each link.
- **Avoid marketing jargon.** Not "cutting-edge solutions for everyone." Say what the product actually does.
- **Be specific.** Include examples and links with clear, short descriptions.
- **Do not copy-paste.** Avoid pasting marketing copy or homepage hero text verbatim.
- **Write it pedagogically.** Webflow's framing: write it "like you're guiding a company intern who's never seen your site before" but who has to describe the business accurately to someone else.
- **Curate.** Public URLs only. Exclude internal or sensitive URLs.

The "do not copy-paste" line is the one most generated files violate, because lifting the meta description is the path of least resistance. See [writing-descriptions.md](writing-descriptions.md) for why that fails and what to do instead.

## What this means for automation

Three constraints compound into a clear division of labour:

1. There is no API for the upload, so tooling produces a file and stops.
2. The file does not update itself, so it goes stale the moment the site changes.
3. The file is not visible on staging, so there is no safe preview environment.

Together these mean the sensible cadence is a scheduled regeneration with a human upload step, and a changelog that tells the human whether the upload is worth doing this month.

## Best Practices

- Confirm the custom domain is connected before troubleshooting a missing file.
- Validate byte size and encoding before handing the file over, not after.
- Never promise a site owner that the file can be published programmatically. It cannot.
- Treat `.md` URLs in an inherited file as defects to fix, not as a style choice to preserve.
- Quote the upload path in full every time. Site owners rarely find it unaided.
