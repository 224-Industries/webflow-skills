---
name: "Variables API"
description: "Reference for design token variables including colors, sizes, fonts, numbers, and percentages organized in collections."
tags: [variables, design-tokens, collections, getDefaultVariableCollection, getAllVariableCollections, getVariableCollectionById, createVariableCollection, createColorVariable, createSizeVariable, createFontFamilyVariable, createNumberVariable, createPercentageVariable, getVariableByName, getVariable, getAllVariables, getBinding, set, setName, CustomValue, SizeValue, variable-modes, calc, clamp, min, max, color-mix, color, size, font-family, number, percentage, design-system]
---

# Variables API Reference

Variables are reusable design tokens for colors, sizes, fonts, numbers, and percentages. Changes to a variable propagate everywhere it's used.

## Table of Contents

- [Variable Collections](#variable-collections)
- [Variable Types](#variable-types)
- [Getting Variables](#getting-variables)
- [Updating Variables](#updating-variables)
- [Variable Binding](#variable-binding)
- [Custom Values and CSS Functions](#custom-values-and-css-functions)
- [Variable Modes](#variable-modes)
- [Using Variables in Styles](#using-variables-in-styles)
- [Workflow Examples](#workflow-examples)
- [Best Practices](#best-practices)

---

## Variable Collections

Collections organize related variables into logical groups.

### Get Default Collection
```typescript
const collection = await webflow.getDefaultVariableCollection();
```

### Get All Collections
```typescript
const collections = await webflow.getAllVariableCollections();
```

### Get Collection by ID
```typescript
const collection = await webflow.getVariableCollectionById('collection-4a393cee-14d6-d927-f2af-44169031a25');
```

### Create Collection
```typescript
const collection = await webflow.createVariableCollection("Brand Colors");
```

## Variable Types

### Color Variables

```typescript
collection.createColorVariable(
  name: string,
  value: string | ColorVariable | CustomValue,
  options?: { mode?: VariableMode }
): Promise<ColorVariable>
```

Accepts color names, RGB hex, and RGBA hex values.

```typescript
const collection = await webflow.getDefaultVariableCollection();

const brandBlue = await collection.createColorVariable('Brand Blue', '#146EF5');
const textDark = await collection.createColorVariable('Text Dark', '#1E1E1E');

// Reference another color variable
const linkColor = await collection.createColorVariable('Link Color', brandBlue);
```

### Size Variables

```typescript
collection.createSizeVariable(
  name: string,
  value: SizeValue | SizeVariable | CustomValue,
  options?: { mode?: VariableMode }
): Promise<SizeVariable>
```

Value uses the `SizeValue` object format `{ unit: SizeUnit, value: number }`.

```typescript
const spacingMd = await collection.createSizeVariable('Spacing Medium', { unit: 'px', value: 16 });
const borderRadius = await collection.createSizeVariable('Border Radius', { unit: 'rem', value: 0.5 });

// Reference another size variable
const spacingLg = await collection.createSizeVariable('Spacing Large', spacingMd);
```

#### Supported Size Units

| Category | Units |
|----------|-------|
| Absolute | `px` |
| Relative | `em`, `rem`, `ch` |
| Viewport | `vh`, `vw`, `vmin`, `vmax` |
| Dynamic Viewport | `dvh`, `dvw`, `svh`, `svw`, `lvh`, `lvw` |

### Font Family Variables

```typescript
collection.createFontFamilyVariable(
  name: string,
  value: string | FontFamilyVariable,
  options?: { mode?: VariableMode }
): Promise<FontFamilyVariable>
```

```typescript
const headingFont = await collection.createFontFamilyVariable('Heading Font', 'Inter');
const bodyFont = await collection.createFontFamilyVariable('Body Font', 'system-ui');

// Reference another font variable
const altFont = await collection.createFontFamilyVariable('Alt Font', headingFont);
```

### Number Variables

```typescript
collection.createNumberVariable(
  name: string,
  value: number | NumberVariable | CustomValue,
  options?: { mode?: VariableMode }
): Promise<NumberVariable>
```

```typescript
const columns = await collection.createNumberVariable('Grid Columns', 12);
const opacity = await collection.createNumberVariable('Card Opacity', 0.95);
```

### Percentage Variables

```typescript
collection.createPercentageVariable(
  name: string,
  value: number | PercentageVariable | CustomValue,
  options?: { mode?: VariableMode }
): Promise<PercentageVariable>
```

```typescript
const containerWidth = await collection.createPercentageVariable('Container Width', 80);
const overlayOpacity = await collection.createPercentageVariable('Overlay Opacity', 50);
```

## Getting Variables

### Get Variable by Name
```typescript
const variable = await collection.getVariableByName('Brand Blue');
```

### Get Variable by ID
```typescript
const variable = await collection.getVariable('variable-81b8fa46-aa26-f1ef-e265-a87ef3be63a5');
```

### Get All Variables in Collection
```typescript
const variables = await collection.getAllVariables();
```

## Updating Variables

```typescript
// Update color
await brandBlue.set('#0052CC');

// Update size
await spacingMd.set({ unit: 'px', value: 20 });

// Update font
await headingFont.set('Poppins');

// Rename a variable
await brandBlue.setName('Primary Blue');
```

## Variable Binding

Use `getBinding()` to get the CSS `var()` reference for a variable. This is needed when building custom value expressions that reference other variables.

```typescript
const binding = await brandBlue.getBinding();
// Returns: "var(--brand-blue)"

// Use in a custom value expression
const lightBlue = await collection.createColorVariable('Light Blue', {
  type: 'custom',
  value: `color-mix(in srgb, ${binding}, white 50%)`
});
```

## Custom Values and CSS Functions

All variable types that accept `CustomValue` support CSS functions via the `{ type: "custom", value: string }` format.

### Supported CSS Functions

| Function | Description | Example |
|----------|-------------|---------|
| `calc()` | Mathematical calculations | `calc(100vh - 80px)` |
| `clamp()` | Fluid values with min/max bounds | `clamp(1rem, 2vw, 2rem)` |
| `min()` | Smallest of multiple values | `min(100%, 600px)` |
| `max()` | Largest of multiple values | `max(50px, 5vw)` |
| `color-mix()` | Blend colors | `color-mix(in srgb, #146EF5, white 75%)` |

```typescript
// Fluid heading size
const h1Size = await collection.createSizeVariable('h1-font-size', {
  type: 'custom',
  value: 'clamp(1rem, 2vw, 2rem)'
});

// Computed number
const computedNum = await collection.createNumberVariable('Computed', {
  type: 'custom',
  value: 'clamp(1, 2, 2)'
});

// Blended color
const binding = await brandBlue.getBinding();
const lightBrand = await collection.createColorVariable('Light Brand', {
  type: 'custom',
  value: `color-mix(in srgb, ${binding}, white 75%)`
});
```

## Variable Modes

All creation methods accept an optional `mode` parameter for specifying which variable mode the value applies to. Retrieve a mode using `collection.getVariableModeByName()`.

```typescript
const mode = await collection.getVariableModeByName('Dark');
const bgColor = await collection.createColorVariable('Background', '#1E1E1E', { mode });
```

## Using Variables in Styles

```typescript
const collection = await webflow.getDefaultVariableCollection();
const primaryColor = await collection.createColorVariable('Primary', '#146EF5');
const fontSize = await collection.createSizeVariable('Body Size', { unit: 'px', value: 16 });

const style = await webflow.createStyle('Card');
await style.setProperties({
  'background-color': primaryColor,
  'font-size': fontSize,
  'padding-top': '20px',
  'padding-bottom': '20px',
  'padding-left': '20px',
  'padding-right': '20px',
});

const element = await webflow.getSelectedElement();
if (element) {
  await element.setStyles([style]);
}
```

## Workflow Examples

### Design System Setup

Creates a full set of design tokens for colors, spacing, and typography.

```typescript
async function setupDesignSystem() {
  const collection = await webflow.getDefaultVariableCollection();

  // Colors
  const colors = {
    primary: '#146EF5',
    secondary: '#6B7280',
    success: '#10B981',
    warning: '#F59E0B',
    error: '#EF4444',
    background: '#FFFFFF',
    surface: '#F3F4F6',
    textPrimary: '#111827',
    textSecondary: '#6B7280',
  };

  for (const [name, value] of Object.entries(colors)) {
    await collection.createColorVariable(name, value);
  }

  // Spacing
  const spacing = {
    'spacing-xs': 4,
    'spacing-sm': 8,
    'spacing-md': 16,
    'spacing-lg': 24,
    'spacing-xl': 32,
  };

  for (const [name, value] of Object.entries(spacing)) {
    await collection.createSizeVariable(name, { unit: 'px', value });
  }

  // Typography
  await collection.createFontFamilyVariable('font-heading', 'Inter');
  await collection.createFontFamilyVariable('font-body', 'Inter');

  await webflow.notify({ type: 'Success', message: 'Design system created!' });
}
```

### Create Fluid Typography Scale

Uses `clamp()` custom values to create responsive font size variables.

```typescript
async function createFluidTypography() {
  const collection = await webflow.getDefaultVariableCollection();

  const scale = [
    { name: 'text-sm', value: 'clamp(0.75rem, 1vw, 0.875rem)' },
    { name: 'text-base', value: 'clamp(0.875rem, 1.5vw, 1rem)' },
    { name: 'text-lg', value: 'clamp(1rem, 2vw, 1.25rem)' },
    { name: 'text-xl', value: 'clamp(1.25rem, 2.5vw, 1.5rem)' },
    { name: 'text-2xl', value: 'clamp(1.5rem, 3vw, 2rem)' },
  ];

  for (const { name, value } of scale) {
    await collection.createSizeVariable(name, { type: 'custom', value });
  }

  await webflow.notify({ type: 'Success', message: `Created ${scale.length} fluid type sizes` });
}
```

### Generate Color Tints from a Base Variable

Uses `getBinding()` and `color-mix()` to create lighter tints from an existing color variable.

```typescript
async function generateColorTints() {
  const collection = await webflow.getDefaultVariableCollection();
  const base = await collection.getVariableByName('primary');

  if (!base) {
    await webflow.notify({ type: 'Error', message: 'Variable "primary" not found' });
    return;
  }

  const binding = await base.getBinding();
  const tints = [25, 50, 75, 90];

  for (const pct of tints) {
    await collection.createColorVariable(`primary-${pct}`, {
      type: 'custom',
      value: `color-mix(in srgb, ${binding}, white ${pct}%)`,
    });
  }

  await webflow.notify({ type: 'Success', message: `Created ${tints.length} color tints` });
}
```

## Best Practices

1. **Use semantic names**: Name variables by purpose, not value (e.g., `"Primary Color"` not `"Blue"`)
2. **Organize by collection**: Group related variables into collections (colors, spacing, typography)
3. **Use the SizeValue object format**: Pass `{ unit, value }` instead of strings for size variables
4. **Leverage custom values for fluid design**: Use `clamp()` and `calc()` for responsive tokens
5. **Reference variables instead of duplicating**: Pass an existing variable as the value to keep tokens linked
