---
name: "Reading Webflow AEO Analytics"
description: "The two halves of AEO Analytics (AI crawler traffic and prompt tracking), their different date rules, what visibility and citation rate mean, and why a crawler visit is not a citation."
tags: [aeo, ai-search, llm, crawlers, bot-traffic, prompts, visibility, citations, answer-engines, chatgpt, perplexity, gemini, claude]
---

# Reading Webflow AEO Analytics

AEO Analytics shows how AI systems read a site and how AI answers talk about the brand. It has two halves with different rules, and keeping them apart is most of the work.

| Half | Answers | Reports |
|---|---|---|
| **Crawler traffic** | Which AI crawlers visit, how often, and which pages they read | `get_bot_traffic`, `get_bot_traffic_pages` |
| **Prompt tracking** | What AI answers say when asked the questions the site tracks, and whether they mention or cite the site | `list_prompts`, `list_prompt_executions`, `get_prompt_execution`, `get_visibility`, `get_visibility_breakdown`, `get_citation_rate`, `get_top_cited_domains`, `get_cited_domain_paths`, `get_page_citation_share`, `get_competitor_citations`, `get_citations` |

Both need AEO Analytics on the plan. Prompt tracking also needs the workspace's AI features switched on, so a site can have crawler data and no prompt data. See `availability.md`.

## Table of Contents

- [A crawler visit is not a citation](#a-crawler-visit-is-not-a-citation)
- [Crawler traffic](#crawler-traffic)
- [Prompt tracking](#prompt-tracking)
- [Visibility and citation rate](#visibility-and-citation-rate)
- [Call rules that trip agents up](#call-rules-that-trip-agents-up)
- [Best Practices](#best-practices)

## A crawler visit is not a citation

Webflow says this directly, and it's the most common misreading. A crawler requesting a page shows the page is being read. It doesn't show that any AI answer used it. Never describe crawler counts as "appearing in ChatGPT" or "being cited". Say "OpenAI's crawlers requested this page 340 times".

Citations and mentions only come from the prompt-tracking reports.

## Crawler traffic

- **The window must end no later than today at `00:00:00.000Z` UTC.** Today's crawler data isn't ready yet. "Last 7 days" means end at today `00:00:00.000Z` and start 7 days before. Don't use the end of today.
- At most 100 days per call.
- **Filter by provider** with `botProviders`, an array of slugs: `openai`, `anthropic`, `google`, `perplexity`, `microsoft`, `meta`, `apple`, `amazon`, `bytedance`, `mistral`, `duckduckgo`, `common-crawl`, `ai2`. Never join them into one comma-separated string.
- **Filter by purpose** with `botCategory`. Explain the categories to the person in plain words:

| Category | Roughly means |
|---|---|
| `training` | Collecting pages to train AI models |
| `indexer` | Building a search index that AI answers draw on |
| `agent` | Fetching a page live, on behalf of someone using an AI tool right now |
| `multiple` | A crawler that does more than one of these |

- **Zero is valid.** No crawler visits in a window is an answer, not a fault.

What crawler data is good for:

- Seeing whether the pages that matter (services, pricing, key articles) are being read at all.
- Spotting pages that get heavy crawler attention but little human traffic, or the reverse.
- Checking that a new or updated page has been picked up since it was published.

If an important page gets no crawler visits, worth checking: whether it's linked from the rest of the site, whether it's in the sitemap and the site's llms.txt, and whether robots settings block AI crawlers. Present these as things to check, not as the diagnosis.

## Prompt tracking

- `list_prompts` returns each tracked prompt with its id, text, status and topic (`{id, name}`). Use it to turn "the pricing prompt" into ids. There's no separate topics call.
- `list_prompt_executions` is the history of each prompt being run against each answer engine. `promptId` and `topicId` are optional, but **never send both**. Window up to 90 days (not 100). `limit` is 1 to 25. Rows carry a preview. Add `includeRawResponse: true` to get the full answer text.
- `get_prompt_execution` fetches one run by id, including archived runs, although the full text may have been purged.
- Answer engines are `chat-gpt`, `gemini`, `claude` and `perplexity`. These are the AI products. Don't confuse them with crawler providers like `openai` or `anthropic`, which are the companies' bots.

## Visibility and citation rate

| Measure | Means | Report |
|---|---|---|
| Visibility | How often the brand appears in AI answers to the tracked prompts | `get_visibility` (one score, or a series), `get_visibility_breakdown` (by topic or prompt) |
| Citation rate | How often answers cite the site's own domains as a source | `get_citation_rate` (by topic or prompt) |
| Top cited domains | Which sites AI answers cite most for these prompts, which often shows who the real competition is | `get_top_cited_domains` |
| Page citation share | How much of the citing a single page earns | `get_page_citation_share` |
| Competitor citations | Where configured competitors are cited | `get_competitor_citations` |

- **The server works out the brand, the site's own domains and the competitors.** Never send `brandNames`, `domains` or `competitorDomains`. The site's own domains include every custom domain and the webflow.io address.
- **Don't calculate visibility or citation rate yourself** from answer text. Call the report.
- Visibility can be high while citation rate is low. That means AI tools know the brand but are using other sites as their sources, which is worth saying plainly.
- `get_visibility` takes a single `answerEngine`. The citation reports take `answerEngines` as an array.
- `topicIds` and `promptIds` combine with AND on visibility, citation rate and citations. `get_top_cited_domains`, `get_cited_domain_paths` and `get_competitor_citations` accept `topicIds` only. `get_page_citation_share` takes neither.

## Call rules that trip agents up

- **One bad action fails the whole call.** `data_aeo_tool` checks every action in the array before running any. Send independent reads as separate calls.
- **The two halves have different date rules:** crawler reports end at today's UTC midnight, prompt executions cap at 90 days, and visibility and citation reports cap at 100 days.
- **State the window** in every answer.
- **Report only fields that came back.**

## Best Practices

- Lead with whichever half the site has. Many sites will have crawler data only.
- Pair crawler data with Analyze referrals from AI tools (chatgpt.com, perplexity.ai and similar) for the human side of the picture.
- When citation rate is low, list the top cited domains. They show who the AI tools trust on this topic.
- Use full answer text sparingly. It's long, and a quoted line or two is usually enough to show how the brand is described.
