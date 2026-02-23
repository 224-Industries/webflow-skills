---
name: "Custom Attributes & setAttributes()"
description: "Reference for Optimize custom attributes and wf.setAttributes(): defining visitor characteristics, scopes (user vs pageview), and using attributes for audiences and result filtering."
tags: [attributes, set-attributes, optimize, personalization, audience, scope, user, pageview, enterprise]
---

# Custom Attributes & setAttributes()

Custom attributes represent visitor characteristics such as demographics, behavior, or account data. Use them to define rules-based audiences and filter optimization results.

---

## Concept

Attributes let you store and retrieve visitor data not available by default in Webflow Optimize. The workflow is:

1. Define the attribute in Webflow Optimize settings
2. Set it via the Browser API using `wf.setAttributes()`
3. Use the attribute to build audiences or filter results

> **Note:** Custom JavaScript attributes are only available on Enterprise Webflow sites.

## Configuration

### Step 1: Create the attribute in Webflow Optimize

1. Navigate to **Insights > Integrations** on your site
2. Find the **"Custom JavaScript attributes"** section
3. Add a new attribute entry

### Step 2: Set the attribute via Browser API

Use `wf.setAttributes()` to assign values to the attribute at runtime.

## `wf.setAttributes()`

Sets custom visitor attributes for use in Optimize audiences and result filtering.

### Syntax

```typescript
wf.setAttributes(scope: "user" | "pageview", attributes: Record<string, string>): void
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scope` | `"user" \| "pageview"` | Yes | Attribute lifetime scope |
| `attributes` | `Record<string, string>` | Yes | Key-value pairs of attribute names and values |

### Scopes

| Scope | Lifetime |
|-------|----------|
| `"pageview"` | Duration of a single page view |
| `"user"` | Session duration (ends after 30 minutes of inactivity) |

### Attribute Key Constraints

- Must be under 40 characters
- Cannot contain `=`

### Return Value

No client-side return value. Data is transmitted to Webflow Optimize and recorded in the dashboard.

### Usage

```javascript
wf.ready(function() {
  wf.setAttributes("user", {
    customerSegment: "enterprise",
    userRole: "technicalBuyer",
  });
});
```

### Pageview-scoped example

```javascript
wf.ready(function() {
  wf.setAttributes("pageview", {
    referrer: document.referrer || "direct",
    landingPage: window.location.pathname,
  });
});
```

## Using Attributes

After setting attributes via the Browser API, you can:

- **Build rules-based audiences** — Target visitors by attribute values in Optimize
- **Filter optimization results** — Segment experiment results by attribute values in the dashboard

## Best Practices

- Always pass string values explicitly — the API attempts automatic conversion of booleans and numbers, but strings are most reliable
- Create the attribute in **Insights > Integrations** before calling `setAttributes()`, otherwise the values won't be recorded
- Use `"user"` scope for persistent characteristics (account type, segment) and `"pageview"` scope for contextual data (referrer, landing page)
- Keep attribute keys short, descriptive, and under 40 characters
