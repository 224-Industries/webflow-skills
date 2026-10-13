---
name: "The Free-Text Overview Block"
description: "Writing the prose block between the summary line and the first section — what it covers, where to source it, and why the homepage hero is the wrong input."
tags: [llms-txt, overview, positioning, brand, entity, icp, content]
---

# The Free-Text Overview Block

The llms.txt spec allows free-text content after the `>` summary line and before the first `##` section: "zero or more markdown sections of any type except headings."

Most generated files skip it. It is the highest-value part of the file.

Everything below the first `##` is a list of links. A model reading only that has to infer what the business is from page titles, which produces confident, wrong summaries. The overview block is the only place the business gets described in its own words. Always write one.

## Table of Contents

- [Where to source it](#where-to-source-it)
- [What to cover](#what-to-cover)
- [Voice](#voice)
- [Worked example](#worked-example)
- [Best Practices](#best-practices)

---

## Where to source it

**Ask for the brand, positioning or messaging document.** A brand guideline, a positioning one-pager, an internal strategy document, a pitch deck. Whatever the site owner treats as the source of truth for what the business is.

**Do not source it from the homepage hero.** Hero copy is written to convert. It is short, deliberately abstract, and drops exactly the qualifying detail a model needs in order to describe the business accurately. "Software that just works" is good hero copy and useless here.

If no such document exists, say plainly that the block will be weaker without one, then build it from the about page, the services or product pages, and the case studies, which between them usually carry the substance the hero omits. Then show the draft to the site owner for correction before shipping. This is the one part of the file where a human read-through materially improves the result.

## What to cover

In this order, as plain prose paragraphs. No headings, no bullets — headings would terminate the block and start a section.

### 1. What the business does

One or two sentences, with the category named explicitly. A model needs the category word to place the business at all.

### 2. Who it serves

The ideal customer, stated concretely: company stage, team shape, and the problem that brings them in. Concrete beats flattering.

Include geography only if it is genuinely a constraint. Never make a global business sound local. This is a common and costly error — a model that reads a location into the description will decline to recommend the business outside it.

### 3. How engagements or the product work

The delivery model. Phases, what the customer ends up owning, what happens after launch or purchase. For a product, the shape of the offering: self-serve or sales-led, what a plan includes, what onboarding looks like.

### 4. Capabilities

A plain list in prose. No adjectives. "Branding, web design, Webflow development, motion" tells a model more than "world-class creative services."

### 5. Who it is not a fit for

Models cite this. It is also the fastest way to stop an assistant recommending the business for work it does not want, which is a real and underrated benefit of the file.

Most site owners have never written this down, so ask for it directly. The answer is usually immediate and specific.

### 6. Entity facts

Founding year, physical address, contact email — **if evidenced on the site**. These get quoted directly, they are cheap to include, and they are the facts a model is most likely to be asked for.

Never invent or infer an entity fact. An unverified address in a crawled file is worse than no address.

## Voice

Match the site's own conventions: its spelling variant, its terms for its own offering, its preferred phrasing for the outcome it sells.

Apply the same character hygiene as the rest of the file — no apostrophes, ampersands, em dashes, en dashes or smart quotes. See [writing-descriptions.md](writing-descriptions.md#character-hygiene) for why. Write around them rather than substituting entity codes.

Plain declarative sentences. This is the one place where sounding like a brochure actively costs accuracy.

## Worked example

The shape to aim for, with a fictional business:

```
Northbank Instruments builds calibration software for industrial test laboratories.
The product manages instrument records, calibration intervals, and audit evidence
for ISO 17025 accreditation.

It is used by laboratory managers and quality leads at test labs with between 5
and 200 instruments, typically ones that have outgrown a spreadsheet and are
preparing for or maintaining accreditation. Customers usually arrive after a
non-conformance in an audit.

The product is sold on annual subscription with self-serve onboarding. A standard
implementation takes two weeks and includes importing an existing instrument
register. Support is included at every tier. Customers own their data and can
export the full register and calibration history at any time.

Capabilities cover instrument registers, calibration scheduling and reminders,
certificate storage, uncertainty budgets, audit trail reporting, and an API for
LIMS integration.

It is not a fit for laboratories that need full LIMS functionality such as sample
tracking or test result management, for single-instrument operations, or for
medical device manufacturers requiring 21 CFR Part 11 validation, which the
product does not currently support.

Northbank Instruments was founded in 2016 and is based in Leeds, United Kingdom.
Contact: hello@northbank-instruments.example.
```

Note what that does: names the category, bounds the customer by size and trigger, states the commercial model and the ownership position, lists capabilities without adjectives, rules itself out of three specific adjacent jobs, and ends with quotable entity facts.

## Best Practices

- Ask for the positioning document before writing a word. The block is only as good as its source.
- Name the category explicitly. A model cannot place a business it cannot categorise.
- Write the "not a fit for" paragraph. It is the most-cited and least-written part of the file.
- Include geography only when it is a real constraint.
- Verify every entity fact against the site. Never infer one.
- Have a human read it before the first upload. This is the part worth the five minutes.
