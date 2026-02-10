---
name: "Components API"
description: "Reference for creating component definitions, managing instances, and editing components in context."
tags: [components, registerComponent, createInstance, enterComponent, exitComponent, getRootElement, ComponentInstance, component-definition, component-instance, reusable-elements, component-context, component-editing, component-properties]
---

# Components API Reference

Components are reusable element blocks. A **Component Definition** is the blueprint; **Component Instances** are copies that can be customized.

## Key Concepts

- **Component Definition**: Blueprint defining structure and properties
- **Component Instance**: Copy of definition, can have custom property values
- **Component Properties**: Attributes that can be customized per instance (text, images, links)

> **Note**: Component property creation/management is not yet supported in the API.

## Creating a Component Definition

Register an element hierarchy as a component:

```typescript
// Get root element with child elements
const rootElement = await webflow.getSelectedElement();

if (rootElement) {
  const component = await webflow.registerComponent('Card Component', rootElement);
  console.log(`Component ID: ${component.id}`);
}
```

The root element and all its children become the component structure.

## Creating Component Instances

Add a component instance to the page:

```typescript
const instance = await webflow.createInstance(componentDefinition);
```

Instances can be nested within other elements or component instances.

## Editing Component Definitions

To modify a component definition, enter its context:

```typescript
const selectedElement = await webflow.getSelectedElement();

if (selectedElement && selectedElement.type === 'ComponentInstance') {
  // Enter component context
  await webflow.enterComponent(selectedElement);
  console.log('Entered component context');

  // Get root element of component
  const rootElement = await webflow.getRootElement();
  
  if (rootElement?.children) {
    // Add new element to component definition
    const newElement = await rootElement.append(webflow.elementPresets.DivBlock);
    console.log('Added element to component');
  }
}
```

Changes to the definition propagate to all instances.

## Exiting Component Context

```typescript
await webflow.exitComponent();
```

## Checking Element Type

```typescript
const element = await webflow.getSelectedElement();

if (element?.type === 'ComponentInstance') {
  // Handle component instance
}
```

## Workflow Example

### Create Component from Selection
```typescript
async function createComponentFromSelection(name: string) {
  const root = await webflow.getSelectedElement();
  
  if (!root) {
    await webflow.notify({ type: 'Error', message: 'Select an element first' });
    return null;
  }
  
  try {
    const component = await webflow.registerComponent(name, root);
    await webflow.notify({ type: 'Success', message: `Created "${name}" component` });
    return component;
  } catch (err) {
    await webflow.notify({ type: 'Error', message: 'Failed to create component' });
    return null;
  }
}
```

### Edit Selected Component
```typescript
async function editSelectedComponent() {
  const selected = await webflow.getSelectedElement();
  
  if (!selected || selected.type !== 'ComponentInstance') {
    await webflow.notify({ type: 'Error', message: 'Select a component instance' });
    return;
  }
  
  await webflow.enterComponent(selected);
  
  // Now in component editing mode
  const root = await webflow.getRootElement();
  // Make modifications...
  
  // Exit when done
  await webflow.exitComponent();
}
```

## Best Practices

1. **Plan structure first**: Design the element hierarchy before registering as component
2. **Use semantic naming**: Name components descriptively (e.g., "Hero Card", "Testimonial Block")
3. **Exit after editing**: Always call `exitComponent()` when done modifying
4. **Check element type**: Verify `type === 'ComponentInstance'` before entering
