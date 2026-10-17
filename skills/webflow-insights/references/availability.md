---
name: "Product Availability and Client Wording"
description: "How to tell which of Analyze, Optimize and AEO Analytics a site has, how to read each response, and the exact plain-language wording to use when a product is missing."
tags: [availability, entitlement, plan, analyze, optimize, aeo, errors, wording, 403, 429]
---

# Product Availability and Client Wording

Not every Webflow site has all three products. Many have Analyze only, some have none, and AEO Analytics is mostly found on enterprise plans. A product the site doesn't have is a normal state, not a fault. The person asking should finish reading the answer knowing what their site does have and what it doesn't, without ever thinking something is broken.

## Table of Contents

- [The availability check](#the-availability-check)
- [Reading each response](#reading-each-response)
- [What the person reads](#what-the-person-reads)
- [How to place the note in an answer](#how-to-place-the-note-in-an-answer)
- [When the question is about a product the site doesn't have](#when-the-question-is-about-a-product-the-site-doesnt-have)
- [Mistakes that are yours, not the site's](#mistakes-that-are-yours-not-the-sites)
- [Best Practices](#best-practices)

## The availability check

Run one light read per product before the real queries. Probe only the products the question needs, except for a check-up, which probes all three.

| Product | Probe | Why this one |
|---|---|---|
| Analyze | `data_analyze_tool > list_goals` with the `site_id` | Takes no date window, so it can't fail on a bad range |
| Optimize | `data_optimize_tool > list_optimize_resources` | Lists every Optimize resource the connection can reach, each paired with the site it belongs to |
| AEO, crawler half | `data_aeo_tool > get_bot_traffic` for the last 7 days, ending today at `00:00:00.000Z` | Crawler reports have their own gate, separate from prompt tracking |
| AEO, prompt half | `data_aeo_tool > list_prompts` with `limit: 1` | Tells you whether prompt tracking is on and whether any prompts exist |

Send each AEO probe as its own call. `data_aeo_tool` validates the whole actions array before running any of it, so one bad sibling fails the lot.

## Reading each response

| What comes back | State | Notes |
|---|---|---|
| Analyze: data, or an empty goals list | **Available** | An empty goals list means no goals are set up, not that Analyze is off |
| Analyze: 403 whose message contains "Analyze entitlement required" | **Not on the plan** | |
| Analyze: 404 | **Not available for this site** | The endpoint is switched off for the site. Treat it like "not on the plan" in wording, without naming a plan |
| Analyze, on a Campaign Hub site | **Use the campaigns tool instead** | `data_analyze_tool` is for standard sites. Campaign traffic comes from `data_campaigns_tool` |
| Optimize: a resource whose site matches | **Available** | Keep its `optimizeId` for every later call |
| Optimize: empty list, or no resource for this site | **Not set up on this site** | Don't name a plan. Optimize may be bought but not set up, or not bought at all, and the response can't tell you which |
| Optimize: resource found, `list_optimizations` returns nothing live | **Available, nothing running** | Check `status: ["off", "archived"]` before saying there have never been tests |
| AEO: 403 whose message contains "AEO analytics entitlement required" | **Not on the plan** | Applies to both halves |
| AEO: crawler reports work, prompt or visibility reports are refused | **Crawler data available, prompt tracking not switched on** | Prompt tracking sits behind the workspace's AI features setting |
| AEO: `brand_not_configured` | **Available, brand not set up** | Visibility reports need the brand name entered in AEO settings |
| AEO: `competitors_not_configured` | **Available, competitors not set up** | Only affects competitor citation reports |
| AEO: `list_prompts` returns nothing | **Available, no prompts tracked yet** | |
| Any product: 403 without the word "entitlement" | **No access for this person** | Their Webflow role can't see this product. Their workspace admin can grant it |
| Any product: empty data or zeros | **Available, nothing recorded** | Zero is a valid answer. Say what was measured and over which dates |

## What the person reads

Use these lines, adjusted to the sentence around them. Don't swap in "blocked", "forbidden", "failed", "error", "denied" or "unauthorised" for any availability state, and never show a status code, an error name or raw JSON.

| State | Wording |
|---|---|
| Analyze not on the plan | "Analyze isn't switched on for this site, so Webflow doesn't hold traffic data for it." |
| Analyze not available for this site | "Webflow's Analyze data isn't available for this site." |
| Optimize not set up | "Optimize isn't set up on this site, so there are no A/B test results to show." |
| Optimize, nothing running | "You don't have any tests running right now." Add the last finished test if there is one. |
| AEO not on the plan | "AI search visibility (AEO Analytics) isn't included in your current Webflow plan. Webflow currently offers it as part of its Enterprise Analyze package." |
| Prompt tracking not switched on | "Webflow can see which AI crawlers visit your site, but tracking how AI answers mention you needs Webflow's AI features turned on for your workspace." |
| Brand not set up | "AI visibility tracking needs your brand name added in Webflow's AEO settings before it can report." |
| Competitors not set up | "To compare against competitors, add them in Webflow's AEO settings first." |
| No prompts tracked | "You're not tracking any AI prompts yet. Add a few in AEO settings and results will start to build up." |
| No access for this person | "Your Webflow account doesn't have access to [product] on this site. Your workspace admin can grant it." |
| Nothing recorded | "No [visits / conversions / crawler visits] were recorded between [start] and [end]." |
| Webflow not responding, after one retry | "Webflow didn't respond just now. Try again in a few minutes." |

## How to place the note in an answer

1. **Lead with what the site has.** A site with only Analyze gets a full Analyze answer. The availability note goes at the end.
2. **Say each missing product once per answer**, as one line, not once for every report that couldn't run.
3. **Group them when more than one is missing:** "This site has Analyze. Optimize isn't set up, and AEO Analytics isn't included in your current plan."
4. **Offer the way to get it once, without pushing.** One plain line, no prices, no "unlock" or "upgrade now". Skip it if you've already said it in this conversation.

## When the question is about a product the site doesn't have

When the question is about the missing product itself ("which pages did AI crawlers read last week?"), say so in the first line, then give the person whatever the available data can honestly say.

> That's not something Webflow can show for this site: AEO Analytics isn't included in your current plan. Analyze can show part of the picture, though. In the last 30 days, 14 visits arrived from chatgpt.com and 3 from perplexity.ai.

Useful fallbacks:

| Missing | What Analyze can still show |
|---|---|
| AEO | Visits referred by AI tools. Rank `get_top_dimensions_report` by `referrer` and look for chatgpt.com, perplexity.ai, gemini.google.com, claude.ai and copilot.microsoft.com. Only report the ones that actually appear. |
| Optimize | Before-and-after comparisons of a page around the date it changed. Label these as a comparison, not a test, because nothing controlled for other changes in that period. |

## Mistakes that are yours, not the site's

These come from the request, not the site. Fix the query and run it again without mentioning the error to the person.

| Response | Fix |
|---|---|
| `invalid_time_range` | Make sure `endTime` is after `startTime`, and both are UTC and end in `Z` |
| `time_range_too_wide` | Over 100 days (90 for prompt executions). Split the window into chunks |
| `end_time_too_recent` | Crawler reports can't include today. End at today `00:00:00.000Z` |
| `conflicting_scope_filters` | You sent `promptId` and `topicId` together. Send one |
| `unsupported_bot_provider` | Pass providers as an array of slugs, never a comma-joined string |
| `aeo_input_validation`, malformed id | Re-read the id from the list call that produced it |
| 429 with `Retry-After` | Wait the stated time and retry once. Run event and time-on-page reports one at a time |
| Optimize window outside an interval | Interval bounds are exact instants. Copy them as returned rather than rounding to the day |

If a retry still fails with something not covered here, use the "Webflow didn't respond" line and stop. Don't loop.

## Best Practices

- Check availability once per conversation and reuse the result. Don't re-probe for every question.
- Treat zeros as answers. "No AI crawler visits in the last 7 days" is useful information.
- Separate the two AEO halves. A site can have crawler data and no prompt tracking.
- Keep the person's attention on their site, not on Webflow's packaging. One line about plans is enough.
