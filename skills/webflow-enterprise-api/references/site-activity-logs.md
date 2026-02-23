---
name: "Site Activity Logs"
description: "GET site activity logs: retrieve design changes, page operations, CMS edits, publishing events, locale changes, branch operations, and library events for a site."
tags: [site-activity, activity-logs, events, publishing, cms, pages, branches, locales, libraries, enterprise]
---

# Site Activity Logs

Retrieve activity log records for a specific site. Tracks design changes, page operations, CMS edits, publishing events, and more.

## Table of Contents

- [List Site Activity Logs](#list-site-activity-logs)
- [Error Responses](#error-responses)
- [Best Practices](#best-practices)

---

## List Site Activity Logs

```
GET https://api.webflow.com/v2/sites/{site_id}/activity_logs
```

**Required scope:** `site_activity:read`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Max records returned (max: 100) |
| `offset` | integer | No | Pagination offset |

### Response (200)

Returns an object with `items` (array of activity log entries) and `pagination` (`limit`, `offset`, `total`).

#### Activity Log Entry

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique entry identifier |
| `createdOn` | string (date-time) | When the event occurred |
| `lastUpdated` | string (date-time) | When the entry was last updated |
| `event` | string | Event type (see below) |
| `resourceOperation` | string | Operation type (see below) |
| `user` | object or null | `{ id, displayName }` — who performed the action |
| `resourceId` | string or null | ID of the affected resource |
| `resourceName` | string or null | Name of the affected resource |
| `newValue` | string or null | New value after the change |
| `previousValue` | string or null | Previous value before the change |
| `payload` | object or null | Additional event-specific data |

#### Event Types

**Design & content:**
`styles_modified`, `ix2_modified_on_page`, `ix2_modified_on_component`, `ix2_modified_on_class`, `page_dom_modified`, `symbols_modified`, `variable_modified`, `variables_modified`

**Pages:**
`page_created`, `page_deleted`, `page_duplicated`, `page_renamed`, `page_settings_modified`, `page_settings_custom_code_modified`, `page_custom_code_modified`

**CMS:**
`cms_item`, `cms_collection`

**Publishing:**
`site_published`, `site_unpublished`

**Custom code:**
`site_custom_code_modified`

**Backups:**
`backup_created`, `backup_restored`

**Locales:**
`locale_added`, `locale_removed`, `locale_enabled`, `locale_disabled`, `locale_display_name_updated`, `locale_subdirectory_updated`, `locale_tag_updated`, `secondary_locale_page_content_modified`

**Branches:**
`branch_created`, `branch_deleted`, `branch_merged`, `branch_review_created`, `branch_review_approved`, `branch_review_canceled`

**Libraries:**
`library_shared`, `library_unshared`, `library_installed`, `library_uninstalled`, `library_update_shared`, `library_update_accepted`

#### Resource Operations

`CREATED`, `MODIFIED`, `PUBLISHED`, `UNPUBLISHED`, `DELETED`, `GROUP_REORDERED`, `GROUP_CREATED`, `GROUP_DELETED`, `REORDERED`

### SDK Examples

#### Python

```python
from webflow import Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.activity_logs.list(
    site_id="580e63e98c9a982ac9b8b741",
    limit=100,
    offset=0,
)
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.activityLogs.list("580e63e98c9a982ac9b8b741", {
  limit: 100,
  offset: 0,
});
```

#### HTTP

```
GET https://api.webflow.com/v2/sites/{site_id}/activity_logs?limit=100&offset=0
Authorization: Bearer <token>
```

---

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

- Use pagination (`limit` and `offset`) to iterate through large activity histories
- Monitor `site_published` and `site_unpublished` events for deployment tracking
- Track `branch_merged` and `branch_review_approved` events for workflow auditing
- Use `resourceOperation` to filter for specific change types (e.g., only `CREATED` or `DELETED`)
