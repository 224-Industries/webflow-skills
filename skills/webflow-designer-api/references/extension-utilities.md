---
name: "Extension Utilities"
description: "Reference for site info, extension sizing, element snapshots, event subscriptions, notifications, app intents/connections, and user authentication."
tags: [utilities, getSiteInfo, setExtensionSize, closeExtension, getMediaQuery, getElementSnapshot, subscribe, notify, getLaunchContext, getIdToken, setAppConnection, getAppConnections, removeAppConnection, events, selectedElement, currentpage, mediaquery, currentcmsitem, currentappmode, pseudomode, notifications, app-intents, app-connections, authentication, jwt, site-info, breakpoint, resize, snapshot, webflow-json]
---

# Extension Utilities API Reference

Utilities for managing extension behavior, responding to Designer events, and integrating with Webflow's discovery features.

## Table of Contents

- [Site Information](#site-information)
- [Extension Sizing](#extension-sizing)
- [Element Snapshots](#element-snapshots)
- [Event Subscriptions](#event-subscriptions)
- [Notifications](#notifications)
- [App Intents and Connections](#app-intents-and-connections)
- [User Authentication](#user-authentication)
- [Workflow Examples](#workflow-examples)
- [Best Practices](#best-practices)

---

## Site Information

Retrieve metadata about the current site.

```typescript
webflow.getSiteInfo(): Promise<SiteInfo>
```

```typescript
const siteInfo = await webflow.getSiteInfo();
```

**Returns:**

| Property | Type | Description |
|----------|------|-------------|
| `siteId` | `string` | Unique site ID |
| `siteName` | `string` | Site name |
| `shortName` | `string` | Short name (for deep links) |
| `isPasswordProtected` | `boolean` | Password protection status |
| `isPrivateStaging` | `boolean` | Private staging status |
| `workspaceId` | `string` | Workspace ID |
| `workspaceSlug` | `string` | Workspace slug |
| `domains` | `Array<{ url, lastPublished, default, stage }>` | Domain info (`stage` is `"staging"` or `"production"`) |

## Extension Sizing

Dynamically resize the extension panel.

```typescript
webflow.setExtensionSize(
  size: "default" | "comfortable" | "large" | { width: number, height: number }
): Promise<null>
```

**Preset Sizes:**

| Size | Dimensions | Use Case |
|------|------------|----------|
| `"default"` | 240 x 360px | Simple apps |
| `"comfortable"` | 320 x 460px | Forms, more content |
| `"large"` | 800 x 600px | Complex workflows, previews |
| `{ width, height }` | Custom | Min: 240 x 360, Max: 1200 x 800 |

```typescript
// Preset size
await webflow.setExtensionSize("comfortable");

// Custom size
await webflow.setExtensionSize({ width: 400, height: 500 });
```

### Close Extension

Programmatically close the extension.

```typescript
webflow.closeExtension(): Promise<null>
```

```typescript
await webflow.closeExtension();
```

### Get Current Breakpoint

Retrieve the current responsive breakpoint in the Designer.

```typescript
webflow.getMediaQuery(): Promise<BreakpointId>
```

**Returns:** `"xxl" | "xl" | "large" | "main" | "medium" | "small" | "tiny"`

```typescript
const breakpoint = await webflow.getMediaQuery();
if (breakpoint === 'small' || breakpoint === 'tiny') {
  console.log("Mobile view active");
}
```

## Element Snapshots

Capture a visual snapshot of an element as a base64-encoded PNG image.

```typescript
webflow.getElementSnapshot(
  element: AnyElement
): Promise<string | null>
```

Returns a string with the `data:image/png;base64,` prefix, or `null` if capture fails.

```typescript
const selected = await webflow.getSelectedElement();
if (selected) {
  const snapshot = await webflow.getElementSnapshot(selected);
  if (snapshot) {
    const img = document.getElementById("preview") as HTMLImageElement;
    img.src = snapshot;
  }
}
```

## Event Subscriptions

Subscribe to Designer events to keep your extension in sync. Returns an unsubscribe function.

```typescript
const unsubscribe = webflow.subscribe(eventName, callback);
```

**Available Events:**

| Event | Callback Parameter | Description |
|-------|-------------------|-------------|
| `"selectedElement"` | `Element \| null` | User selects a different element |
| `"currentpage"` | `Page` | User switches pages |
| `"mediaquery"` | `BreakpointId` | User changes breakpoint |
| `"currentcmsitem"` | `CmsItem` | User selects a Collection page or item |
| `"currentappmode"` | `Mode` | User switches modes in the Designer |
| `"pseudomode"` | `PseudoState` | Pseudo-state of the Designer changes |

**Returns:** `() => void` — call to unsubscribe

```typescript
// Track selected element
const unsubscribe = webflow.subscribe("selectedElement", (element) => {
  if (element) {
    console.log("Selected:", element.type);
  } else {
    console.log("No element selected");
  }
});

// Later: stop listening
unsubscribe();
```

```typescript
// Track page changes
webflow.subscribe("currentpage", (page) => {
  console.log("Now on page:", page.getName());
});
```

```typescript
// Track breakpoint changes
webflow.subscribe("mediaquery", (breakpoint) => {
  console.log("Breakpoint:", breakpoint);
});
```

## Notifications

Display in-Designer notifications to users.

```typescript
webflow.notify(
  opts: { type: "Success" | "Error" | "Info", message: string }
): Promise<void>
```

| Type | Appearance | Use Case |
|------|------------|----------|
| `"Success"` | Green | Completed actions |
| `"Error"` | Red | Failures, invalid input (allows user to close the extension) |
| `"Info"` | Blue | Tips, guidance |

```typescript
await webflow.notify({ type: 'Success', message: 'Element created successfully!' });
await webflow.notify({ type: 'Error', message: 'Please select an element first.' });
await webflow.notify({ type: 'Info', message: 'Tip: Hold Shift to select multiple elements.' });
```

## App Intents and Connections

Make your extension discoverable in element settings panels.

### Concepts

- **App Intents**: Make your app appear in "Connect an App" when users interact with supported elements. Configured in `webflow.json`.
- **App Connections**: Direct links between specific elements and your app. Users see your app in the element's settings panel.

### Supported Elements

Currently supported: `Image`, `FormForm`, `FormWrapper`

### Configure in webflow.json

```json
{
  "appIntents": {
    "image": ["manage"],
    "form": ["manage"]
  },
  "appConnections": ["manageImageElement", "manageFormElement"]
}
```

### Get Launch Context

Determine how your extension was launched.

```typescript
webflow.getLaunchContext(): Promise<LaunchContext | null>
```

**Returns:**

```typescript
type LaunchContext = {
  type: 'AppIntent' | 'AppConnection' | 'AppsPanel';
  value: null | string | Record<'form' | 'image', 'create' | 'manage'>;
}
```

| Type | Value | Trigger |
|------|-------|---------|
| `'AppIntent'` | `{ image: 'manage' }` or `{ form: 'manage' }` | User clicks "Connect an App" on a supported element |
| `'AppConnection'` | Connection identifier string | User clicks an existing connection |
| `'AppsPanel'` | `null` | User launches from the Apps panel |

```typescript
const context = await webflow.getLaunchContext();

if (context?.type === 'AppIntent') {
  if (context.value?.image === 'manage') {
    showImageManager();
  } else if (context.value?.form === 'manage') {
    showFormManager();
  }
} else if (context?.type === 'AppConnection') {
  handleConnection(context.value);
} else {
  showHomePage();
}
```

### Manage App Connections

```typescript
// Set a connection on an element
await element.setAppConnection('manageImageElement');

// Get all connections for an element (only returns connections from your app)
const connections = await element.getAppConnections();

// Remove a connection
await element.removeAppConnection('manageImageElement');
```

> **Note**: Check `element.appConnections` to verify the element supports app connections before calling these methods.

## User Authentication

Authenticate users for Data API access or personalized features.

```typescript
webflow.getIdToken(): Promise<string>
```

Returns a JWT valid for 15 minutes that identifies the current user.

```typescript
const idToken = await webflow.getIdToken();
```

### Token Resolution

Send the token to Webflow's Resolve ID Token endpoint to get user details:

```typescript
// In your extension
const idToken = await webflow.getIdToken();

// Send to your backend
const response = await fetch('https://your-backend.com/auth', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ idToken })
});
```

```typescript
// On your backend - resolve with Webflow API
const resolved = await fetch('https://api.webflow.com/token/resolve', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ idToken })
});

const userData = await resolved.json();
// Returns: { id, email, firstName, lastName, ... }
```

## Workflow Examples

### Responsive Extension Layout

Adjusts the extension size based on the current breakpoint.

```typescript
async function setupResponsiveLayout() {
  const breakpoint = await webflow.getMediaQuery();

  if (breakpoint === 'small' || breakpoint === 'tiny') {
    await webflow.setExtensionSize("default");
  } else {
    await webflow.setExtensionSize("comfortable");
  }

  webflow.subscribe("mediaquery", async (newBreakpoint) => {
    if (newBreakpoint === 'small' || newBreakpoint === 'tiny') {
      await webflow.setExtensionSize("default");
    } else {
      await webflow.setExtensionSize("comfortable");
    }
  });
}
```

### Handle Launch Context with Element Connection

Sets up an app connection when launched from an App Intent on an image element.

```typescript
async function handleImageIntent() {
  const context = await webflow.getLaunchContext();

  if (context?.type !== 'AppIntent' || context.value?.image !== 'manage') {
    return;
  }

  const selected = await webflow.getSelectedElement();
  if (!selected || selected.type !== 'Image') {
    await webflow.notify({ type: 'Error', message: 'No image element selected' });
    return;
  }

  await selected.setAppConnection('manageImageElement');
  await webflow.notify({ type: 'Success', message: 'Image connected to app' });
}
```

### Authenticate and Fetch User Data

Retrieves the current user's ID token and sends it to a backend for resolution.

```typescript
async function authenticateUser() {
  try {
    const idToken = await webflow.getIdToken();

    const response = await fetch('/api/auth', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idToken })
    });

    if (response.ok) {
      const user = await response.json();
      await webflow.notify({ type: 'Success', message: `Welcome, ${user.firstName}!` });
      return user;
    }
  } catch (error) {
    await webflow.notify({ type: 'Error', message: 'Authentication failed' });
  }
}
```

## Best Practices

1. **Subscribe to events**: Keep extension state synced with the Designer
2. **Size appropriately**: Use the smallest size that works; resize only when needed, then return to a smaller size
3. **Notify users**: Provide feedback for completed actions, errors, and tips
4. **Handle launch context**: Show relevant UI based on how the user launched the extension
5. **Clean up subscriptions**: Always call the unsubscribe function when no longer needed
6. **Refresh tokens**: ID tokens expire after 15 minutes; refresh before making authenticated requests
