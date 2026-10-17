---
name: "Questions, Check-ups and Diagnosing a Change"
description: "The three ways the skill is used (a single question, a monthly check-up and diagnosing a traffic change), with the call plan and answer layout for each."
tags: [check-up, monthly-report, diagnose, traffic-drop, cross-product, answer-format, workflow]
---

# Questions, Check-ups and Diagnosing a Change

## Table of Contents

- [Answering a question](#answering-a-question)
- [Monthly check-up](#monthly-check-up)
- [Diagnosing a change](#diagnosing-a-change)
- [Answer layout](#answer-layout)
- [Best Practices](#best-practices)

## Answering a question

1. Work out which products the question touches, and check only those (see `availability.md`).
2. Resolve the window. If the person gave none, pick a sensible default and say which: last 28 days for traffic, the latest interval for a test, the last 7 days for crawlers.
3. Run the fewest reports that answer it. "Which pages get the most traffic?" is one call, not five.
4. Answer in the layout below. A one-line question gets a short answer.

Questions that span products ("why did traffic drop, and is it the test?") follow **Diagnosing a change**.

## Monthly check-up

The default window is the last complete calendar month in the site's time zone, compared with the month before. If the person asks for "the last 30 days", use rolling windows instead.

Check all three products first. Then run what's available, and check both months' daily series for automated spikes before writing any comparison (see `analyze.md` > Check for automated traffic before comparing).

| Section | Product | Calls |
|---|---|---|
| Traffic | Analyze | `get_traffic_report` sessions for both months; users and pageviews for the current month |
| Top pages and movers | Analyze | `get_top_pages_report`, limit 25, for both months. Compare to find the biggest rises and falls, and any page that's new to the list or has dropped off it |
| Where visitors come from | Analyze | `get_top_dimensions_report` for `trafficSource` and `referrer`, current month. Note any AI-tool referrers |
| Goals | Analyze | `list_goals`, then `get_goal_performance` for each goal, both months. Work out a conversion rate against sessions, labelled as calculated |
| Tests | Optimize | Live tests and anything that finished during the month, each with type, goal and where it stands |
| AI crawlers | AEO | `get_bot_traffic` total for both months, and `get_bot_traffic_pages` top 10 for the current month |
| AI visibility | AEO | `get_visibility` and `get_citation_rate` by topic, if prompt tracking is on |

Check-up layout:

```markdown
## [Site name]: [Month YYYY] check-up

[Two or three sentences: the most important thing that happened, then the second.]

**Traffic:** [sessions] visits, [up/down X%] on [previous month] ([previous sessions]). [users] visitors, [pageviews] pageviews.

**Top pages:** [top 5, each with visits and change]
**Biggest movers:** [up to 3 rises and 3 falls, with counts]

**Where visitors came from:** [top sources with share of visits]. [AI-tool referrals, if any]

**Goals:** [each goal: conversions, change, calculated rate]

**Tests:** [each live or finished test: name, type, goal, current standing in plain words]

**AI crawlers:** [total requests and change; most-read pages]
**AI visibility:** [visibility and citation rate, with the top topic]

**Worth looking at:**
1. [Most useful action, tied to a number above]
2. [...]
(up to 5)

[One line naming any product the site doesn't have, per availability.md]
```

Leave out any section whose product isn't available. Don't print empty headings.

## Diagnosing a change

Use this when someone says traffic, conversions or leads dropped or jumped. Work through it in order and stop when the cause is clear.

1. **Confirm the change.** Run `get_traffic_report` daily for the period and the one before. Find the day it started. If the change is small or within normal weekly swings, say so. That can be the whole answer. If it's a short spike, check it for automated traffic before going further: filter to the spike days and look at country, top pages and sessions against visitors.
2. **Find where it happened.** Run `get_top_pages_report` for both periods: is it one page, one section or everywhere? Then `get_top_dimensions_report` for `trafficSource`, `deviceType` and `country`: is it one source, one device or one market?
3. **Check what changed on the site.** Look for Optimize tests that started, stopped or changed near the start day (from the intervals). Check the site's `lastPublished` date from `get_site`. Check whether the affected pages still exist, using `data_pages_tool`, and whether the 404 page rose at the same time.
4. **Check AI crawlers, if AEO is available.** Did requests to the affected pages change around the same date?
5. **Give a conclusion with a confidence level.** "Most likely: organic search visits to the three service pages fell from 15-09, the same week the services section was republished. I'd put this at moderate confidence: the timing lines up, but Analyze can't see search rankings."
6. **Say what Webflow's data can't show.** Search rankings and queries live in Google Search Console. Ad spend changes live in the ad platform. Say which source would settle the question.

## Answer layout

For anything other than a check-up:

1. **The answer**, in one or two sentences, first.
2. **The numbers behind it**, with the date window in local dates.
3. **What it means or what to do next**, up to three points, each tied to a number.
4. **What the data can't tell you**, only when it matters to the question.
5. **The availability note**, one line, only when a missing product is relevant.

Writing rules:

- Plain words. Say "visits", not "sessions", unless the person used the term.
- Numbers as counts and percentages together.
- No raw ids, field names, status codes or JSON in the answer.
- Hedge judgements, not facts. "Visits fell 18%" is a fact. "Probably because of the redesign" is a judgement and gets the hedge.
- When there's nothing notable, say so in one line rather than padding.

## Best Practices

- Default windows are a choice, so say which one you made.
- In a check-up, lead with the change that matters most to the business, which is usually goals before traffic.
- Keep the action list short and specific. "Set up a goal for the contact form, so next month's check-up can count enquiries" beats "improve tracking".
- A diagnosis that ends in "not sure, here's what would settle it" is better than a confident wrong cause.
