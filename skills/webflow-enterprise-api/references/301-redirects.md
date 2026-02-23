---
name: "301 Redirects"
description: "Manage 301 redirect rules for a site: list, create, update, and delete redirect rules with source and target URL paths."
tags: [redirects, 301, site-configuration, seo, routing, enterprise, create, update, delete]
---

# 301 Redirects

Manage 301 redirect rules configured for a site.

## Table of Contents

- [List Redirects](#list-redirects)
- [Create Redirect](#create-redirect)
- [Update Redirect](#update-redirect)
- [Delete Redirect](#delete-redirect)
- [Error Responses](#error-responses)
- [Best Practices](#best-practices)

---

## List Redirects

```
GET https://api.webflow.com/v2/sites/{site_id}/redirects
```

**Required scope:** `sites:read`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |

### Response (200)

Returns an object with `redirects` (array) and `pagination` (`limit`, `offset`, `total`).

#### Redirect Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | The ID of the specific redirect rule |
| `fromUrl` | string | The source URL path that will be redirected |
| `toUrl` | string | The target URL path where the user or client will be redirected |

#### Pagination Object

| Field | Type | Description |
|-------|------|-------------|
| `limit` | integer | The limit used for pagination |
| `offset` | integer | The offset used for pagination |
| `total` | integer | The total number of records |

### SDK Examples

#### Python

```python
from webflow import Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.redirects.list(site_id="580e63e98c9a982ac9b8b741")
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.redirects.list("580e63e98c9a982ac9b8b741");
```

---

## Create Redirect

```
POST https://api.webflow.com/v2/sites/{site_id}/redirects
```

**Required scope:** `sites:write`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | No | The ID of the specific redirect rule |
| `fromUrl` | string | No | The source URL path that will be redirected |
| `toUrl` | string | No | The target URL path where the user or client will be redirected |

### Response (200)

Returns the created redirect object with `id`, `fromUrl`, and `toUrl`.

### SDK Examples

#### Python

```python
from webflow import Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.redirects.create(
    site_id="580e63e98c9a982ac9b8b741",
    id="42e1a2b7aa1a13f768a0042a",
    from_url="/mostly-harmless",
    to_url="/earth",
)
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.redirects.create("580e63e98c9a982ac9b8b741", {
  id: "42e1a2b7aa1a13f768a0042a",
  fromUrl: "/mostly-harmless",
  toUrl: "/earth",
});
```

---

## Update Redirect

```
PATCH https://api.webflow.com/v2/sites/{site_id}/redirects/{redirect_id}
```

**Required scope:** `sites:write`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |
| `redirect_id` | string | Yes | Unique identifier for a site redirect |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | No | The ID of the specific redirect rule |
| `fromUrl` | string | No | The source URL path that will be redirected |
| `toUrl` | string | No | The target URL path where the user or client will be redirected |

### Response (200)

Returns the updated redirect object with `id`, `fromUrl`, and `toUrl`.

### SDK Examples

#### Python

```python
from webflow import Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.redirects.update(
    site_id="580e63e98c9a982ac9b8b741",
    redirect_id="66c4cb9a20cac35ed19500e6",
    id="42e1a2b7aa1a13f768a0042a",
    from_url="/mostly-harmless",
    to_url="/earth",
)
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.redirects.update("580e63e98c9a982ac9b8b741", "66c4cb9a20cac35ed19500e6", {
  id: "42e1a2b7aa1a13f768a0042a",
  fromUrl: "/mostly-harmless",
  toUrl: "/earth",
});
```

---

## Delete Redirect

```
DELETE https://api.webflow.com/v2/sites/{site_id}/redirects/{redirect_id}
```

**Required scope:** `sites:write`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |
| `redirect_id` | string | Yes | Unique identifier for a site redirect |

### Response (200)

Returns the remaining redirects list with `redirects` (array) and `pagination` (`limit`, `offset`, `total`).

### SDK Examples

#### Python

```python
from webflow import Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.redirects.delete(
    site_id="580e63e98c9a982ac9b8b741",
    redirect_id="66c4cb9a20cac35ed19500e6",
)
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.redirects.delete(
  "580e63e98c9a982ac9b8b741",
  "66c4cb9a20cac35ed19500e6"
);
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

- Audit redirects regularly to identify redirect chains (A -> B -> C) that hurt SEO and page load
- Use the PATCH endpoint to update existing redirects instead of deleting and re-creating them
- Use pagination when listing redirects for sites with many rules
- Cross-reference `fromUrl` paths with your sitemap to ensure old pages are properly redirected
- Clean up stale redirects by deleting rules that are no longer needed
