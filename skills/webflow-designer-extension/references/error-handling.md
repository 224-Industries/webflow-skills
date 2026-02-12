---
name: "Error Handling"
description: "Reference for Designer API error structure, cause tags, and patterns for graceful error recovery and user notifications."
tags: [errors, error-handling, try-catch, cause-tag, DuplicateValue, Forbidden, InternalError, InvalidElementPlacement, InvalidRequest, InvalidStyle, InvalidStyleName, InvalidStyleProperty, InvalidStyleVariant, InvalidTargetElement, PageCreateFailed, ResourceCreationFailed, ResourceMissing, ResourceRemovalFailed, VariableInvalid, notify, error-recovery, validation]
---

# Error Handling Reference

Designer API errors use a consistent structure with stable cause tags for programmatic handling.

## Table of Contents

- [Error Structure](#error-structure)
- [Error Cause Tags](#error-cause-tags)
- [Basic Error Handling](#basic-error-handling)
- [User Notification Pattern](#user-notification-pattern)
- [Common Error Scenarios](#common-error-scenarios)
- [Workflow Examples](#workflow-examples)
- [Best Practices](#best-practices)

---

## Error Structure

Designer API errors have two key properties:

```typescript
{
  cause: { tag: "ErrorTag" },  // Consistent, unchanging identifier
  message: "Human readable..."  // May change over time
}
```

> **Note**: Always use `err.cause.tag` for programmatic handling, not `err.message`.

## Error Cause Tags

| Tag | Description |
|-----|-------------|
| `DuplicateValue` | Value must be unique but already exists |
| `Forbidden` | User/app lacks permission (check App Modes) |
| `InternalError` | System error occurred |
| `InvalidElementPlacement` | Element cannot be placed in this location |
| `InvalidRequest` | Request invalid for current Designer state |
| `InvalidStyle` | Style is invalid or not recognized |
| `InvalidStyleName` | Style name doesn't exist or is incorrect |
| `InvalidStyleProperty` | Style property is invalid or not applicable |
| `InvalidStyleVariant` | Style variant is invalid or not recognized |
| `InvalidTargetElement` | Target element is invalid for operation |
| `PageCreateFailed` | Failed to create page |
| `ResourceCreationFailed` | Failed to create resource |
| `ResourceMissing` | Requested resource is missing or unavailable |
| `ResourceRemovalFailed` | Failed to remove resource (ensure no usages remain) |
| `VariableInvalid` | Variable value is invalid or out of expected range |

## Basic Error Handling

### Try/Catch Pattern
```typescript
try {
  const element = await webflow.getSelectedElement();
  if (!element) throw new Error('No element selected');
  await element.remove();
} catch (err) {
  console.error(`Tag: ${err.cause?.tag}`);
  console.error(`Message: ${err.message}`);
}
```

### Switch on Cause Tag
```typescript
function handleErrors(err) {
  switch (err.cause.tag) {
    case 'ResourceMissing':
      webflow.notify({ type: 'Error', message: 'The element no longer exists. Select a different element' });
      break;
    case 'InvalidElementPlacement':
      webflow.notify({ type: 'Error', message: 'The element cannot be placed here. Try another location' });
      break;
    default:
      webflow.notify({ type: 'Error', message: 'An error occurred. Please try again later' });
  }
}
```

## User Notification Pattern

Map error tags to user-friendly messages:

```typescript
async function handleError(err: any) {
  const messages: Record<string, string> = {
    'ResourceMissing': 'Element no longer exists. Select another.',
    'InvalidElementPlacement': 'Cannot place element here. Try another location.',
    'DuplicateValue': 'Name already exists. Choose a unique name.',
    'Forbidden': 'Permission denied. Check your access level.',
    'InvalidStyle': 'Invalid style configuration.',
    'ResourceRemovalFailed': 'Cannot remove. Item may be in use.',
  };

  const message = messages[err.cause?.tag] || 'An error occurred. Please try again.';
  await webflow.notify({ type: 'Error', message });
}
```

Notification types available:

```typescript
await webflow.notify({ type: 'Success', message: 'Operation completed!' }); // Green
await webflow.notify({ type: 'Error', message: 'Something went wrong' });   // Red
await webflow.notify({ type: 'Info', message: 'Tip: Try selecting an element' }); // Blue
```

See [Extension Utilities](./extension-utilities.md) for more on notifications.

## Common Error Scenarios

### No Element Selected
```typescript
const el = await webflow.getSelectedElement();
if (!el) {
  await webflow.notify({ type: 'Error', message: 'Select an element first' });
  return;
}
```

### Element Can't Have Children
```typescript
if (!element.children) {
  await webflow.notify({
    type: 'Error',
    message: 'This element cannot contain children'
  });
  return;
}
```

### Duplicate Style Name
```typescript
try {
  const style = await webflow.createStyle('MyStyle');
} catch (err) {
  if (err.cause?.tag === 'DuplicateValue') {
    const style = await webflow.getStyleByName('MyStyle');
    // Use existing style
  } else {
    throw err;
  }
}
```

### Element Removed During Operation
```typescript
try {
  const styles = await element.getStyles();
} catch (err) {
  if (err.cause?.tag === 'ResourceMissing') {
    await webflow.notify({
      type: 'Error',
      message: 'Element was removed. Select another.'
    });
  }
}
```

## Workflow Examples

### Safe Operation Wrapper

Wraps any async operation with error handling and user notification.

```typescript
async function safeOperation(operation: () => Promise<void>) {
  try {
    await operation();
  } catch (err) {
    const messages: Record<string, string> = {
      'ResourceMissing': 'Resource no longer exists.',
      'InvalidElementPlacement': 'Cannot place element here.',
      'DuplicateValue': 'Name already exists.',
      'Forbidden': 'Permission denied.',
      'ResourceRemovalFailed': 'Cannot remove. Item may be in use.',
    };

    const message = messages[err.cause?.tag] || `Error: ${err.message}`;
    await webflow.notify({ type: 'Error', message });
  }
}

// Usage
await safeOperation(async () => {
  const el = await webflow.getSelectedElement();
  if (el) await el.remove();
});
```

### Create Style with Fallback

Attempts to create a style, falling back to the existing one if the name is taken.

```typescript
async function getOrCreateStyle(name: string) {
  try {
    return await webflow.createStyle(name);
  } catch (err) {
    if (err.cause?.tag === 'DuplicateValue') {
      const existing = await webflow.getStyleByName(name);
      if (existing) return existing;
    }
    await webflow.notify({ type: 'Error', message: `Failed to create style "${name}"` });
    return null;
  }
}
```

### Validate Before Inserting Elements

Checks element capabilities before attempting insertion, with targeted error recovery.

```typescript
async function insertChildElement(preset: ElementPreset) {
  const parent = await webflow.getSelectedElement();

  if (!parent) {
    await webflow.notify({ type: 'Error', message: 'Select a parent element first' });
    return null;
  }

  if (!parent.children) {
    await webflow.notify({ type: 'Error', message: 'Selected element cannot contain children' });
    return null;
  }

  try {
    const child = await parent.append(preset);
    await webflow.notify({ type: 'Success', message: 'Element inserted' });
    return child;
  } catch (err) {
    if (err.cause?.tag === 'InvalidElementPlacement') {
      await webflow.notify({ type: 'Error', message: 'This element type cannot be placed here' });
    } else if (err.cause?.tag === 'ResourceMissing') {
      await webflow.notify({ type: 'Error', message: 'Parent element was removed' });
    } else {
      await webflow.notify({ type: 'Error', message: 'Failed to insert element' });
    }
    return null;
  }
}
```

## Best Practices

1. **Always use try/catch**: Wrap API calls to prevent unhandled errors
2. **Check cause.tag**: Use stable error tags for logic, not message text
3. **Notify users**: Provide actionable feedback with `webflow.notify()`
4. **Validate before acting**: Check that the element exists and supports the operation before calling methods
5. **Handle gracefully**: Recover when possible (e.g., fall back to existing style), inform the user when not
6. **Log for debugging**: Console.log error details during development
