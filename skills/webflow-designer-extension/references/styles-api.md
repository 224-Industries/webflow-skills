---
name: "Styles API"
description: "Reference for creating, applying, and managing CSS styles/classes with support for responsive breakpoints and pseudo-states."
tags: [styles, css, classes, createStyle, getStyleByName, getAllStyles, removeStyle, setProperty, setProperties, getProperty, getProperties, removeProperty, removeProperties, removeAllProperties, setStyles, getStyles, isComboClass, combo-class, breakpoints, pseudo-states, hover, active, focus, pressed, visited, focus-visible, focus-within, placeholder, responsive, breakpoint, xxl, xl, large, main, medium, small, tiny]
---

# Styles API Reference

Styles (called "Classes" in the Designer) save styling that can be reused across elements.

## Table of Contents

- [Getting Styles](#getting-styles)
- [Creating and Removing Styles](#creating-and-removing-styles)
- [Managing Style Properties](#managing-style-properties)
- [Managing Style Variables](#managing-style-variables)
- [Responsive Styling](#responsive-styling)
- [Element Styles](#element-styles)
- [Breakpoint Reference](#breakpoint-reference)
- [Pseudo-State Reference](#pseudo-state-reference)
- [Workflow Examples](#workflow-examples)
- [Best Practices](#best-practices)

---

## Getting Styles

```typescript
// By name
const style = await webflow.getStyleByName("MyStyle");

// All styles
const allStyles = await webflow.getAllStyles();
```

## Creating and Removing Styles

```typescript
// Names must be unique across project
const style = await webflow.createStyle("MyStyle");

// Create a combo class by passing a parent
const parentStyle = await webflow.getStyleByName("ParentStyle");
const comboStyle = await webflow.createStyle("ComboStyle", { parent: parentStyle });

// Check if combo class
const isComboClass = await comboStyle.isComboClass();

await webflow.removeStyle(style);
```

## Managing Style Properties

All properties must be valid CSS properties and long-form names (e.g. `background-color` instead of `background`).

### Get Properties
```typescript
const allProperties = await style.getProperties();
const hoverProps = await style.getProperties({ pseudo: 'hover' });
const medBreakpointProps = await style.getProperties({ breakpoint: 'medium' });
```

### Get Single Property
```typescript
const bgColor = await style.getProperty("background-color");
```

### Set Single Property
```typescript
await style.setProperty("background-color", "blue");
```

### Set Multiple Properties
```typescript
const propertyMap : PropertyMap = {
  'background-color': '#146EF5',
  'font-size': '16px',
  'font-weight': 'bold',
  'padding': '20px 30px',
};
const options = { breakpoint: 'medium', pseudo: 'hover' } as BreakpointAndPseudo; // options are not required
await style.setProperties(propertyMap, options);
```

### Remove Single Property
```typescript
await style.removeProperty("background-color");
```

### Remove Multiple Properties
```typescript
const properties : StyleProperty[] = ['background-color', 'accent-color',"font-family"]
await style.removeProperties({properties});
```

### Remove All Properties
```typescript
await style.removeAllProperties();
```

## Managing Style Variables

See [Variables API Reference](./variables-api.md) for managing style variables, which can be used within style properties for dynamic theming and design systems.

## Responsive Styling

### Breakpoint-Specific
```typescript
await style.setProperties(
  { 'font-size': '24px' },
  { breakpoint: 'large' }
);

await style.setProperties(
  { 'font-size': '18px' },
  { breakpoint: 'medium' }
);

await style.setProperties(
  { 'font-size': '14px' },
  { breakpoint: 'small' }
);
```

### Pseudo-State Styling
```typescript
await style.setProperty(
  'background-color', 
  '#187CD9',
  { pseudo: 'hover' }
);

await style.setProperty(
  'opacity',
  '0.8',
  { pseudo: 'active' }
);
```

### Combined Breakpoint + Pseudo
```typescript
await style.setProperties(
  { 'font-size': '12px', 'padding': '10px' },
  { breakpoint: 'medium', pseudo: 'hover' }
);
```

## Element Styles

### Applying Style to Element

```typescript
const element = await webflow.getSelectedElement();
await element.setStyles([style]);
```

### Getting Element Styles

```typescript
const styles = await element.getStyles();
```

See [Elements API Reference](./elements-api.md) for more on working with elements.

## Breakpoint Reference

```typescript
type BreakpointId = "xxl" | "xl" | "large" | "main" | "medium" | "small" | "tiny"
```

| ID | Description |
|----|-------------|
| `xxl` | Very large screens / high-res monitors |
| `xl` | Large desktop monitors |
| `large` | Standard desktop monitors |
| `main` | Default breakpoint, smaller desktops |
| `medium` | Tablets and large phones |
| `small` | Larger mobile devices |
| `tiny` | Smallest mobile devices |

## Pseudo-State Reference

```typescript
type PseudoStateKey = "noPseudo" | "nth-child(odd)" | "nth-child(even)" | 
  "first-child" | "last-child" | "hover" | "active" | "pressed" | 
  "visited" | "focus" | "focus-visible" | "focus-within" | 
  "placeholder" | "empty" | "before" | "after"
```

| Key | Designer Name | Use Case |
|-----|--------------|----------|
| `hover` | Hover | Mouse over |
| `pressed` | Pressed | Click/tap active |
| `visited` | Visited | Visited links |
| `focus` | Focused | Keyboard/input focus |
| `focus-visible` | Focused (Keyboard) | Keyboard focus indicator |
| `focus-within` | -- | Element or descendant has focus |
| `placeholder` | Placeholder | Form input placeholders |
| `first-child` | First Item | First collection item |
| `last-child` | Last Item | Last collection item |
| `nth-child(odd)` | Odd Items | Odd collection items |
| `nth-child(even)` | Even Items | Even collection items |

## Workflow Examples

### Create and Apply a Button Style

Creates a reusable button style with hover state and applies it to the selected element.

```typescript
async function createButtonStyle() {
  const selected = await webflow.getSelectedElement();
  if (!selected) {
    await webflow.notify({ type: 'Error', message: 'Select an element' });
    return;
  }

  const style = await webflow.createStyle("PrimaryButton");

  await style.setProperties({
    'background-color': '#146EF5',
    'color': '#ffffff',
    'padding-top': '12px',
    'padding-bottom': '12px',
    'padding-left': '24px',
    'padding-right': '24px',
    'border-radius': '8px',
    'font-weight': '600',
    'font-size': '16px',
  });

  await style.setProperties(
    { 'background-color': '#0F5BD1' },
    { pseudo: 'hover' }
  );

  await selected.setStyles([style]);
  await webflow.notify({ type: 'Success', message: 'Button style applied' });
}
```

### Create Responsive Typography

Sets font sizes across multiple breakpoints for a heading style.

```typescript
async function createResponsiveHeadingStyle() {
  const style = await webflow.createStyle("ResponsiveHeading");

  await style.setProperties({
    'font-size': '48px',
    'font-weight': '700',
    'line-height': '1.2',
  });

  await style.setProperties(
    { 'font-size': '36px' },
    { breakpoint: 'medium' }
  );

  await style.setProperties(
    { 'font-size': '28px' },
    { breakpoint: 'small' }
  );

  await style.setProperties(
    { 'font-size': '24px' },
    { breakpoint: 'tiny' }
  );

  const selected = await webflow.getSelectedElement();
  if (selected) {
    await selected.setStyles([style]);
  }

  await webflow.notify({ type: 'Success', message: 'Responsive heading style created' });
}
```

### Apply a Shared Style to Multiple Elements

Finds all Heading elements and applies the same style to each one.

```typescript
async function applyStyleToAllHeadings() {
  const style = await webflow.getStyleByName("SectionHeading");
  if (!style) {
    await webflow.notify({ type: 'Error', message: 'Style "SectionHeading" not found' });
    return;
  }

  const elements = await webflow.getAllElements();
  const headings = elements.filter((el) => el.type === 'Heading');

  for (const heading of headings) {
    await heading.setStyles([style]);
  }

  await webflow.notify({ type: 'Success', message: `Styled ${headings.length} headings` });
}
```

## Best Practices

1. **Use long-form CSS property names**: Always use `background-color` instead of `background`, `padding-top` instead of `padding`, etc.
2. **Choose descriptive style names**: Names must be unique across the project — use semantic names like `"PrimaryButton"` or `"CardWrapper"`
3. **Set base styles on the main breakpoint first**: Define core properties without a breakpoint option, then override for smaller screens
4. **Reuse styles across elements**: Retrieve existing styles with `getStyleByName` rather than creating duplicates
5. **Keep hover and focus states accessible**: Ensure interactive states have sufficient contrast and visible focus indicators