---
name: "llms.txt File Format"
description: "The exact output format — header, summary line, overview block, section ordering, entry syntax, and the spec's Optional convention."
tags: [llms-txt, format, spec, structure, sections, optional, ordering]
---

# llms.txt File Format

The structure defined by the llms.txt spec, with the ordering conventions this skill applies on top of it.

## Table of Contents

- [Structure](#structure)
- [Template](#template)
- [Section ordering](#section-ordering)
- [The Optional section](#the-optional-section)
- [Entry syntax](#entry-syntax)
- [Validation](#validation)
- [Best Practices](#best-practices)

---

## Structure

The spec defines five elements, in this order:

| Element | Required | Spec wording |
|---------|----------|--------------|
| H1 | Yes | "An H1 with the name of the project or site. This is the only required section" |
| Blockquote | No | "A blockquote with a short summary of the project, containing key information necessary for understanding the rest of the file" |
| Free text | No | "Zero or more markdown sections of any type except headings, containing more detailed information about the project" |
| H2 sections | No | "Zero or more markdown sections delimited by H2 headers, containing file lists of URLs where further detail is available" |
| Entries | — | "a required markdown hyperlink `[name](url)`, then optionally a `:` and notes about the file" |

Only the H1 is required by the spec. All five are required by this skill — a file with a bare H1 and a link list is technically valid and practically useless.

Note the constraint on the free-text block: **any type except headings**. A heading terminates the block and begins a section, so the overview must be plain prose paragraphs.

## Template

Match this exactly. One blank line between sections, no trailing whitespace, newline at end of file.

```
# Site Name
> One-line summary of what the site is and who it serves.

Free-text overview block: what the business does, who it serves, how engagements
or the product work, capabilities, who it is not a fit for, entity facts. Plain
prose paragraphs, no headings, no bullets.

## Standard Pages
- [Title](https://example.com): Description of what the page is and covers.
- [Title](https://example.com/about): Description.

## Blog
- [Title](https://example.com/blog/post-slug): Description.

## Case Studies
- [Title](https://example.com/work/project-slug): Description.

## Optional

### Legal
- [Privacy Policy](https://example.com/legal/privacy): Description.
```

## Section ordering

1. **Standard Pages** first. The site's fixed pages, home first.
2. **Collection sections** next, in order of importance to the business. A blog usually precedes case studies; a product catalogue usually precedes both.
3. **`## Optional` last.** Always.

Within a section:

- **Dated content newest first**, sorted on the publish date descending, so the freshest material is what a crawler reads first in a truncated read.
- **Everything else** keeps the site's own ordering, or alphabetical where the site has none.

Omit a section entirely if it has no qualifying entries. An empty heading is noise.

## The Optional section

`## Optional` is part of the spec and carries a defined meaning: by convention it holds "secondary information: links an agent can skip when a shorter context is needed."

This is where lower-priority links belong — legal pages, policies, anything a model should be able to find but should not weight as core content.

Two consequences worth stating:

- Legal pages go under `## Optional`, with an `### Legal` sub-heading. Never in a top-level `## Legal` section, which would signal they are core content.
- Do not put anything under `## Optional` that you actually want read. The convention exists so agents can drop it.

## Entry syntax

```
- [Title](URL): Description
```

- **Title**: the page's SEO title with any brand suffix trimmed, falling back to the page title. The header already names the site, so ` | Brand Name` on every line is wasted bytes.
- **URL**: absolute, on the canonical host, plain HTML. No `.md` suffix — Webflow does not serve markdown variants. No trailing slash on the home entry, whose path is `/`.
- **Description**: one line, no line breaks. See [writing-descriptions.md](writing-descriptions.md).

The colon and space after the closing parenthesis are what parsers key on. Keep the shape exact so next month's diff can read this month's file.

## Validation

```bash
python scripts/validate_llms_txt.py llms.txt
```

Checks encoding, byte size against the 100 KB ceiling, character hygiene, the presence of the H1, summary and overview block, and that every entry line parses.

```bash
python scripts/check_urls.py llms.txt
```

HEAD-checks every URL. Follow a `301` and emit its destination; drop a `404`. Never ship a URL you know is broken.

## Best Practices

- Write all five structural elements, not just the ones the spec requires.
- Keep the entry line shape byte-exact. The diff depends on it.
- Sort dated sections newest first. Truncated reads are common.
- Reserve `## Optional` for what you are willing to have skipped.
- Validate before handing over, not after.
