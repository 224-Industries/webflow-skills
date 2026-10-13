---
name: "Platform Limits"
description: "The two Webflow JSON-LD field limits found by live testing: bound CMS values are HTML-escaped, and bound RichText fields come back empty, plus which field types bind and how to write safe copy."
tags: [limits, escaping, html-entities, richtext, plaintext, binding, apostrophe, smart-quotes, field-types, json-ld-field]
---

# Platform Limits

## Table of Contents

- [Limit 1: bound CMS values are HTML-escaped](#limit-1-bound-cms-values-are-html-escaped)
- [Limit 2: bound RichText fields come back empty](#limit-2-bound-richtext-fields-come-back-empty)
- [Field types that bind](#field-types-that-bind)
- [Static text is not escaped](#static-text-is-not-escaped)
- [Best Practices](#best-practices)

---

## Limit 1: bound CMS values are HTML-escaped

A `<script>` block is a raw-text element, so character references inside it are never decoded by a browser or a parser. Webflow escapes the bound value anyway, so a consumer reads the escape code as literal text.

Observed on a live page, a bound key takeaway rendered as:

```text
Reverse proxies get you past Webflow&#39;s static page limits
```

That is what Google and every AI crawler sees.

**This is the most common way template schema breaks.** Any CMS field bound into the JSON-LD field must contain none of these:

| Character | Renders as |
|---|---|
| `'` straight apostrophe (U+0027) | `&#39;` |
| `"` straight double quote (U+0022) | `&quot;` |
| `&` ampersand | `&amp;` |

**Typographic punctuation is the fix, not rewording.** Only characters that are special in HTML get escaped. The curly forms are not, so they pass through raw:

| Character | Status |
|---|---|
| `’` smart apostrophe (U+2019) | Safe. Verified on a live page. |
| `“` `”` smart quotes (U+201C, U+201D) | Expected safe by the same mechanism. Not yet verified live. |
| `—` em dash, `–` en dash | Expected safe by the same mechanism. Not yet verified live. |

Write `It’s` with a smart apostrophe rather than avoiding the contraction. `&` has no typographic alternative, so spell it "and".

> **Do not reword schema copy away from the visible copy to dodge the escape.** Writing "Here is how" in the schema while the page says "Here's how" stops the schema matching what the page shows. That breaks the accuracy the whole approach rests on, and over time the two drift apart.

Check the field values before you bind anything with `scripts/check_bindable_text.py`, and check again on the live page after publishing.

## Limit 2: bound RichText fields come back empty

A RichText field bound into the JSON-LD field renders as an empty string. Not stripped of tags and not escaped: `""`. This was confirmed across multiple items, where FAQ questions (PlainText) rendered correctly and FAQ answers (RichText) came back empty.

**Rich text can never be template-bound.** If content needs to appear in schema and it lives in a RichText field, either:

- add a parallel PlainText field that exists only for schema, or
- use the client-side script approach (Architecture B in [architectures.md](architectures.md)).

## Field types that bind

| Type | Binds | Notes |
|---|---|---|
| `PlainText` | Yes | Subject to Limit 1 |
| `Number` | Yes | |
| `Date` | Yes | Renders ISO 8601. Use it for every date property. |
| `ImageRef` | Yes | Renders the image URL |
| `Link` | Yes | |
| Reference sub-fields | Yes | Written with a colon, for example `author:name` |
| `RichText` | No | Renders empty (Limit 2) |

## Static text is not escaped

Text typed directly into a static page's JSON-LD field is not escaped. Hand-written apostrophes in a static page's `description` render correctly on the live page. Do not rewrite static page copy to avoid apostrophes. The limits apply only to `{{wf ...}}` bindings.

## Best Practices

1. **Write schema-only fields as PlainText** from the start, with smart punctuation.
2. **Spell out "and"** in any bound field. There is no safe form of `&`.
3. **Keep schema copy identical to visible copy** wherever the same text appears on the page.
4. **Run the character check before binding** and the audit script after publishing.
5. **Add a parallel PlainText field** rather than trying to bind RichText.
