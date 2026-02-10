---
name: "Styles API"
description: "Reference for creating, applying, and managing CSS styles/classes with support for responsive breakpoints and pseudo-states."
tags: [styles, css, classes, createStyle, getStyleByName, getAllStyles, setProperty, setProperties, getProperty, getProperties, breakpoints, pseudo-states, hover, active, focus, responsive, media-query, typography, spacing, layout, flexbox, grid, background, border, box-shadow, transition, variables]
---

# Styles API Reference

Styles (called "Classes" in Designer) save styling that can be reused across elements.

## Creating Styles

```typescript
const style = await webflow.createStyle("MyStyle");
// Names must be unique across project
```

## Getting Styles

```typescript
// By name
const style = await webflow.getStyleByName("MyStyle");

// All styles
const allStyles = await webflow.getAllStyles();
```

## Setting Properties

### Single Property
```typescript
await style.setProperty("background-color", "blue");
await style.setProperty("font-size", "16px");
await style.setProperty("padding", "20px");
```

### Multiple Properties
```typescript
const propertyMap = {
  'background-color': '#146EF5',
  'font-size': '16px',
  'font-weight': 'bold',
  'padding': '20px 30px',
};
await style.setProperties(propertyMap);
```

### With Variables
```typescript
const collection = await webflow.getDefaultVariableCollection();
const brandColor = await collection?.createColorVariable('Brand', '#146EF5');

await style.setProperties({
  'background-color': brandColor,
  'font-size': '16px',
});
```

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

## Applying Styles

```typescript
const element = await webflow.getSelectedElement();
await element.setStyles([style]);

// Multiple styles (cascade)
await element.setStyles([baseStyle, modifierStyle]);
```

## Getting Element Styles

```typescript
const styles = await element.getStyles();
```

## Breakpoint Reference

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

## Common Style Properties

```typescript
// Typography
'font-family': 'Inter, sans-serif'
'font-size': '16px'
'font-weight': '400' | '600' | 'bold'
'line-height': '1.5'
'letter-spacing': '-0.02em'
'text-align': 'left' | 'center' | 'right'
'color': '#333333'

// Spacing
'margin': '20px'
'margin-top': '10px'
'padding': '20px 30px'
'padding-left': '15px'

// Layout
'display': 'flex' | 'grid' | 'block' | 'none'
'flex-direction': 'row' | 'column'
'justify-content': 'center' | 'space-between'
'align-items': 'center' | 'flex-start'
'gap': '20px'

// Sizing
'width': '100%' | '300px' | 'auto'
'max-width': '1200px'
'height': '100vh' | '200px'

// Background
'background-color': '#ffffff'
'background-image': 'url(...)'

// Border
'border': '1px solid #e0e0e0'
'border-radius': '8px'

// Effects
'box-shadow': '0 4px 6px rgba(0,0,0,0.1)'
'opacity': '0.9'
'transform': 'translateY(-2px)'
'transition': 'all 0.2s ease'
```

## Limitations

- Cannot style HTML tags (only CSS classes)
- Style names must be unique
- Duplicate names throw `DuplicateValue` error
