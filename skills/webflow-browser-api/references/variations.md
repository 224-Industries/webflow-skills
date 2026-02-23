---
name: "Variations & onVariationRecorded()"
description: "Reference for Optimize variations and the wf.onVariationRecorded() callback: tracking experiment data, result object properties, and forwarding to third-party analytics."
tags: [variations, on-variation-recorded, optimize, experiment, ab-test, personalization, analytics, callback]
---

# Variations & onVariationRecorded()

Variations are alternate webpage versions displayed to different visitors for testing engagement. They always belong to either a **test** or **personalization** optimization.

---

## Concept

An optimization contains one or more variations. For example, testing three homepage headlines means creating an optimization with three corresponding variations.

After each variation is recorded, the applied variation data is passed to callback functions registered through `onVariationRecorded()`. The primary use case is capturing variation data and forwarding it to custom or third-party analytics tools.

## `wf.onVariationRecorded()`

Registers a callback that fires whenever a variation runs successfully.

### Syntax

```javascript
wf.onVariationRecorded(callback: (result: VariationResult) => void): void
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `callback` | `(result) => void` | Yes | Function that receives variation data when a variation is recorded |

### Result Object

The callback receives a result object with these properties:

| Property | Type | Description |
|----------|------|-------------|
| `experienceId` | `string` | Unique experiment identifier |
| `experienceName` | `string` | Display name of the experiment |
| `experienceType` | `"ab" \| "rbp" \| "cc"` | A/B Test, Rules-Based Personalization, or Content Configuration |
| `variationId` | `string` | Unique variation identifier |
| `variationName` | `string` | Display name of the variation |
| `ccStatus` | `"holdout" \| "optimized"` | Content Configuration only — holdout group or optimized content |

### Example Result

```json
{
  "experienceId": "417228929",
  "experienceName": "Hero Optimization",
  "experienceType": "rbp",
  "variationId": "617106113",
  "variationName": "Desktop",
  "ccStatus": "optimized"
}
```

### Usage

```javascript
wf.ready(function() {
  wf.onVariationRecorded(function(result) {
    console.log(result);

    // Forward to analytics
    analytics.track("Variation Recorded", {
      experimentId: result.experienceId,
      experimentName: result.experienceName,
      variationId: result.variationId,
      variationName: result.variationName,
    });
  });
});
```

### Timing and Behavior

- **Register early** — The callback only triggers for variations recorded *after* registration. Place it in `<head>` custom code before DOM rendering to avoid missing events.
- **Fires per variation** — Multiple variations on a page trigger multiple callbacks.
- **Recording trigger** — A variation is considered recorded after it's selected, applied to the page, and analytics events are dispatched.

## Best Practices

- Register `onVariationRecorded()` as early as possible in `<head>` to capture all variation events
- Forward variation data to your analytics platform to correlate experiment results with business metrics
- Use `experienceType` to distinguish between A/B tests (`"ab"`), rules-based personalizations (`"rbp"`), and content configurations (`"cc"`)
- Handle the `ccStatus` field for content configuration experiments to differentiate holdout vs. optimized groups
