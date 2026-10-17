---
name: "Reading Webflow Analyze"
description: "Date windows, fair comparisons, which Analyze report answers which question, and how to read traffic, pages, sources, goals, engagement, scroll depth and page flow without overstating them."
tags: [analyze, traffic, sessions, users, pageviews, top-pages, goals, conversions, events, scroll-depth, page-flow, time-zone, comparisons]
---

# Reading Webflow Analyze

Analyze is Webflow's built-in site analytics. Through the MCP it answers traffic, page, source, goal and engagement questions for one site at a time. Webflow's own `get_query_guide` action covers the mechanics. This file covers the judgement around them: picking fair windows, choosing the right report, and reading the numbers honestly.

## Table of Contents

- [Date windows](#date-windows)
- [Comparing two periods](#comparing-two-periods)
- [Which report answers which question](#which-report-answers-which-question)
- [Metrics in plain words](#metrics-in-plain-words)
- [Pages and CMS items](#pages-and-cms-items)
- [Goals and conversion rate](#goals-and-conversion-rate)
- [Engagement: events, time, scroll and flow](#engagement-events-time-scroll-and-flow)
- [Reading the numbers honestly](#reading-the-numbers-honestly)
- [Best Practices](#best-practices)

## Date windows

- **Time zone.** Use the site's `timeZone` from `data_sites_tool > get_site` unless the person names another. Work out every date in that zone, then convert to UTC instants ending in `Z`. Pass the same zone as `bucketTimeZone` on bucketed reports.
- **Window shape.** Start date at `00:00:00.000`, end date at `23:59:59.999`, both in the site's zone. For a site in `Australia/Brisbane` (UTC+10), 1 September to 30 September is `2026-08-31T14:00:00.000Z` to `2026-09-30T13:59:59.999Z`.
- **Plain-language periods.** "Last 7 days" is today minus 6 through today. "Last week" is the most recent complete Sunday to Saturday. "This month" is the 1st to today. "Last month" is the previous complete month.
- **Limits.** One call covers at most 100 days, and data starts on 09-04-2025. Nothing before that date exists.
- **Today is partial.** If the window includes today, say so. For comparisons, end on yesterday so both sides are complete days.
- **Always state the window** you used, in the site's local dates, in the answer.

## Comparing two periods

A comparison is only fair when both sides are built the same way.

| Asked for | Compare with |
|---|---|
| This week | The same days of last week, so Monday meets Monday |
| Last 7 or 28 days | The 7 or 28 days immediately before, same length |
| Last month | The month before it. Note when the two months have different numbers of days, and compare daily averages if the gap matters |
| Year on year | Only if the earlier period is on or after 09-04-2025 |

Longer than 100 days: split into chunks and add up sessions and pageviews across them. **Don't add users across chunks.** Users are counted once per window, so one person visiting in two chunks would be counted twice. Say users aren't available for the full span, or report them per chunk.

Report changes as both numbers and a percentage, and say what the percentage is from: "Sessions rose from 412 to 506, up 23%."

### Getting a period total

`get_traffic_report` returns a **daily series, not a total**. For a period total of sessions or pageviews, add up the daily counts. **Don't add up daily users**: one person visiting on three days appears in three days' counts. Report visits and pageviews for the period, and give visitors as a daily average if they're needed. To sanity-check a session total, the `trafficSource` rows from `get_top_dimensions_report` over the same window should add up to roughly the same number.

### Check for automated traffic before comparing

Bots and scanners show up in Analyze as real-looking visits, and one bad day can swamp a small site's month. Before comparing two periods, look at the daily series for a spike and check it with the same report filtered to just those days. Signs it's automated:

- One to three days far above the usual daily level, then back to normal
- Sessions roughly equal to visitors: everyone came once
- Most of it from one country, or with no referrer (Direct)
- Landing mostly on the 404 page and the home page

If those line up, report the comparison both ways ("visits rose 58%, or about 20% leaving out two days of what looks like automated traffic on 20 and 21 September") and label it as likely, not certain. Analyze doesn't flag bots itself.

## Which report answers which question

| Question | Report | Notes |
|---|---|---|
| How much traffic, and the trend | `get_traffic_report` | Needs `metricScope` and `bucketTimeZone` |
| Which pages get the most visits | `get_top_pages_report` | `sortBy` session, user or pageview. Add `timeseries` for a daily line per page |
| Where visitors come from | `get_top_dimensions_report` with `trafficSource` or `referrer` | Sessions or users only, no pageviews |
| Which countries, devices, browsers | `get_top_dimensions_report` | |
| Which campaigns | `get_top_dimensions_report` with `utmCampaign`, `utmSource`, `utmMedium` | |
| What goals are set up | `list_goals` | A catalogue only. Takes no window or filters |
| How a goal performed | `get_goal_performance` | Daily unique conversions for one goal |
| What people click | `get_top_events_report` | Ranked by frequency |
| How long people stay | `get_time_on_page_report` | One number, or a daily or weekly trend |
| How far people scroll | `get_scroll_depth_report` with `get_browser_window_height_report` | See below |
| Where people go before or after a page | `get_page_flow_report` | Needs the anchor `pageId` from `data_pages_tool` |

Filter any report to one page, source, country, device or campaign with the promoted filters (`pagePath`, `trafficSource`, `deviceType` and so on), or use the `filter` object for anything else. To get a valid filter value, run `get_top_dimensions_report` for that dimension first and use a row's `attributeKey`.

### Traffic sources and referrers

- `trafficSource` rows come back with a short code (`attributeKey`, such as `DN`) and a name (`Direct`). Use the name in answers and the code in filters.
- **Direct is a catch-all.** It includes bookmarks, typed addresses, links in apps and email, privacy settings that strip the referrer, and most automated traffic. A large Direct share isn't a finding by itself.
- **The site's own domain appears in the referrer list** when visitors move between pages or subdomains. Leave the site's own domains out when describing where visitors come from.

## Metrics in plain words

| Metric | Say it as |
|---|---|
| Session | A visit. One person can make several |
| User | A distinct visitor in the window |
| Pageview | A page load. One visit can view several pages |
| Time on page | The average time spent, based on sessions, users or pageviews depending on `metricScope`. Name which one you used |

## Pages and CMS items

- **A static page:** get its `publishedPath` from `data_pages_tool`, then filter on `pagePath`.
- **A whole CMS collection, such as all blog posts:** filter on `collectionId` from `data_cms_tool`.
- **One CMS item:** filter on `collectionId` and `itemSlug`, or build its path as the collection page path plus the item slug.
- **CMS items share their template's `pageId`.** In top pages, two blog posts can carry the same `pageId`. Tell them apart by `itemSlug` and title.
- **The 404 page in the top pages list** has two usual causes, and its daily series tells them apart. Filter `get_traffic_report` to the 404 page's `pageId`. A steady trickle across the month points to old URLs or broken links from other sites, and is worth a redirect review. Sharp spikes on a few days point to automated scanning, which isn't something the site owner needs to fix.

## Goals and conversion rate

- `get_goal_performance` returns **unique conversions per day**. Zero conversions comes back as empty data, which is a valid answer, not a failure.
- Analyze doesn't return a conversion rate. When you work one out, divide the goal's conversions by sessions over the same window and filters, and say you calculated it.
- Goals can be clicks, page views, form integrations (HubSpot, Marketo, Shopify) or custom events. Name the goal as Webflow names it.
- The MCP can't tell you which page elements a goal tracks. If asked, describe the goal from `list_goals` and say the elements can't be seen from here.
- If `list_goals` is empty, say no goals are set up and suggest setting up one for the site's main action, such as a form submission or booking. Without a goal there's nothing to measure conversions against.

## Engagement: events, time, scroll and flow

- **Events.** `get_top_events_report` ranks clicks and interactions by count. To find the element behind an event, follow Webflow's `get_resolve_event_element_guide`. Describe the element in plain words ("the 'Book a call' button in the header"), not by id.
- **Rate limits.** Events and time-on-page reports share a concurrency limit. Run them one at a time. On a 429, wait for the `Retry-After` time and retry once.
- **Scroll depth** comes back in pixels at three points: the depth that 75%, 50% and 25% of pageviews reached. Pixels mean little to most people, so divide by the average window height from `get_browser_window_height_report` and express it in screens: "Half of visitors scroll about 2.5 screens down this page." Run both reports with the same filters, ideally per device type, because mobile and desktop screens differ a lot.
- **Page flow.** `get_page_flow_report` with `direction: "previous"` shows where visitors came from on the site before a page, and `"next"` shows where they went after. It's useful for "do people reach the contact page from the services page?"

## Reading the numbers honestly

- **Small numbers swing.** When a page or period has fewer than about 100 sessions, a 40% change can be a handful of visits. Lead with the counts and say the sample is small.
- **One week isn't a trend.** Before calling something a trend, check at least three or four comparable periods with a daily or weekly series.
- **Analyze won't match GA4.** The two tools count differently and handle consent differently. If the person has both, say the numbers will differ and don't try to reconcile them.
- **Correlation isn't cause.** A traffic change near a site update is worth pointing out, labelled as something that happened at the same time, not as the proven cause.
- **Report only fields that came back.** Don't estimate missing values.

## Best Practices

- Resolve the site, its time zone and the window before any report call.
- Put the date window and the comparison window in the answer.
- Use daily series for anything under 60 days, weekly above that.
- Pair top pages with top sources when explaining a change. Together they show both where and why.
- Flag the 404 page, empty goals and zero-conversion goals as fixable, because they usually are.
