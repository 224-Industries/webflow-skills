---
name: "Components API"
description: "Reference for creating component definitions, retrieving components, inserting instances, and editing components in context."
tags: [components, registerComponent, getAllComponents, enterComponent, exitComponent, getRootElement, getName, ComponentElement, ComponentInstance, component-definition, component-instance, before, after, append, prepend]
---

# Components API Reference

Components are reusable element blocks. A **Component Definition** is the blueprint; **Component Instances** are carbon-copies that retain the core design and structure of the definition.

## Table of Contents

- [Key Concepts](#key-concepts)
- [Retrieving Components](#retrieving-components)
- [Creating a Component Definition](#creating-a-component-definition)
- [Creating Component Instances](#creating-component-instances)
- [Editing Component Definitions](#editing-component-definitions)
- [Component Properties](#component-properties)
- [Workflow Examples](#workflow-examples)
- [Best Practices](#best-practices)

---

## Key Concepts

- **Component Definition**: Blueprint defining the structure of elements within a component
- **Component Instance** (`ComponentElement`): A copy of the definition placed on the canvas, customizable through properties
- **Component Properties**: Pre-defined attributes within a definition that can be assigned specific values per instance

> **Note**: Component property creation and management is not yet supported via the API.

## Retrieving Components

### Get All Components
```typescript
const components = await webflow.getAllComponents();
```

### Get Component Name
```typescript
const component = components[0];
const name = await component.getName();
```

### Get Component Root Element
```typescript
const root = await component.getRootElement();
```

### Get Component from an Instance

When you have a `ComponentInstance` element on the page, retrieve its definition via the Elements API:

```typescript
const element = await webflow.getSelectedElement();
if (element?.type === 'ComponentInstance') {
  const component = await element.getComponent();
  const name = await component.getName();
}
```

See the [Elements API Reference](./elements-api.md) for more on working with component instance elements.

## Creating a Component Definition

Register an element hierarchy as a reusable component:

```typescript
webflow.registerComponent(
  name: string,
  root: AnyElement | ElementPreset<AnyElement> | Component
): Promise<Component>
```

```typescript
const rootElement = await webflow.getSelectedElement();

if (rootElement) {
  const component = await webflow.registerComponent('Card Component', rootElement);
  console.log(`Component ID: ${component.id}`);
}
```

The root element and all its children become the component structure.

## Creating Component Instances

Component instances are created using the standard element insertion methods (`.before()`, `.after()`, `.append()`, `.prepend()`) with a `Component` object.

```typescript
const allComponents = await webflow.getAllComponents();
const cardComponent = allComponents[0];

const selected = await webflow.getSelectedElement();
if (selected) {
  // Insert as sibling
  await selected.before(cardComponent);
  await selected.after(cardComponent);
}

// Insert as child
if (selected?.children) {
  await selected.append(cardComponent);
  await selected.prepend(cardComponent);
}
```

## Editing Component Definitions

### Enter Component Context

Focus the Designer on a component definition for editing. Requires a `ComponentElement` instance on the page.

```typescript
webflow.enterComponent(
  instance: ComponentElement
): Promise<null>
```

```typescript
const selected = await webflow.getSelectedElement();
if (selected?.type === 'ComponentInstance') {
  await webflow.enterComponent(selected as ComponentElement);
}
```

### Get Root Element in Context

While inside a component context, get the root element of the component being edited:

```typescript
const root = await webflow.getRootElement();
```

> **Note**: When not inside a component context, `webflow.getRootElement()` returns the page `Body` element.

### Exit Component Context

Return the Designer focus to the page body:

```typescript
await webflow.exitComponent();
```

Changes made to the definition while in context propagate to all instances.

## Component Properties

Component properties (text, images, links) allow per-instance customization in the Designer UI.

> **Note**: Component property creation and management is not yet supported via the API. Properties can only be configured manually in the Webflow Designer.

## Workflow Examples

### Create Component from Selection

Registers the selected element and its children as a new component definition.

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

### Insert Component Instance by Name

Finds a component by name and inserts an instance after the selected element.

```typescript
async function insertComponentByName(componentName: string) {
  const selected = await webflow.getSelectedElement();
  if (!selected) {
    await webflow.notify({ type: 'Error', message: 'Select an element first' });
    return;
  }

  const components = await webflow.getAllComponents();
  let target: Component | null = null;

  for (const component of components) {
    const name = await component.getName();
    if (name === componentName) {
      target = component;
      break;
    }
  }

  if (!target) {
    await webflow.notify({ type: 'Error', message: `Component "${componentName}" not found` });
    return;
  }

  await selected.after(target);
  await webflow.notify({ type: 'Success', message: `Inserted "${componentName}" instance` });
}
```

### Edit Component and Add a Child Element

Enters a component's editing context, appends a new element, then exits.

```typescript
async function addElementToComponent() {
  const selected = await webflow.getSelectedElement();

  if (!selected || selected.type !== 'ComponentInstance') {
    await webflow.notify({ type: 'Error', message: 'Select a component instance' });
    return;
  }

  await webflow.enterComponent(selected as ComponentElement);

  const root = await webflow.getRootElement();
  if (root?.children) {
    const newElement = await root.append(webflow.elementPresets.Paragraph);
    await newElement.setTextContent('New paragraph added to component');
  }

  await webflow.exitComponent();
  await webflow.notify({ type: 'Success', message: 'Component updated' });
}
```

## Best Practices

1. **Plan structure first**: Design the element hierarchy before registering as a component
2. **Use semantic names**: Name components descriptively (e.g., `"Hero Card"`, `"Testimonial Block"`)
3. **Always exit after editing**: Call `exitComponent()` when done modifying a component definition
4. **Check element type before entering**: Verify `type === 'ComponentInstance'` before calling `enterComponent()`
5. **Use element insertion methods for instances**: Create instances with `.before()`, `.after()`, `.append()`, or `.prepend()` — not a dedicated create method
