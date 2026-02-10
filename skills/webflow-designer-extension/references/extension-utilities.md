---
name: "Extension Utilities"
description: "Reference for site info, extension sizing, event subscriptions, notifications, app intents/connections, and user authentication."
tags: [utilities, getSiteInfo, setExtensionSize, closeExtension, getMediaQuery, subscribe, notify, getLaunchContext, getIdToken, setAppConnection, getAppConnections, removeAppConnection, events, selectedelement, currentpage, mediaquery, mode, notifications, app-intents, app-connections, authentication, jwt, site-info, breakpoint, resize, webflow-json]
---

# Extension Utilities API Reference

Utilities for managing extension behavior, responding to Designer events, and integrating with Webflow's discovery features.

## Table of Contents

- [Site Information & Settings](#site-information--settings)
- [User Events & Notifications](#user-events--notifications)
- [App Intents & Connections](#app-intents--connections)
- [User Authentication](#user-authentication)

---

## Site Information & Settings

### Get Site Info

Retrieve metadata about the current site.

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
| `domains` | `Array<{url, lastPublished, default, stage}>` | Domain info |

**Example:**

```typescript
const siteInfo = await webflow.getSiteInfo();
console.log("Site:", siteInfo.siteName);
console.log("Workspace:", siteInfo.workspaceSlug);
console.log("Domains:", siteInfo.domains);
```

### Resize Extension

Dynamically resize the extension panel.

```typescript
await webflow.setExtensionSize(size);
```

**Parameters:**

| Size | Dimensions | Use Case |
|------|------------|----------|
| `"default"` | 240×360px | Simple apps |
| `"comfortable"` | 320×460px | Forms, more content |
| `"large"` | 800×600px | Complex workflows, previews |
| `{width, height}` | Custom | Min: 240×360, Max: 1200×800 |

**Example:**

```typescript
// Preset sizes
await webflow.setExtensionSize("comfortable");

// Custom size
await webflow.setExtensionSize({ width: 400, height: 500 });
```

### Close Extension

Programmatically close the extension.

```typescript
await webflow.closeExtension();
```

**Example:**

```typescript
// Close after completing an action
async function completeAndClose() {
  await performTask();
  await webflow.notify({ type: 'Success', message: 'Done!' });
  await webflow.closeExtension();
}
```

### Get Current Breakpoint

Retrieve the current responsive breakpoint in the Designer.

```typescript
const breakpoint = await webflow.getMediaQuery();
```

**Returns:** `"xxl" | "xl" | "large" | "main" | "medium" | "small" | "tiny"`

**Example:**

```typescript
const breakpoint = await webflow.getMediaQuery();
if (breakpoint === 'small' || breakpoint === 'tiny') {
  console.log("Mobile view active");
}
```

---

## User Events & Notifications

### Subscribe to Events

Listen for Designer events to keep your extension in sync.

```typescript
const unsubscribe = webflow.subscribe(eventName, callback);
```

**Available Events:**

| Event | Callback Parameter | Description |
|-------|-------------------|-------------|
| `"selectedelement"` | `Element \| null` | User selects different element |
| `"currentpage"` | `Page` | User switches pages |
| `"mediaquery"` | `BreakpointId` | User changes breakpoint |
| `"mode"` | `Mode` | Designer mode changes |

**Returns:** `() => void` - Unsubscribe function

**Examples:**

```typescript
// Track selected element
const unsubscribe = webflow.subscribe("selectedelement", (element) => {
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

```typescript
// Track mode changes (design/edit)
webflow.subscribe("mode", (mode) => {
  console.log("Mode:", mode);
});
```

### Send Notifications

Display in-Designer notifications to users.

```typescript
await webflow.notify({ type, message });
```

**Parameters:**

| Type | Appearance | Use Case |
|------|------------|----------|
| `"Success"` | Green | Completed actions |
| `"Error"` | Red | Failures, invalid input |
| `"Info"` | Blue | Tips, guidance |

**Examples:**

```typescript
// Success notification
await webflow.notify({ 
  type: 'Success', 
  message: 'Element created successfully!' 
});

// Error notification
await webflow.notify({ 
  type: 'Error', 
  message: 'Please select an element first.' 
});

// Info notification
await webflow.notify({ 
  type: 'Info', 
  message: 'Tip: Hold Shift to select multiple elements.' 
});
```

### Callback Best Practices

- **Keep lightweight**: Callbacks should execute quickly
- **Handle errors**: Include try/catch in callbacks
- **Clean up**: Unsubscribe when no longer needed
- **Avoid heavy operations**: Don't block the UI thread

---

## App Intents & Connections

Make your extension discoverable in element settings panels.

### Concepts

**App Intents**: Make your app appear in "Connect an App" when users interact with supported elements. Configured in `webflow.json`.

**App Connections**: Direct links between specific elements and your app. Users see your app in the element's settings panel.

### Supported Elements

Currently supported: `Image`, `FormForm`, `FormWrapper`

### Configure App Intents (webflow.json)

```json
{
  "appIntents": {
    "image": ["manage"],
    "form": ["manage"]
  }
}
```

### Configure App Connections (webflow.json)

```json
{
  "appConnections": ["manageImageElement", "manageFormElement"]
}
```

### Get Launch Context

Determine how your extension was launched.

```typescript
const context = await webflow.getLaunchContext();
```

**Returns:**

```typescript
// From App Intent
{ type: 'AppIntent', value: { image: 'manage' } }

// From App Connection
{ type: 'AppConnection', value: 'manageImageElement' }

// Direct launch (no context)
null
```

**Example:**

```typescript
const context = await webflow.getLaunchContext();

if (context?.type === 'AppIntent') {
  if (context.value?.image === 'manage') {
    // User wants to manage an image
    showImageManager();
  } else if (context.value?.form === 'manage') {
    // User wants to manage a form
    showFormManager();
  }
} else if (context?.type === 'AppConnection') {
  // Launched from existing connection
  switch (context.value) {
    case 'manageImageElement':
      showImageManager();
      break;
    case 'manageFormElement':
      showFormManager();
      break;
  }
} else {
  // Direct launch
  showHomePage();
}
```

### Set App Connection

Create a connection between an element and your app.

```typescript
await element.setAppConnection(connectionId);
```

**Example:**

```typescript
const element = await webflow.getSelectedElement();
if (element?.type === 'Image') {
  await element.setAppConnection('manageImageElement');
  await webflow.notify({ type: 'Success', message: 'Image connected!' });
}
```

### Get App Connections

Retrieve connections for an element.

```typescript
const connections = await element.getAppConnections();
```

**Example: Find all connected elements**

```typescript
async function findConnectedElements() {
  const elements = await webflow.getAllElements();
  const connected = [];
  
  for (const element of elements) {
    if (element.getAppConnections) {
      const connections = await element.getAppConnections();
      if (connections?.length > 0) {
        connected.push({ element, connections });
      }
    }
  }
  
  return connected;
}
```

### Remove App Connection

```typescript
await element.removeAppConnection(connectionId);
```

---

## User Authentication

Authenticate users for Data API access or personalized features.

### Get ID Token

Retrieve a JWT identifying the current user.

```typescript
const idToken = await webflow.getIdToken();
```

**Returns:** `string` - JWT valid for 15 minutes

**Token Resolution:**

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

**Use Cases:**

- Authenticate users with your backend
- Access Data API resources on behalf of the user
- Implement permission-based features
- Create personalized experiences

**Example:**

```typescript
async function authenticateUser() {
  try {
    const idToken = await webflow.getIdToken();
    
    // Send to backend for verification
    const response = await fetch('/api/auth', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idToken })
    });
    
    if (response.ok) {
      const user = await response.json();
      console.log('Authenticated:', user.email);
      return user;
    }
  } catch (error) {
    console.error('Authentication failed:', error);
  }
}
```

---

## Quick Reference

| Method | Description |
|--------|-------------|
| `webflow.getSiteInfo()` | Get site metadata |
| `webflow.setExtensionSize(size)` | Resize extension panel |
| `webflow.closeExtension()` | Close the extension |
| `webflow.getMediaQuery()` | Get current breakpoint |
| `webflow.subscribe(event, callback)` | Listen for Designer events |
| `webflow.notify(opts)` | Show user notification |
| `webflow.getLaunchContext()` | Get how extension was launched |
| `webflow.getIdToken()` | Get user authentication token |
| `element.setAppConnection(id)` | Create element connection |
| `element.getAppConnections()` | Get element connections |
| `element.removeAppConnection(id)` | Remove element connection |

---

## Best Practices

1. **Subscribe to events**: Keep extension state synced with Designer
2. **Size appropriately**: Use smallest size that works; resize only when needed
3. **Notify users**: Provide feedback for actions, errors, and tips
4. **Handle launch context**: Show relevant UI based on how user launched extension
5. **Clean up subscriptions**: Unsubscribe when component unmounts
6. **Refresh tokens**: ID tokens expire after 15 minutes; refresh as needed
