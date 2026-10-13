---
name: "Re-running and Diffing an Existing File"
description: "Auditing a site against its previous llms.txt — what to diff, how to re-pair slug changes, and the changelog format."
tags: [llms-txt, audit, diff, changelog, maintenance, recurring, slug-changes]
---

# Re-running and Diffing an Existing File

An llms.txt is only as good as its last regeneration. Pages ship, slugs change, posts get retitled, and a file that was accurate in March describes a site that no longer exists by June.

The recurring run produces two things: the refreshed file, and a changelog that tells the site owner whether uploading it is worth their time this month.

## Table of Contents

- [First run versus recurring run](#first-run-versus-recurring-run)
- [What to diff](#what-to-diff)
- [Re-pairing slug changes](#re-pairing-slug-changes)
- [Changelog format](#changelog-format)
- [A large first diff is not a month of change](#a-large-first-diff-is-not-a-month-of-change)
- [Best Practices](#best-practices)

---

## First run versus recurring run

The previous state is the stored `llms.txt` from the last run. Parse it by section; every entry line has the form `- [Title](URL): Description`.

If no previous file exists, **this is a first run**. Say so plainly, write the files, and make the changelog a baseline summary: counts per section, pages with no usable description, link failures, and URLs still falling back to a meta description. Do not manufacture a diff against nothing.

If a live file exists at `{host}/llms.txt` but no stored copy does, fetch the live one and diff against that. It is usually more informative than a baseline, because it shows how far the published file has drifted.

## What to diff

Match entries **on URL**, falling back to title when a URL has changed. Report:

- Pages and items **added**
- Pages and items **removed**
- Items that went to **draft or archived**
- **Title** changes, old then new
- **Description** changes, old then new, truncated to roughly 15 words each side
- **Slug or URL** changes
- Any URL that **failed the HEAD check**, with its status code
- Pages with **no description** that had to be skipped
- URLs still falling back to a meta description
- Anything needing a decision, such as an item that is `isDraft: true` but still live

Do this deterministically rather than by eye:

```bash
python scripts/diff_llms_txt.py previous-llms.txt llms.txt
```

The script returns JSON with `added`, `removed`, `changed` and `repaired` arrays. Write the changelog from that, not from a visual comparison.

## Re-pairing slug changes

A changed slug surfaces as one addition plus one removal, because the URL key changed. Reporting it that way is actively misleading: a site owner reading "one page added, one page removed" will go looking for a page that was never deleted.

Re-pair them by matching titles across the added and removed lists, and report the result as a single "URL changed" line. The diff script does this automatically and returns the pairs under `repaired`, but check its work when titles also changed in the same run — a page that was both retitled and re-slugged will not auto-pair, and needs a human eye.

## Changelog format

Short and scannable. This gets read by a site owner, so no tool names, no API call counts, no internal mechanics. Skip any heading with nothing under it.

```markdown
# Site Name - llms.txt update, 14 September 2026

One or two sentences: what changed this month, and whether anything needs attention.

## Added
- [Title](url) - Blog

## Removed
- [Title](url) - was in Case Studies

## Updated
- **Title** - description rewritten
- **Title** - URL changed from /old-slug to /new-slug

## Needs your attention
- [Title](url) returned 404 and has been removed from the file
- "Page Title" has no meta description, so it is not in the file yet
- "Item Title" is set to draft but is still live on the site. It should either be republished or unpublished properly.

---
Upload: Site settings > SEO > LLMs.txt > Upload file
```

Two notes on tone. The "needs your attention" items are the reason the changelog exists — they are findings the site owner cannot get any other way, and they should be phrased as observations with a suggested action, not as faults. And the upload line goes at the bottom of every changelog, because the file does nothing until somebody uploads it.

## A large first diff is not a month of change

The first run against an inherited file frequently produces an enormous diff, because the published file was generated once and never refreshed. Dozens of missing posts, stale slugs, pages that no longer exist.

Say that plainly. Presenting accumulated drift as a single month of change misrepresents both the site and the work. The honest framing is that the published file had drifted by however many entries, and this run brings it current.

## Best Practices

- Diff programmatically. Visual comparison misses description edits, which are the most common change and the least visible.
- Re-pair slug changes before writing the changelog, and check the pairing when titles changed too.
- Keep the stored `llms.txt` under version control. It is the only record of what the site looked like last month.
- Write the changelog for the site owner, not for yourself.
- Never ship a URL that failed the HEAD check. Follow the redirect or drop the entry.
