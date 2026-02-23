---
name: "FAQ & Troubleshooting"
description: "Frequently asked questions and troubleshooting for Webflow webhooks: signature failures, missing headers, webhook not firing, secret key confusion, body parsing issues, and common error messages."
tags: [faq, troubleshooting, debugging, signature, verification, headers, missing-headers, raw-body, secret, timestamp, errors, retries, dashboard, oauth, api]
---

# FAQ & Troubleshooting

## Table of Contents

- [General Questions](#general-questions)
- [Signature Verification Issues](#signature-verification-issues)
- [Webhook Delivery Issues](#webhook-delivery-issues)
- [API & Configuration Issues](#api--configuration-issues)

---

## General Questions

### Do dashboard-created webhooks support signature verification?

No. Webhooks created through the Webflow dashboard do **not** include `x-webflow-signature` or `x-webflow-timestamp` headers. Only webhooks created via OAuth apps or the API include signature headers. If you need verification, recreate the webhook via the API — see [Webhook API Reference](webhook-api.md).

### Which secret should I use for verification?

It depends on how the webhook was created:

| Creation Method | Signing Secret |
|----------------|----------------|
| OAuth App | Your OAuth app's **client secret** |
| API (after April 2025) | The webhook-specific secret (`whsec_xxxxx`) returned in the create response |
| Dashboard | No signature verification available |

### What happens if my endpoint doesn't return 200?

Webflow treats any non-200 response as a failure and retries the webhook up to **3 additional times** at **10-minute intervals**. Redirects and SSL certificate issues are also treated as failures.

### What's the maximum number of webhooks I can register?

75 per `triggerType` per site. For example, you can have 75 `form_submission` webhooks and 75 `site_publish` webhooks on the same site.

### Are webhooks fired for draft changes?

No. Webhooks only fire for published changes. Draft CMS items, unpublished pages, and other draft content do not trigger events until they are published.

---

## Signature Verification Issues

### "Invalid signature" — wrong secret

The most common cause. Double-check which secret you're using:

- **OAuth App webhooks** → use the OAuth app's client secret
- **API-created webhooks (after April 2025)** → use the `whsec_xxxxx` secret from the creation response

If you've lost the secret, you'll need to delete and recreate the webhook.

### "Invalid signature" — body parsing issue

Signature verification requires the **raw request body** as a string, not parsed JSON. If your framework auto-parses the body, the signature will never match.

**Express:**
```javascript
// Use express.raw() to get the raw body
app.post('/webhooks/webflow',
  express.raw({ type: 'application/json' }),
  handler
);
```

**Next.js (App Router):**
```typescript
// Use request.text() to get the raw body
const rawBody = await request.text();
```

**FastAPI:**
```python
# Use request.body() to get raw bytes
raw_body = await request.body()
```

### "Invalid signature" — encoding mismatch

Webflow uses **hex** encoding for the HMAC-SHA256 signature. Make sure you're using `.digest('hex')` (Node.js) or `.hexdigest()` (Python), not base64 or other encodings.

### "Invalid signature" — timestamp expired

The verification should enforce a 5-minute window (300,000 milliseconds). If your server's clock is significantly skewed, valid webhooks may fail timestamp validation. Check that your server time is synchronized via NTP.

### "Missing required headers"

The webhook was likely created via the dashboard, which does not include signature headers. Recreate it via the API to get `x-webflow-signature` and `x-webflow-timestamp` headers.

### How do I debug signature verification?

Log everything during development:

```javascript
function debugVerification(rawBody, signature, timestamp, secret) {
  console.log('Raw Body:', rawBody);
  console.log('Signature Header:', signature);
  console.log('Timestamp Header:', timestamp);
  console.log('Secret (first 6 chars):', secret.substring(0, 6) + '...');

  const signedContent = `${timestamp}:${rawBody}`;
  console.log('Signed Content:', signedContent);

  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(signedContent)
    .digest('hex');
  console.log('Expected Signature:', expectedSignature);
  console.log('Match:', signature === expectedSignature);
}
```

### Common verification error matrix

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| No signature headers at all | Dashboard-created webhook | Recreate via API |
| Signature never matches | Wrong secret key | Check OAuth secret vs webhook secret |
| Signature never matches | Body was parsed before verification | Use raw body middleware |
| Signature never matches | Wrong encoding | Use hex, not base64 |
| Intermittent failures | Server clock skew | Sync time via NTP, ensure 5-min window |
| Header not found | Framework normalizes to lowercase | Use `req.headers['x-webflow-signature']` (lowercase) |

---

## Webhook Delivery Issues

### Webhook not firing

- **Site not published:** Draft changes don't trigger webhooks. Publish the site first.
- **Webhook disabled:** Verify the webhook is still active via the API (`GET /webhooks/{id}`).
- **Wrong trigger type:** Confirm the webhook is registered for the correct event.
- **Endpoint returning non-200:** Check your server logs. Any non-200 response causes Webflow to consider delivery failed.

### Webhook fired but my app didn't process it

- **Check for 200 response:** Your endpoint must return `200` quickly. If processing takes too long, the request times out and Webflow counts it as failed.
- **Async processing:** For heavy workloads, acknowledge with `200` immediately, then process the event asynchronously (e.g., via a job queue).
- **Duplicate events:** Webflow retries on failure. Implement idempotency to handle duplicate deliveries safely.

### Webhook retries and failures

Webflow retries failed webhooks up to 3 times at 10-minute intervals. The following are all treated as failures:

- Non-200 HTTP status code
- HTTP redirects (3xx)
- SSL certificate negotiation or validation failures
- Request timeout

After 3 retries, the webhook delivery is abandoned for that event.

---

## API & Configuration Issues

### "401 Unauthorized" when creating webhooks

- Verify your bearer token is valid and not expired
- Ensure the token is from a Data Client App (not a site token for write operations)
- Check that your app has the `sites:write` scope for creating webhooks

### "404 Not Found" when getting/deleting a webhook

- Confirm the `webhook_id` is correct
- The webhook may have already been deleted
- Ensure you're using the v2 API path (`/v2/webhooks/{id}`, not `/webhooks/{id}`)

### "429 Too Many Requests"

You've hit the Webflow API rate limit. Implement exponential backoff and retry logic. Check the `Retry-After` header for timing guidance.

### Can't receive events for a specific trigger type

Your OAuth app or API token must have the correct scope for the event category:

| Events | Required Scope |
|--------|----------------|
| `form_submission` | `forms:read` |
| `site_publish` | `sites:read` |
| `page_*` | `pages:read` |
| `ecomm_*` | `ecommerce:read` |
| `collection_item_*` | `cms:read` |
| `comment_created` | `comments:read` |

Update your app's scopes in the Webflow Dashboard under Workspace Settings > Apps & Integrations.