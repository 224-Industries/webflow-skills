---
name: "wf.ready()"
description: "API reference for wf.ready(): ensures the Browser API is fully loaded before executing any API methods."
tags: [wf-ready, initialization, callback, browser-api, async]
---

# wf.ready()

Ensures the Browser API is loaded before executing any API methods. All Browser API logic should be wrapped inside this method.

---

## Syntax

```typescript
wf.ready(callback: () => void): void
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `callback` | `() => void` | Yes | Function to execute once the Browser API is ready |

## Return Value

`void`

## Usage

```javascript
wf.ready(function() {
  console.log("The Browser API is ready to use!");
  const consentStatus = wf.getUserTrackingChoice();
  console.log(consentStatus);
});
```

## Multiple Calls

You can call `wf.ready()` multiple times on the same page. Each callback executes in registration order:

```javascript
wf.ready(function() {
  // First callback
  wf.onVariationRecorded(function(result) {
    console.log(result);
  });
});

wf.ready(function() {
  // Second callback
  wf.setAttributes("user", { userSegment: "enterprise" });
});
```

## Best Practices

- Always place Browser API method calls inside the `wf.ready()` callback
- Call `wf.ready()` as early as possible — ideally before DOM rendering begins — to avoid missing time-sensitive events
- Place scripts in `<head>` custom code for earliest possible execution
