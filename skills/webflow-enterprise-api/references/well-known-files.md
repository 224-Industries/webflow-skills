---
name: "Well-Known Files"
description: "Upload and delete well-known files for a site: manage files in the .well-known directory for domain verification, app associations, and security policies."
tags: [well-known, site-configuration, domain-verification, app-association, security, enterprise, put, delete]
---

# Well-Known Files

Upload and delete files in the `.well-known` directory of a site. Used for domain verification, app associations (e.g., Apple App Site Association), and security policies.

## Table of Contents

- [Upload File](#upload-file)
- [Delete Files](#delete-files)
- [Error Responses](#error-responses)
- [Best Practices](#best-practices)

---

## Upload File

```
PUT https://api.webflow.com/v2/sites/{site_id}/well_known
```

**Required scope:** `site_config:write`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `fileName` | string | Yes | Name of the file |
| `fileData` | string | Yes | Contents of the file |
| `contentType` | string | No | `"application/json"` (default) or `"text/plain"` |

#### File Restrictions

| Constraint | Limit |
|------------|-------|
| Max file size | 100 KB per file |
| Max file count | 30 files total |
| Allowed extensions | `.txt`, `.json`, `.noext` (or no extension) |

> **Note:** The `.noext` extension strips the extension at upload time. For example, `apple-app-site-association.noext.txt` becomes `apple-app-site-association` in the `.well-known` directory.

### Response (201)

Returns an empty object on success.

### SDK Examples

#### Python

```python
from webflow import Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.well_known.put(
    site_id="580e63e98c9a982ac9b8b741",
    file_name="apple-app-site-association.txt",
    file_data='{"applinks": {"apps": [], "details": []}}',
    content_type="application/json",
)
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.wellKnown.put("580e63e98c9a982ac9b8b741", {
  fileName: "apple-app-site-association.txt",
  fileData: '{"applinks": {"apps": [], "details": []}}',
  contentType: "application/json",
});
```

#### HTTP

```
PUT https://api.webflow.com/v2/sites/{site_id}/well_known
Authorization: Bearer <token>
Content-Type: application/json

{
  "fileName": "apple-app-site-association.txt",
  "fileData": "{\"applinks\": {\"apps\": [], \"details\": []}}",
  "contentType": "application/json"
}
```

## Delete Files

```
DELETE https://api.webflow.com/v2/sites/{site_id}/well_known
```

**Required scope:** `site_config:write`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier for a Site |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `fileNames` | array of strings | No | List of file names to delete |

### Response (204)

Returns an empty object on success.

### SDK Examples

#### Python

```python
from webflow import Webflow

client = Webflow(access_token="YOUR_ACCESS_TOKEN")
client.sites.well_known.delete(site_id="580e63e98c9a982ac9b8b741")
```

#### TypeScript

```typescript
import { WebflowClient } from "webflow-api";

const client = new WebflowClient({ accessToken: "YOUR_ACCESS_TOKEN" });
await client.sites.wellKnown.delete("580e63e98c9a982ac9b8b741");
```

## Error Responses

| Code | Description |
|------|-------------|
| 400 | Request body was incorrectly formatted |
| 401 | Provided access token is invalid or does not have access to requested resource |
| 404 | Requested resource not found |
| 429 | Rate limit reached — check `X-RateLimit-Remaining` header |
| 500 | Server error — try again later |

## Best Practices

- Use `.noext` for files that must not have an extension (e.g., `apple-app-site-association`)
- Keep file content under 100 KB — compress or minify JSON if needed
- Use `"application/json"` content type for JSON files and `"text/plain"` for text files
- Verify uploaded files are accessible at `https://your-domain.com/.well-known/{fileName}` after publishing
