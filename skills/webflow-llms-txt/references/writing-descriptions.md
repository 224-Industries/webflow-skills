---
name: "Writing llms.txt Descriptions"
description: "Why meta descriptions fail as llms.txt descriptions, per-page-type patterns for writing good ones, the overrides file, and character hygiene."
tags: [llms-txt, descriptions, meta-description, copywriting, overrides, character-hygiene, json-ld]
---

# Writing llms.txt Descriptions

The description after each link is where a generated file is usually worst, because the path of least resistance is to lift the meta description, and the meta description is written for a different job.

## Table of Contents

- [Why meta descriptions fail here](#why-meta-descriptions-fail-here)
- [Rules for a good description](#rules-for-a-good-description)
- [Patterns by page type](#patterns-by-page-type)
- [The overrides file](#the-overrides-file)
- [Character hygiene](#character-hygiene)
- [Best Practices](#best-practices)

---

## Why meta descriptions fail here

A meta description is written to win a click in a search result. It opens with an imperative, it markets the subject of the page, and it deliberately withholds detail to create curiosity.

An llms.txt description has the opposite job. It tells a model what the page **is** and what it **covers**, so the model can decide whether reading the page is worth it.

Compare, for a case study page:

> **Poor:** Discover how Meridian Health transformed their digital presence with a stunning new website that drives real results.

That markets the client and says nothing about the page. A model cannot tell whether it is a case study, a service page, or a blog post, nor what was actually built.

> **Good:** Case study on the website built for Meridian Health, an allied health clinic group. Covers branding, information architecture, Webflow build and booking integration.

That names the page type, identifies the subject in a few words, and lists what the page covers. A model routing a question about booking integrations can now find it.

Webflow's own guidance says the same thing more bluntly: avoid pasting marketing copy verbatim, and describe what things actually do.

## Rules for a good description

- **One line, roughly 100 to 160 characters.** Long enough to be specific, short enough to scan.
- **Lead with what the page is.** Case study, guide, service page, index, contact page, policy.
- **Then say what it covers.** The sub-topics, the scope, the named entities.
- **Factual only.** Never invent a claim, a metric, or a service that is not evidenced on the page. If the existing description is not enough to write from, fetch the page and read it. If the page has nothing readable, leave it out of the file and record it in the changelog.
- **Match the site's spelling convention.** Australian, British or American, whichever the site uses.
- **No adjectives doing load-bearing work.** "Comprehensive", "innovative" and "leading" carry no information and cost characters.

## Patterns by page type

### Case studies and project pages

Name the client and what they do in a few words, then what was built.

> Case study on the {what was built} for {client}, a {what they do}. Covers {scope}.

### Blog posts and guides

State the question the post answers, then the sub-topics.

> Guide answering {question}. Covers {sub-topics}.

Avoid restating the title as a sentence. If the title is "How to set up 301 redirects in Webflow", the description should not be "A guide to setting up 301 redirects in Webflow." Say what it covers that the title does not: bulk imports, wildcard rules, the Enterprise API path.

### Service or product pages

What the service is, what it includes, who it is for.

> {Service} for {audience}. Covers {what is included}.

### Index and listing pages

Say what it lists and name a few entries, so a model knows whether following the link is worthwhile.

> Index of {what}, including {two or three named examples}.

### Contact, pricing and legal pages

Plain and literal. These are the pages models are most often asked to find, and cleverness costs accuracy.

> Contact form and business details including address and email.

> Pricing for {offering}, with {tier names} and what each includes.

## The overrides file

Descriptions belong in a file of their own, decoupled from the site's meta descriptions. Optimising one string to serve both search snippets and model routing compromises both.

Keep `descriptions.md` in the working directory for the site. One markdown table per section:

```markdown
# Description overrides

Curated llms.txt descriptions, keyed by URL. These win over the page or CMS meta
description when llms.txt is generated. A URL absent from this file falls back to
its meta description and is flagged in the changelog.

## Standard Pages

| URL | Description |
| --- | --- |
| https://example.com | Home page for {business}, a {category}. Covers {top-level offering}. |
| https://example.com/about | Background on {business}, its founding, team and approach. |

## Blog

| URL | Description |
| --- | --- |
| https://example.com/blog/some-post | Guide answering {question}. Covers {sub-topics}. |
```

**Resolution order when generating the file:**

1. The curated line in `descriptions.md` for that exact URL.
2. Failing that, the page or CMS meta description, as a stopgap.
3. Flag every URL that fell through to (2) in the changelog, under a "needs a curated description" heading.

This is what makes the file converge. Every run writes back the URLs it had to fall back on, so the backlog is visible and shrinks over time instead of being silently re-lifted each month.

## Character hygiene

**No apostrophes, ampersands, em dashes, en dashes, smart quotes, non-breaking spaces or HTML entities anywhere in the file.**

The rationale is downstream reuse. This file's content routinely gets lifted into JSON-LD script blocks, CSV exports and other contexts where it is escaped a second time, and the result is literal entity codes (`&#39;`, `&amp;`) appearing in structured data and in model output. Straight ASCII survives every one of those trips.

Write around the characters rather than escaping them:

| Instead of | Write |
|------------|-------|
| the client's team | your team, or the client team |
| Design & development | Design and development |
| a dash — like this | a dash, like this |
| "smart quotes" | plain wording, or straight quotes if unavoidable |

Also check for replacement characters (U+FFFD). Their presence means something upstream had an encoding bug, usually a mangled em dash. Fix it and mention the fix in the changelog.

The validator script enforces all of this:

```bash
python scripts/validate_llms_txt.py llms.txt
```

## Best Practices

- Never ship a description you lifted verbatim. If you had no time to rewrite it, flag it rather than hiding it.
- Fetch and read the page when the meta description is too thin to write from. Guessing is the one unrecoverable error.
- Keep `descriptions.md` under version control alongside the generated file. It is the asset that compounds.
- Run the validator before handing anything over, every time.
- When a description cannot be written truthfully, omit the page. An absent entry costs a little discoverability; a fabricated one costs credibility.
