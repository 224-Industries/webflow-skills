---
name: "Webhook API Reference"
description: "Complete CRUD reference for Webflow's Webhook REST API v2 endpoints: list, get, create, and delete webhooks, including authentication, request/response schemas, filters, pagination, and error codes."
tags: [api, rest, v2, endpoints, create, list, get, delete, authentication, oauth, bearer-token, scopes, filter, pagination, errors, rate-limits]
---

# Webhook API Reference

Base URL: `https://api.webflow.com/v2`

All webhook endpoints require a bearer token from a Data Client App. Authentication uses `Authorization: Bearer <token>`.

## Endpoints Overview

| Method | Endpoint | Scope | Description |
|--------|----------|-------|-------------|
| `GET` | `/sites/{site_id}/webhooks` | `sites:read` | List all webhooks for a site |
| `GET` | `/webhooks/{webhook_id}` | `sites:read` | Get a specific webhook |
| `POST` | `/sites/{site_id}/webhooks` | `sites:write` | Create a new webhook |
| `DELETE` | `/webhooks/{webhook_id}` | `sites:read` | Remove a webhook |

---

## Webhook Object

All endpoints return or accept the same webhook object shape:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the webhook registration (read-only) |
| `triggerType` | enum | The event type — see [Event Types](event-types.md) for all 14 values |
| `url` | string | Destination URL for webhook payloads |
| `workspaceId` | string | Workspace the webhook is registered in (read-only) |
| `siteId` | string | Site the webhook is registered for (read-only) |
| `filter` | object \| null | Form filter — only supported for `form_submission` trigger type |
| `lastTriggered` | string \| null | ISO8601 timestamp of last trigger (read-only) |
| `createdOn` | string \| null | ISO8601 timestamp of creation (read-only) |

### Filter Object

Only supported for `form_submission` webhooks:

```json
{
  "filter": {
    "name": "contact-form"
  }
}
```

---

## List Webhooks

List all app-created webhooks registered for a site.

```
GET /v2/sites/{site_id}/webhooks
```

**Required Scope:** `sites:read`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for the site |

**Response (200):**

```json
{
  "webhooks": [
    {
      "id": "582266e0cd48de0f0e3c6d8b",
      "triggerType": "form_submission",
      "url": "https://your-app.com/webhooks/webflow",
      "workspaceId": "4f4e46fd476ea8c507000001",
      "siteId": "562ac0395358780a1f5e6fbd",
      "filter": {},
      "lastTriggered": "2023-02-08T23:59:28.572Z",
      "createdOn": "2022-11-08T23:59:28.572Z"
    }
  ],
  "pagination": {
    "limit": 100,
    "offset": 0,
    "total": 1
  }
}
```

**cURL:**

```bash
curl -X GET "https://api.webflow.com/v2/sites/{site_id}/webhooks" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Get Webhook

Get a specific webhook instance by ID.

```
GET /v2/webhooks/{webhook_id}
```

**Required Scope:** `sites:read`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `webhook_id` | string | Yes | Unique identifier for the webhook |

**Response (200):**

```json
{
  "id": "582266e0cd48de0f0e3c6d8b",
  "triggerType": "form_submission",
  "url": "https://your-app.com/webhooks/webflow",
  "workspaceId": "4f4e46fd476ea8c507000001",
  "siteId": "562ac0395358780a1f5e6fbd",
  "filter": {},
  "lastTriggered": "2023-02-08T23:59:28.572Z",
  "createdOn": "2022-11-08T23:59:28.572Z"
}
```

**cURL:**

```bash
curl -X GET "https://api.webflow.com/v2/webhooks/{webhook_id}" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Create Webhook

Register a new webhook for a site. Limited to 75 registrations per `triggerType` per site.

```
POST /v2/sites/{site_id}/webhooks
```

**Required Scope:** `sites:write`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for the site |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `triggerType` | enum | Yes | The event type to listen for |
| `url` | string | Yes | Destination URL for payloads |
| `filter` | object | No | Form name filter (only for `form_submission`) |

**Request:**

```json
{
  "triggerType": "form_submission",
  "url": "https://your-app.com/webhooks/webflow",
  "filter": {
    "name": "contact-form"
  }
}
```

**Response (201):**

```json
{
  "id": "582266e0cd48de0f0e3c6d8b",
  "triggerType": "form_submission",
  "url": "https://your-app.com/webhooks/webflow",
  "workspaceId": "4f4e46fd476ea8c507000001",
  "siteId": "562ac0395358780a1f5e6fbd",
  "filter": { "name": "contact-form" },
  "lastTriggered": null,
  "createdOn": "2022-11-08T23:59:28.572Z"
}
```

> **Webhook secrets (after April 2025):** When creating webhooks via the API, the response may include a `secret` field (`whsec_xxxxx`). Save this — it's your signing key for signature verification. See [Verification](verification.md).

**cURL:**

```bash
curl -X POST "https://api.webflow.com/v2/sites/{site_id}/webhooks" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "triggerType": "form_submission",
    "url": "https://your-app.com/webhooks/webflow"
  }'
```

---

## Remove Webhook

Delete a webhook registration.

```
DELETE /v2/webhooks/{webhook_id}
```

**Required Scope:** `sites:read`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `webhook_id` | string | Yes | Unique identifier for the webhook |

**Response:** `204 No Content`

**cURL:**

```bash
curl -X DELETE "https://api.webflow.com/v2/webhooks/{webhook_id}" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Error Codes

All endpoints share the same error responses:

| Status | Error | Description |
|--------|-------|-------------|
| `400` | Bad Request | Invalid request body or parameters |
| `401` | Unauthorized | Missing or invalid bearer token |
| `404` | Not Found | Webhook or site not found |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Webflow server error |

---

## Required Scopes by Trigger Type

Creating a webhook requires `sites:write`, but the events themselves require specific read scopes to be configured on your app:

| Trigger Type | Required App Scope |
|--------------|--------------------|
| `form_submission` | `forms:read` |
| `site_publish` | `sites:read` |
| `page_*` events | `pages:read` |
| `ecomm_*` events | `ecommerce:read` |
| `collection_item_*` events | `cms:read` |
| `comment_created` | `comments:read` |