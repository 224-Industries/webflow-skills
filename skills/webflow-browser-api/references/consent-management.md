---
name: "Consent Management"
description: "Consent management APIs for Webflow Analyze and Optimize: getUserTrackingChoice, allowUserTracking, denyUserTracking, plus CMP integration examples for OneTrust, TrustArc, and custom solutions."
tags: [consent, tracking, privacy, gdpr, onetrust, trustarc, cmp, allow-tracking, deny-tracking, get-tracking-choice, cookie-consent]
---

# Consent Management

Webflow's Browser APIs enable tracking consent management for Analyze and Optimize. Site tracking must be enabled before using these APIs.

---

## Concepts

- **Site tracking** records analytics, personalizes experiences, and runs AI-powered tests
- **Consent management** lets visitors choose how their data is collected, typically via a banner or modal

## API Methods

### `wf.getUserTrackingChoice()`

Returns the user's current tracking consent state.

```typescript
wf.getUserTrackingChoice(): "allow" | "deny" | "none"
```

| Return Value | Meaning |
|--------------|---------|
| `"allow"` | User opted in to tracking |
| `"deny"` | User opted out of tracking |
| `"none"` | No choice has been made yet |

```javascript
wf.ready(function() {
  var choice = wf.getUserTrackingChoice();
  console.log(choice); // "allow", "deny", or "none"
});
```

### `wf.allowUserTracking(options?)`

Opts the user into Webflow tracking.

```typescript
wf.allowUserTracking(options?: { reload?: boolean; activate?: boolean }): void
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `reload` | boolean | `false` | Refresh the page after activation |
| `activate` | boolean | `true` | Trigger tracking immediately |

```javascript
wf.ready(function() {
  wf.allowUserTracking({ activate: true });
});
```

### `wf.denyUserTracking(options?)`

Opts the user out of Webflow tracking.

```typescript
wf.denyUserTracking(options?: { reload?: boolean }): void
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `reload` | boolean | `false` | Reload the page after disabling tracking |

```javascript
wf.ready(function() {
  wf.denyUserTracking({ reload: true });
});
```

## General CMP Integration Pattern

Use `getUserTrackingChoice()` to check the current state, then call `allowUserTracking()` or `denyUserTracking()` based on the user's decision:

```javascript
wf.ready(function() {
  var isOptedOut = wf.getUserTrackingChoice() === "deny";

  if (isOptedOut) {
    // User previously denied — handle CMP opt-in logic
    wf.allowUserTracking();
  } else {
    // Handle CMP opt-out logic
    wf.denyUserTracking();
  }
});
```

## OneTrust Integration

Parse the `OptanonConsent` cookie to check the functional consent group (`3:1`):

```javascript
wf.ready(function() {
  var otCookieKey = "OptanonConsent=";
  var otCookie = document.cookie
    .split("; ")
    .find(function(row) { return row.startsWith(otCookieKey); });

  if (otCookie) {
    var otGroups = decodeURIComponent(otCookie).split("groups=")[1];
    var OT_FUNCTIONAL_CONSENT = "3:1";
    var hasOptedIn = otGroups.indexOf(OT_FUNCTIONAL_CONSENT) !== -1;

    if (hasOptedIn) {
      wf.allowUserTracking();
    } else {
      wf.denyUserTracking();
    }
  }

  // Listen for consent changes
  if (window.OneTrust) {
    OneTrust.OnConsentChanged(function() {
      // Re-check consent state
    });
  }
});
```

> **Note:** This example is provided as-is and is not supported by Webflow. Customize the group/level checks to match your OneTrust configuration.

## TrustArc Integration

Read the `truste.cookie.notice_gdpr_prefs` value from localStorage:

```javascript
wf.ready(function() {
  var prefsRaw = localStorage.getItem("truste.cookie.notice_gdpr_prefs");

  if (prefsRaw) {
    var prefs = JSON.parse(prefsRaw).value;
    var TA_FUNCTIONAL = 1;
    var hasOptedIn = prefs.indexOf(TA_FUNCTIONAL) >= 0;

    if (hasOptedIn) {
      wf.allowUserTracking();
    } else {
      wf.denyUserTracking();
    }
  }
});
```

> **Note:** This example is provided as-is and is not supported by Webflow. Customize the level checks to match your TrustArc configuration.

## Custom Consent Solution

You can build your own consent banner using the Webflow Designer API for the UI and the Browser API for consent logic. A typical flow:

1. On `wf.ready()`, check `getUserTrackingChoice()`
2. If the return value is `"none"`, show the consent banner
3. If `"allow"` or `"deny"`, hide the banner (user already chose)
4. On accept click, call `wf.allowUserTracking({ activate: true })` and hide the banner
5. On decline click, call `wf.denyUserTracking()` and hide the banner

> **Warning:** Custom consent implementations are a starting point and may not fully comply with all privacy laws. Consult legal counsel for your specific requirements.

## Marketplace Apps

For pre-built consent management solutions, see the Webflow Marketplace:

- **DataGrail** — Privacy management platform integration
- **Finsweet Cookie Consent** — Cookie consent component for Webflow

## Best Practices

- Always check `getUserTrackingChoice()` before showing consent UI to avoid prompting users who already made a choice
- Use `{ activate: true }` with `allowUserTracking()` to trigger tracking immediately without requiring a page reload
- Listen for consent changes in third-party CMPs to keep Webflow tracking in sync
- Place consent logic in `<head>` custom code so it executes before page content loads
- Never assume consent — always check and respect the user's explicit choice
