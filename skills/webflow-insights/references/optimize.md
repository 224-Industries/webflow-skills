---
name: "Reading Webflow Optimize"
description: "Finding a site's tests, picking a valid report window, and reading A/B test, AI-optimised and personalisation results without calling a winner too early."
tags: [optimize, ab-test, experiments, personalisation, ai-optimize, lift, statistical-significance, winner, variations, segments, intervals]
---

# Reading Webflow Optimize

Optimize runs A/B tests, AI-optimised tests and personalisation on a Webflow site. Through the MCP it's read-only: you can see what exists and how it's performing, but you can't create, edit, start or stop anything. Webflow says agent editing is in development. Until it arrives, point people to Optimize in their Webflow dashboard for changes.

## Table of Contents

- [The call sequence](#the-call-sequence)
- [Intervals and report windows](#intervals-and-report-windows)
- [The three kinds of optimisation](#the-three-kinds-of-optimisation)
- [Goals](#goals)
- [Segments and filters](#segments-and-filters)
- [Calling a result](#calling-a-result)
- [Best Practices](#best-practices)

## The call sequence

1. `list_optimize_resources` gives an `optimizeId` for each Optimize resource and the site it belongs to. Pick the one for this site.
2. `list_optimizations` with that `optimizeId`. It defaults to `live` and `draft`. Add `off` and `archived` when the person asks about past tests, or before saying there have never been any.
3. Each optimisation lists its **intervals**, oldest first. An interval with no end is still running.
4. `get_optimization_summary` for the headline result over a window inside one interval.
5. `get_optimization_trend` to see how the result moved over time.
6. `get_optimization_audience_insights` to split the result by one dimension, such as device or traffic source.

## Intervals and report windows

- An optimisation's history is split into intervals, and editing a test starts a new one. **Every report window has to sit inside a single interval.** Never stitch intervals together, because they measured different things.
- **Interval bounds are exact instants.** Copy `intervalStart` and `intervalEnd` as returned. Rounding to the start or end of a day puts the window outside the interval, and the call fails.
- For a running interval, use the current time as the end.
- **With no dates given,** report on the latest interval that's longer than an hour, start to end (or now). Shorter intervals come from quick successive edits and hold too little data to mean anything.
- **Trends:** use weekly buckets for windows of 28 days or more, so the line has at least four points. Use daily buckets for shorter windows.

## The three kinds of optimisation

`optimizationType` decides what the comparison means. Read it before saying anything about winners.

| Type | What it returns | How to read it |
|---|---|---|
| `test` (A/B test) | Per variation: sessions, users, conversions, `conversionRate`, `lift` against the base variation, `statisticalSignificance` (0 to 1), `isWinner` | `isWinner` is true only when significance is at least 0.95 and lift is above zero. Lift is a fraction: 0.19 means 19% better than the base |
| `aiOptimize` (AI-optimised) | Per variation: the usual counts plus `strength`, the probability (0 to 1) that the variation beats the base | Strength isn't significance. The system shifts traffic towards stronger variations as it learns, so the split isn't even and conversion rates aren't a fair head-to-head. Report strength as "an 82% chance of beating the original" |
| `personalize` (personalisation) | Per variation counts and conversion rates, with no comparison | There's no control, so there's no winner to call. Report how each audience's version is doing, and don't rank them as if they competed |

## Goals

- Reports default to the optimisation's first primary goal. The response names the goal it used, so name it in the answer.
- To report on a different goal, get its id from `list_optimization_goals` for the same window, or from the optimisation's `currentGoals`.
- Goals change over time. An interval's goals are the ones it ran with, which may differ from `currentGoals` today.
- For value goals (revenue and similar), lift is measured on value, not conversion count. Say which.

## Segments and filters

- Get valid dimension ids from `list_optimization_dimensions` for the same window. `deviceType`, `trafficSource` and custom attributes like `customAttribute:planType` are typical.
- Filter values are **raw codes, not labels**. Get them from `list_dimension_values`. Mobile is a code like `P`, not the word "mobile". This differs from Analyze filters.
- Filters take `in` and `nin` only. Several keys combine with AND.
- The bare `urlParameter` dimension is rejected. Use a listed `urlParameter:<name>` id.

## Calling a result

1. **No winner below 0.95 significance.** Give the current lift as a direction ("leaning towards B, about 6% better so far"), say how long it's run, and say it isn't settled yet.
2. **Be cautious with few conversions.** When a variation has only a handful of conversions, even a high significance score can flip. Give the counts alongside the percentages.
3. **A segment result is a lead, not proof.** Splitting by many segments means one will look like a winner by chance. Describe a strong segment as worth testing on its own, not as a finding.
4. **A losing variation is still a result.** "The new headline did worse, down 11%" is useful. Say it plainly.
5. **Don't recommend shipping a variation unless `isWinner` is true** for an A/B test, or strength is high and stable over several weeks of trend for an AI-optimised test. Even then, suggest it rather than state it, and say what it's based on.

## Best Practices

- Name the test, its type, its goal and the window in the first lines of the answer.
- Show each variation's conversions as counts beside the rate.
- Check the trend before quoting a summary. A result that has bounced around for weeks is weaker than one that has held steady.
- Never combine intervals or compare variations across different goals.
- Point edits to the Webflow dashboard. The MCP can't change a test.
