---
name: "Setting Up Webflow Webhooks"
description: "Step-by-step guide to creating Webflow webhooks via the dashboard and API, OAuth credentials, and environment configuration."
tags: [setup, dashboard, api, oauth, credentials, environment, create, secrets]
---

# Setting Up Webflow Webhooks

## Prerequisites

- A Webflow account with an active site
- For signature verification: OAuth app or API access
- Your application's webhook endpoint URL (must be HTTPS in production)

## Two Ways to Create Webhooks

### 1. Via Webflow Dashboard (No Signature Verification)

⚠️ **Note**: Webhooks created through the dashboard do NOT include signature headers for verification.

1. Go to your Webflow project
2. Navigate to **Project Settings** → **Integrations** → **Webhooks**
3. Click **Add Webhook**
4. Select the trigger event
5. Enter your endpoint URL
6. Save the webhook

### 2. Via API (Recommended - Includes Signatures)

This method provides signature headers for secure verification.

#### Get Your API Credentials

**For OAuth Apps:**
1. Go to [Webflow Dashboard](https://webflow.com/dashboard/account/apps)
2. Create or select your app
3. Note your **Client ID** and **Client Secret**
4. The Client Secret will be your webhook signing secret

**For Site API Tokens:**
1. Go to **Project Settings** → **Integrations** → **API Access**
2. Generate a site token
3. For webhooks created after April 2025, you'll receive a webhook-specific secret

#### Create Webhook via API

```bash
curl -X POST https://api.webflow.com/v2/sites/{site_id}/webhooks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "triggerType": "form_submission",
    "url": "https://your-app.com/webhooks/webflow",
    "filter": {
      "name": "contact-form"
    }
  }'
```

Response (for webhooks after April 2025):
```json
{
  "id": "65a5d7a8f7e2b40012345684",
  "triggerType": "form_submission",
  "url": "https://your-app.com/webhooks/webflow",
  "secret": "whsec_1234567890abcdef",
  "createdOn": "2024-01-15T14:45:00.000Z"
}
```

Save the `secret` field - this is your webhook signing secret.

## Managing Webhooks

For the complete REST API reference (list, get, create, delete), required scopes per trigger type, and response schemas, see [Webhook API Reference](webhook-api.md).

## Environment Setup

Create a `.env` file for your application:

```bash
# For OAuth App webhooks
WEBFLOW_WEBHOOK_SECRET=your_oauth_client_secret

# For API-created webhooks (after April 2025)
WEBFLOW_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx

# Optional: For making API calls
WEBFLOW_API_TOKEN=your_api_token
WEBFLOW_SITE_ID=your_site_id
```

## Best Practices

1. **Always verify signatures** for webhooks that include them
2. **Validate timestamps** to prevent replay attacks
3. **Return 200 quickly** to avoid timeouts (process async if needed)
4. **Log raw payloads** during development for debugging
5. **Use HTTPS** for production endpoints
6. **Handle retries** — Webflow retries failed webhooks up to 3 times (10-minute intervals)

For troubleshooting common issues, see [FAQ](faq.md).