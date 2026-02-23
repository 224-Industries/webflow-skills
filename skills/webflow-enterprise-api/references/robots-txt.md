---
name: "Robots.txt"
description: "Manage robots.txt configuration for a site: get, replace, update, and delete crawler rules (user-agent, allows, disallows) and sitemap URL."
tags: [robots-txt, site-configuration, seo, crawlers, sitemap, enterprise, get, put, patch, delete]
---

# Robots.txt

Manage the robots.txt configuration for a site, including crawler rules and sitemap URL.

## Table of Contents

- [Get Robots.txt](#get-robotstxt)
- [Replace Robots.txt](#replace-robotstxt)
- [Update Robots.txt](#update-robotstxt)
- [Delete Robots.txt Rules](#delete-robotstxt-rules)
- [Error Responses](#error-responses)
- [Best Practices](#best-practices)

---

## Get Robots.txt

```
GET https://api.webflow.com/v2/sites/{site_id}/robots_txt
```

**Required scope:** `site_config:read`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |

### Response (200)

| Field | Type | Description |
|-------|------|-------------|
| `rules` | array | List of rules for user agents |
| `sitemap` | string | URL to the sitemap |

#### Rule Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `userAgent` | string | Yes | The user agent the rules apply to |
| `allows` | array of strings | No | List of paths allowed for this user agent |
| `disallows` | array of strings | No | List of paths disallowed for this user agent |

### SDK Examples

#### Python

```python
from webflow import Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.robots_txt.get(site_id="580e63e98c9a982ac9b8b741")
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.robotsTxt.get("580e63e98c9a982ac9b8b741");
```

---

## Replace Robots.txt

```
PUT https://api.webflow.com/v2/sites/{site_id}/robots_txt
```

**Required scope:** `site_config:write`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rules` | array | No | List of rules for user agents |
| `sitemap` | string | No | URL to the sitemap |

Each rule object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `userAgent` | string | Yes | The user agent the rules apply to |
| `allows` | array of strings | No | List of paths allowed for this user agent |
| `disallows` | array of strings | No | List of paths disallowed for this user agent |

### Response (200)

Returns the replaced robots.txt configuration with the same `rules` and `sitemap` structure.

### SDK Examples

#### Python

```python
from webflow import RobotsRulesItem, Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.robots_txt.put(
    site_id="580e63e98c9a982ac9b8b741",
    rules=[
        RobotsRulesItem(
            user_agent="googlebot",
            allows=["/public"],
            disallows=["/vogon-poetry", "/total-perspective-vortex"],
        )
    ],
    sitemap="https://heartofgold.ship/sitemap.xml",
)
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.robotsTxt.put("580e63e98c9a982ac9b8b741", {
  rules: [
    {
      userAgent: "googlebot",
      allows: ["/public"],
      disallows: ["/vogon-poetry", "/total-perspective-vortex"],
    },
  ],
  sitemap: "https://heartofgold.ship/sitemap.xml",
});
```

---

## Update Robots.txt

```
PATCH https://api.webflow.com/v2/sites/{site_id}/robots_txt
```

**Required scope:** `site_config:write`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rules` | array | No | List of rules for user agents |
| `sitemap` | string | No | URL to the sitemap |

Each rule object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `userAgent` | string | Yes | The user agent the rules apply to |
| `allows` | array of strings | No | List of paths allowed for this user agent |
| `disallows` | array of strings | No | List of paths disallowed for this user agent |

### Response (200)

Returns the updated robots.txt configuration with the same `rules` and `sitemap` structure.

### SDK Examples

#### Python

```python
from webflow import RobotsRulesItem, Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.robots_txt.patch(
    site_id="580e63e98c9a982ac9b8b741",
    rules=[
        RobotsRulesItem(
            user_agent="googlebot",
            allows=["/public"],
            disallows=["/vogon-poetry", "/total-perspective-vortex"],
        )
    ],
    sitemap="https://heartofgold.ship/sitemap.xml",
)
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.robotsTxt.patch("580e63e98c9a982ac9b8b741", {
  rules: [
    {
      userAgent: "googlebot",
      allows: ["/public"],
      disallows: ["/vogon-poetry", "/total-perspective-vortex"],
    },
  ],
  sitemap: "https://heartofgold.ship/sitemap.xml",
});
```

---

## Delete Robots.txt Rules

```
DELETE https://api.webflow.com/v2/sites/{site_id}/robots_txt
```

**Required scope:** `site_config:write`

Removes specific rules for a user-agent in the robots.txt file. Providing an empty rule set deletes all rules for that user-agent entirely, making the user-agent's access unrestricted unless other directives apply.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rules` | array | No | List of rules for user agents |
| `sitemap` | string | No | URL to the sitemap |

Each rule object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `userAgent` | string | Yes | The user agent the rules apply to |
| `allows` | array of strings | No | List of paths allowed for this user agent |
| `disallows` | array of strings | No | List of paths disallowed for this user agent |

### Response (200)

Returns the remaining robots.txt configuration with the same `rules` and `sitemap` structure.

### SDK Examples

#### Python

```python
from webflow import RobotsRulesItem, Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.robots_txt.delete(
    site_id="580e63e98c9a982ac9b8b741",
    rules=[
        RobotsRulesItem(
            user_agent="*",
            allows=["/public"],
            disallows=["/bubbles"],
        )
    ],
)
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.robotsTxt.delete("580e63e98c9a982ac9b8b741", {
  rules: [
    {
      userAgent: "*",
      allows: ["/public"],
      disallows: ["/bubbles"],
    },
  ],
});
```

---

## Error Responses

| Code | Description |
|------|-------------|
| 400 | Request body was incorrectly formatted |
| 401 | Provided access token is invalid or does not have access to requested resource |
| 404 | Requested resource not found |
| 429 | Rate limit reached — check `X-RateLimit-Remaining` header |
| 500 | Server error — try again later |

## Best Practices

- Review robots.txt rules before launching a site to ensure important pages are not accidentally blocked
- Verify the `sitemap` URL points to a valid, up-to-date sitemap
- Use specific `userAgent` rules only when you need different crawl behavior for different bots
- Use the GET endpoint to read current rules before replacing with PUT to avoid accidentally overwriting existing configuration
- Use PATCH for partial updates instead of PUT when you only need to modify specific rules
- When deleting rules for a user-agent, be aware that an empty rule set makes that agent's access unrestricted
