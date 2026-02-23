---
name: "Optimize Overview"
description: "Introduction to Webflow Optimize Browser API methods: tracking variations with onVariationRecorded and personalizing with custom attributes via setAttributes."
tags: [optimize, overview, quickstart, variations, attributes, personalization, ab-testing, experiment]
---

# Optimize Overview

Webflow Optimize enables you to customize the version of a page shown to visitors based on their characteristics. It functions as an enhanced A/B testing tool with dynamic personalization driven by visitor attributes.

---

## Capabilities

| Feature | Method | Description |
|---------|--------|-------------|
| Track variations | `wf.onVariationRecorded()` | Forward experiment data to third-party analytics tools |
| Custom attributes | `wf.setAttributes()` | Personalize experiences based on visitor behavior and data |

Both methods are automatically available on all Webflow Optimize-enabled sites via the global `wf` object with no manual installation required.

## Quickstart

### Prerequisites

- A Webflow site with Optimize enabled
- Ability to add custom JavaScript via Webflow custom code or Google Tag Manager

### Step 1: Wrap code in `wf.ready()`

Since the API loads asynchronously, always wrap your code:

```javascript
wf.ready(function() {
  // Your Optimize code here
});
```

### Step 2: Add callbacks and attributes

```javascript
wf.ready(function() {
  // Track variation events
  wf.onVariationRecorded(function(result) {
    console.log(result);
  });

  // Set custom visitor attributes
  wf.setAttributes("user", {
    userSegment: "enterprise",
    userRole: "technicalBuyer",
  });
});
```

## Next Steps

- **`variations.md`** — Learn about variations and the `onVariationRecorded()` callback
- **`attributes.md`** — Learn about custom attributes and the `setAttributes()` method

## Best Practices

- Register `onVariationRecorded()` callbacks as early as possible to avoid missing variation events
- Place Optimize scripts in `<head>` custom code for earliest possible execution
- Use Google Tag Manager for complex analytics integrations that need additional tag coordination
