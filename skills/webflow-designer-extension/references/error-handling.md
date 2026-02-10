---
name: "Error Handling"
description: "Reference for Designer API error structure, cause tags, and patterns for graceful error recovery and user notifications."
tags: [errors, error-handling, try-catch, cause-tag, DuplicateValue, Forbidden, InternalError, InvalidElementPlacement, InvalidRequest, InvalidStyle, InvalidStyleName, InvalidStyleProperty, InvalidStyleVariant, InvalidTargetElement, PageCreateFailed, ResourceCreationFailed, ResourceMissing, ResourceRemovalFailed, VariableInvalid, notify, error-recovery, validation]
---

# Error Handling Reference

## Error Structure

Designer API errors have two key properties:

```typescript
{
  cause: { tag: "ErrorTag" },  // Consistent, unchanging identifier
  message: "Human readable..."  // May change over time
}
```

Use `err.cause.tag` for programmatic handling, not `err.message`.

## Error Cause Tags

| Tag | Description |
|-----|-------------|
| `DuplicateValue` | Value must be unique but already exists |
| `Forbidden` | User/app lacks permission (check App Modes) |
| `InternalError` | System error occurred |
| `InvalidElementPlacement` | Element cannot be placed in this location |
| `InvalidRequest` | Request invalid for current Designer state |
| `InvalidStyle` | Style is invalid or not recognized |
| `InvalidStyleName` | Style name doesn't exist |
| `InvalidStyleProperty` | Style property is invalid |
| `InvalidStyleVariant` | Style variant is invalid |
| `InvalidTargetElement` | Target element is invalid for operation |
| `PageCreateFailed` | Failed to create page |
| `ResourceCreationFailed` | Failed to create resource |
| `ResourceMissing` | Requested resource not found |
| `ResourceRemovalFailed` | Failed to remove resource (may be in use) |
| `VariableInvalid` | Variable value is invalid |

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

## User Notification Pattern

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

## Full Error Handler Example

```typescript
async function safeOperation(operation: () => Promise<void>) {
  try {
    await operation();
  } catch (err) {
    await handleError(err);
  }
}

// Usage
await safeOperation(async () => {
  const el = await webflow.getSelectedElement();
  if (el) await el.remove();
});
```

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

## Notification Types

```typescript
// Success (green)
await webflow.notify({ type: 'Success', message: 'Operation completed!' });

// Error (red)
await webflow.notify({ type: 'Error', message: 'Something went wrong' });

// Info (blue)
await webflow.notify({ type: 'Info', message: 'Tip: Try selecting an element' });

// Warning (yellow)
await webflow.notify({ type: 'Warning', message: 'This may take a moment' });
```

## Best Practices

1. **Always use try/catch**: Wrap API calls to prevent unhandled errors
2. **Check cause.tag**: Use stable error tags for logic, not message text
3. **Notify users**: Provide actionable feedback with `webflow.notify()`
4. **Validate before acting**: Check element exists and supports operation
5. **Handle gracefully**: Recover when possible, inform user when not
6. **Log for debugging**: Console.log error details during development
