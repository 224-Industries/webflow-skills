---
name: "Browser API Introduction"
description: "Overview of the Webflow Browser API: the global wf object, capabilities, placement options, and getting started with Analyze and Optimize."
tags: [introduction, overview, browser-api, wf, analyze, optimize, custom-code, google-tag-manager]
---

# Browser API Introduction

The Browser API is a JavaScript interface exposed via the global `wf` object on all Webflow sites with Analyze and Optimize enabled. It requires no manual installation — the API is automatically available.

---

## Capabilities

| Feature | Description |
|---------|-------------|
| Manage consent | Handle visitor privacy preferences in real time |
| Track variations | Forward experiment data to third-party analytics tools |
| Custom attributes | Set visitor attributes from behavior or data for personalization |

## Getting Started

### Placement Options

You can add Browser API code in two ways:

1. **Custom Code** — Add an inline script before `</head>` in Webflow's site or page custom code settings
2. **Google Tag Manager** — Configure a custom tag that calls the Browser API

### Readiness Wrapper

Since the API loads asynchronously, always wrap your code in `wf.ready()` to ensure the API is initialized:

```javascript
wf.ready(function() {
  // Your Browser API code here
});
```

> **Note:** Call `wf.ready()` as early as possible — ideally before DOM rendering begins — to avoid missing time-sensitive events like variation recordings.

### Full Example

```javascript
wf.ready(function() {
  wf.onVariationRecorded(function(result) {
    console.log(result);
  });

  wf.setAttributes("user", {
    userSegment: "enterprise",
    userRole: "technicalBuyer",
  });
});
```

### Multiple `wf.ready()` Calls

You can call `wf.ready()` multiple times on the same page. Each callback executes in order:

```javascript
wf.ready(function() {
  wf.onVariationRecorded(function(result) {
    console.log(result);
  });
});

wf.ready(function() {
  wf.setAttributes("user", {
    userSegment: "enterprise",
  });
});
```

## API Methods

### Core

- `wf.ready(callback)` — Ensure the Browser API is loaded before executing code. See `wf-ready.md`.

### Consent Management

- `wf.getUserTrackingChoice()` — Get the user's current consent state
- `wf.allowUserTracking(options?)` — Opt a user into tracking
- `wf.denyUserTracking(options?)` — Opt a user out of tracking

See `consent-management.md` for full details and CMP integration examples.

### Optimize

- `wf.onVariationRecorded(callback)` — Register a callback for variation events
- `wf.setAttributes(scope, attributes)` — Set custom visitor attributes

See `variations.md` and `attributes.md` for full details.

## Best Practices

- Always wrap Browser API calls inside `wf.ready()` to prevent calls before initialization
- Place scripts in `<head>` before DOM rendering for time-sensitive operations like variation tracking
- Use custom code for simple integrations; use Google Tag Manager for complex tag management workflows
