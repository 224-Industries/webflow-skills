---
name: "Webflow Webhooks Overview"
description: "Conceptual overview of Webflow webhooks: what they are, how they work, delivery behavior, limits, and security considerations."
tags: [webhooks, overview, concepts, delivery, limits, security, https, retries, failure-conditions]
---

# Webflow Webhooks Overview

## What Are Webflow Webhooks?

Webflow webhooks are HTTP callbacks that notify your application when events occur in a Webflow site. They enable real-time integration with external systems, allowing you to react to form submissions, content changes, ecommerce orders, and site publishing events.

## How They Work

When an event occurs, Webflow sends a POST request to your registered URL. The webhook body is a JSON object with a consistent envelope:

```json
{
  "triggerType": "event_name",
  "payload": {
    // Event-specific data
  }
}
```

The request headers include:

- `x-webflow-timestamp` — Unix epoch timestamp (ms) when the webhook was sent
- `x-webflow-signature` — HMAC-SHA256 signature of the payload

> **Note:** Signature headers are only present for webhooks created via OAuth apps or the API. Dashboard-created webhooks do not include these headers.

For the complete list of all 14 event types with payload schemas and examples, see **[Event Types](event-types.md)**.

## Delivery Behavior

Your endpoint must return a **200** status to acknowledge receipt. Webflow treats the following as failures:

- **Non-200 HTTP status code** — any response other than 200
- **Redirects** — if the endpoint redirects the request
- **SSL certificate issues** — if SSL negotiation or validation fails

On failure, Webflow retries the webhook up to **3 additional times** at **10-minute intervals**.

## Webhook Limits

| Criteria | Limit |
|----------|-------|
| Max webhooks per trigger type per site | 75 |
| Retry attempts on failure | 3 (at 10-minute intervals) |
| Required response status | 200 |

## Security Considerations

- **Signature Verification**: Webhooks created via OAuth apps or API include signature headers — see [Verification](verification.md)
- **HTTPS Only**: Webhook endpoints must use HTTPS in production
- **Timestamp Validation**: Check timestamps to prevent replay attacks (5-minute window / 300,000ms)
- **Raw Body**: Always use the raw request body for signature verification, not parsed JSON