---
name: "Workspace Audit Logs"
description: "GET workspace audit logs: retrieve login/logout, role changes, membership events, and invitation lifecycle records. Includes event types, subtypes, payloads, and filtering options."
tags: [audit-logs, workspace, user-access, custom-role, membership, invitation, security, compliance, enterprise]
---

# Workspace Audit Logs

Retrieve audit log records for a workspace. Tracks who performed actions, when, and via what method.

## Table of Contents

- [Get Workspace Audit Logs](#get-workspace-audit-logs)
- [Error Responses](#error-responses)
- [Best Practices](#best-practices)

---

## Get Workspace Audit Logs

```
GET https://api.webflow.com/v2/workspaces/{workspace_id_or_slug}/audit_logs
```

**Required scope:** `workspace_activity:read`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id_or_slug` | string | Yes | Unique identifier or slug for the workspace |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Max records returned (max: 100) |
| `offset` | integer | No | Pagination offset |
| `sortOrder` | string | No | `"asc"` or `"desc"` |
| `eventType` | string | No | Filter by event type (see Event Types below) |
| `from` | string (date-time) | No | Start date filter (ISO 8601) |
| `to` | string (date-time) | No | End date filter (ISO 8601) |

### Response (200)

Returns an object with `items` (array of audit log entries) and `pagination` (`limit`, `offset`, `total`).

#### Common Fields

All audit log entries share these fields:

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | string (date-time) | When the event occurred |
| `actor` | object | `{ id, email }` — who performed the action |
| `workspace` | object | `{ id, slug }` — the workspace |
| `eventType` | string | Event category |
| `eventSubType` | string | Specific event within the category |
| `payload` | object | Event-specific data (varies by type) |

### Event Types

#### `user_access`

Login and logout tracking.

**Subtypes:** `login`, `logout`

| Payload Field | Type | Description |
|---------------|------|-------------|
| `method` | string | `"dashboard"`, `"sso"`, `"api"`, or `"google"` |
| `location` | string | Geolocation derived from IP |
| `ipAddress` | string | Client IP address |

#### `custom_role`

Role creation, modification, and deletion.

**Subtypes:** `role_created`, `role_updated`, `role_deleted`

| Payload Field | Type | Description |
|---------------|------|-------------|
| `roleName` | string | Current role name |
| `previousRoleName` | string | Previous role name (for updates) |

#### `workspace_membership`

Users joining, leaving, or changing roles at the workspace level.

**Subtypes:** `user_added`, `user_removed`, `user_role_updated`

| Payload Field | Type | Description |
|---------------|------|-------------|
| `targetUser` | object | `{ id, email }` |
| `method` | string | `"sso"`, `"dashboard"`, `"admin"`, or `"access_request"` |
| `userType` | string | `"member"`, `"guest"`, `"reviewer"`, or `"client"` |
| `roleName` | string | Assigned role |
| `previousRoleName` | string | Previous role (for updates) |

#### `site_membership`

Site-level access tracking, including granular resource permissions.

**Subtypes:** `user_added`, `user_removed`, `user_role_updated`, `user_granular_access_updated`

| Payload Field | Type | Description |
|---------------|------|-------------|
| `site` | object | `{ id, slug }` |
| `targetUser` | object | `{ id, email }` |
| `method` | string | `"sso"`, `"invite"`, `"scim"`, `"dashboard"`, `"admin"`, or `"access_request"` |
| `userType` | string | `"member"`, `"guest"`, `"reviewer"`, or `"client"` |
| `roleName` | string | Assigned role |
| `previousRoleName` | string | Previous role |
| `granularAccess` | object | `{ id, name, type: "cms", restricted: boolean }` |

#### `workspace_invitation`

Full invitation lifecycle monitoring.

**Subtypes:** `invite_sent`, `invite_accepted`, `invite_updated`, `invite_canceled`, `invite_declined`, `access_request_accepted`

| Payload Field | Type | Description |
|---------------|------|-------------|
| `targetUser` | object | `{ id, email }` |
| `method` | string | `"sso"`, `"dashboard"`, or `"admin"` |
| `userType` | string | `"member"`, `"guest"`, `"reviewer"`, or `"client"` |
| `roleName` | string | Role in the invitation |
| `previousRoleName` | string | Previous role (for updates) |
| `targetUsers` | array | Array of `{ id, email }` (for bulk operations) |

### SDK Examples

#### Python

```python
import datetime
from webflow import Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.workspaces.audit_logs.get_workspace_audit_logs(
    workspace_id_or_slug="hitchhikers-workspace",
    limit=100,
    offset=0,
    sort_order="asc",
    event_type="user_access",
    from_=datetime.datetime.fromisoformat("2025-06-22T16:00:31+00:00"),
    to=datetime.datetime.fromisoformat("2025-07-22T16:00:31+00:00"),
)
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.workspaces.auditLogs.getWorkspaceAuditLogs(
  "hitchhikers-workspace",
  {
    limit: 100,
    offset: 0,
    sortOrder: "asc",
    eventType: "user_access",
    from: new Date("2025-06-22T16:00:31.000Z"),
    to: new Date("2025-07-22T16:00:31.000Z"),
  }
);
```

#### HTTP

```
GET https://api.webflow.com/v2/workspaces/{workspace_id_or_slug}/audit_logs?limit=100&offset=0&eventType=user_access&from=2025-06-22T16:00:31Z&to=2025-07-22T16:00:31Z
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

- Use `eventType` filtering to reduce response size when querying specific event categories
- Use `from` and `to` date filters for time-bounded queries instead of paginating through all records
- Store audit logs externally for long-term retention and compliance requirements
- Monitor `user_access` events for security alerting on suspicious login patterns
