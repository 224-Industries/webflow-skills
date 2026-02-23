---
name: "Workspace Management"
description: "Create, update, delete, and get site plans within a workspace: site creation with templates and folder placement, renaming, moving, deletion, and hosting plan details."
tags: [workspace-management, create-site, update-site, delete-site, get-site-plan, workspace, sites, templates, folders, hosting-plan, enterprise]
---

# Workspace Management

Create, update, delete sites, and get site plans within an Enterprise workspace.

## Table of Contents

- [Create Site](#create-site)
- [Update Site](#update-site)
- [Delete Site](#delete-site)
- [Get Site Plan](#get-site-plan)
- [Site Response Object](#site-response-object)
- [Error Responses](#error-responses)
- [Best Practices](#best-practices)

---

## Create Site

```
POST https://api.webflow.com/v2/workspaces/{workspace_id}/sites
```

**Required scope:** `workspace:write`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | string | Yes | Unique identifier for a Workspace |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | The name of the site |
| `templateName` | string | No | Workspace or marketplace template to use |
| `parentFolderId` | string or null | No | ID of parent folder for the site |

### Response (201)

Returns the created site object. See Site Response Object below.

### SDK Examples

#### Python

```python
from webflow import Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.create(
    workspace_id="580e63e98c9a982ac9b8b741",
    name="The Hitchhiker's Guide to the Galaxy",
)
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.create("580e63e98c9a982ac9b8b741", {
  name: "The Hitchhiker's Guide to the Galaxy",
});
```

---

## Update Site

```
PATCH https://api.webflow.com/v2/sites/{site_id}
```

**Required scope:** `sites:write`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | The name of the site |
| `parentFolderId` | string or null | No | The parent folder ID of the site (or `null` to move to root) |

### Response (200)

Returns the updated site object. See Site Response Object below.

### SDK Examples

#### Python

```python
from webflow import Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.update(
    site_id="580e63e98c9a982ac9b8b741",
    name="Renamed Site",
)
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.update("580e63e98c9a982ac9b8b741", {
  name: "Renamed Site",
});
```

---

## Delete Site

```
DELETE https://api.webflow.com/v2/sites/{site_id}
```

**Required scope:** `sites:write`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |

### Response (204)

No content returned on success.

### SDK Examples

#### Python

```python
from webflow import Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.delete(site_id="580e63e98c9a982ac9b8b741")
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.delete("580e63e98c9a982ac9b8b741");
```

---

## Get Site Plan

```
GET https://api.webflow.com/v2/sites/{site_id}/plan
```

**Required scope:** `sites:read`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |

### Response (200)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (enum) | ID of the hosting plan |
| `name` | string (enum) | Name of the hosting plan |
| `pricingInfo` | string | URL for Webflow hosting plan pricing info |

#### Plan ID Values

| ID |
|----|
| `hosting-basic-v3` |
| `hosting-cms-v3` |
| `hosting-business-v3` |
| `hosting-ecommerce-standard-v2` |
| `hosting-ecommerce-plus-v2` |
| `hosting-ecommerce-advanced-v2` |
| `hosting-basic-v4` |
| `hosting-cms-v4` |
| `hosting-business-v4` |
| `hosting-ecommerce-standard-v3` |
| `hosting-ecommerce-plus-v3` |
| `hosting-ecommerce-advanced-v3` |

#### Plan Name Values

| Name |
|------|
| `Basic Hosting` |
| `CMS Hosting` |
| `Business Hosting` |
| `ECommerce Standard Hosting` |
| `ECommerce Plus Hosting` |
| `ECommerce Advanced Hosting` |

### SDK Examples

#### Python

```python
from webflow import Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.plans.get_site_plan(site_id="580e63e98c9a982ac9b8b741")
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.plans.getSitePlan("580e63e98c9a982ac9b8b741");
```

---

## Site Response Object

Returned by Create and Update endpoints:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the Site |
| `workspaceId` | string | Unique identifier for the Workspace |
| `displayName` | string | Name given to the Site |
| `shortName` | string | Slugified version of name |
| `createdOn` | string (date-time) | Date the Site was created |
| `lastPublished` | string (date-time) | Date the Site was last published |
| `lastUpdated` | string (date-time) | Date the Site was last updated |
| `previewUrl` | string (URI) | URL of a generated image for the given Site |
| `timeZone` | string | Site timezone set under Site Settings |
| `parentFolderId` | string or null | The ID of the parent folder the Site exists in |
| `customDomains` | array | List of custom domain objects |
| `locales` | object | Locale configuration object |
| `dataCollectionEnabled` | boolean | Indicates if data collection is enabled for the site |
| `dataCollectionType` | string | `"always"`, `"optOut"`, or `"disabled"` |

### Custom Domain Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the Domain |
| `url` | string | The registered Domain name |
| `lastPublished` | string (date-time) or null | The date the custom domain was last published to |

### Locales Object

| Field | Type | Description |
|-------|------|-------------|
| `primary` | object | The primary locale for the site |
| `secondary` | array of objects | List of secondary locales available |

#### Locale Item Fields (shared by primary and secondary)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | The unique identifier for the locale |
| `cmsLocaleId` | string | A CMS-specific identifier for the locale |
| `enabled` | boolean | Indicates if the locale is enabled |
| `displayName` | string | The display name of the locale, typically in English |
| `displayImageId` | string or null | An optional ID for an image associated with the locale |
| `redirect` | boolean | Determines if requests should redirect to the locale's subdirectory |
| `subdirectory` | string | The subdirectory path for the locale, used in URLs |
| `tag` | string | A tag or code representing the locale (e.g., `en-US`) |

## Error Responses

| Code | Description |
|------|-------------|
| 400 | Request body was incorrectly formatted |
| 401 | Provided access token is invalid or does not have access to requested resource |
| 403 | Forbidden request |
| 404 | Requested resource not found |
| 429 | Rate limit reached — check `X-RateLimit-Remaining` header |
| 500 | Server error — try again later |

## Best Practices

- Use `templateName` to create sites from standardized workspace templates for consistency
- Use `parentFolderId` to organize sites into folders within the workspace
- Store the returned `id` for subsequent API operations on the created site
- Use PATCH to rename or move sites between folders without affecting site content
- Use Get Site Plan to verify the hosting tier before making plan-dependent API calls
- Deletion is permanent — confirm the site ID before calling DELETE
