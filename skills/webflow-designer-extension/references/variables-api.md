---
name: "Variables API"
description: "Reference for design token variables including colors, sizes, fonts, numbers, and percentages organized in collections."
tags: [variables, design-tokens, getDefaultVariableCollection, getAllVariableCollections, createVariableCollection, createColorVariable, createSizeVariable, createFontFamilyVariable, createNumberVariable, createPercentageVariable, getVariableByName, getAllVariables, getColorVariables, getSizeVariables, getFontFamilyVariables, getValue, setValue, design-system, color, size, font-family, spacing, typography]
---

# Variables API Reference

Variables are reusable design tokens for colors, sizes, fonts, numbers, and percentages. Changes to a variable propagate everywhere it's used.

## Variable Collections

Collections organize related variables.

### Get Default Collection
```typescript
const collection = await webflow.getDefaultVariableCollection();
```

### Get All Collections
```typescript
const collections = await webflow.getAllVariableCollections();
```

### Create Collection
```typescript
const collection = await webflow.createVariableCollection("Brand Colors");
```

## Variable Types

### Color Variables
```typescript
const collection = await webflow.getDefaultVariableCollection();

// Create color variable
const brandBlue = await collection.createColorVariable('Brand Blue', '#146EF5');
const textDark = await collection.createColorVariable('Text Dark', '#1E1E1E');

// Use in styles
await style.setProperties({
  'background-color': brandBlue,
  'color': textDark
});
```

### Size Variables
```typescript
// Create size variable
const spacingMd = await collection.createSizeVariable('Spacing Medium', '16px');
const borderRadius = await collection.createSizeVariable('Border Radius', '8px');

// Use in styles
await style.setProperties({
  'padding': spacingMd,
  'border-radius': borderRadius
});
```

### Font Family Variables
```typescript
// Create font variable
const headingFont = await collection.createFontFamilyVariable('Heading Font', 'Inter');
const bodyFont = await collection.createFontFamilyVariable('Body Font', 'system-ui');

// Use in styles
await style.setProperty('font-family', headingFont);
```

### Number Variables
```typescript
// Create number variable (unitless)
const columns = await collection.createNumberVariable('Grid Columns', 12);
const opacity = await collection.createNumberVariable('Card Opacity', 0.95);
```

### Percentage Variables
```typescript
// Create percentage variable
const containerWidth = await collection.createPercentageVariable('Container Width', 80);
const overlayOpacity = await collection.createPercentageVariable('Overlay Opacity', 50);
```

## Getting Variables

### Get Variable by Name
```typescript
const variable = await collection.getVariableByName('Brand Blue');
```

### Get All Variables in Collection
```typescript
const variables = await collection.getAllVariables();
```

### Filter by Type
```typescript
const colorVars = await collection.getColorVariables();
const sizeVars = await collection.getSizeVariables();
const fontVars = await collection.getFontFamilyVariables();
```

## Updating Variables

```typescript
// Update color
await brandBlue.setValue('#0052CC');

// Update size
await spacingMd.setValue('20px');

// Update font
await headingFont.setValue('Poppins');
```

## Using Variables in Styles

```typescript
// Create variables
const collection = await webflow.getDefaultVariableCollection();
const primaryColor = await collection.createColorVariable('Primary', '#146EF5');
const fontSize = await collection.createSizeVariable('Body Size', '16px');

// Create style using variables
const style = await webflow.createStyle('Card');
await style.setProperties({
  'background-color': primaryColor,
  'font-size': fontSize,
  'padding': '20px'
});

// Apply to element
await element.setStyles([style]);
```

## Workflow Example: Design System Setup

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
    textSecondary: '#6B7280'
  };
  
  for (const [name, value] of Object.entries(colors)) {
    await collection.createColorVariable(name, value);
  }
  
  // Spacing
  const spacing = {
    'spacing-xs': '4px',
    'spacing-sm': '8px',
    'spacing-md': '16px',
    'spacing-lg': '24px',
    'spacing-xl': '32px'
  };
  
  for (const [name, value] of Object.entries(spacing)) {
    await collection.createSizeVariable(name, value);
  }
  
  // Typography
  await collection.createFontFamilyVariable('font-heading', 'Inter');
  await collection.createFontFamilyVariable('font-body', 'Inter');
  
  await webflow.notify({ type: 'Success', message: 'Design system created!' });
}
```

## Best Practices

1. **Use semantic names**: Name variables by purpose, not value (e.g., "Primary Color" not "Blue")
2. **Organize by collection**: Group related variables (colors, spacing, typography)
3. **Consistent naming**: Use consistent naming conventions (kebab-case or camelCase)
4. **Document variables**: Comment on intended use cases
5. **Update centrally**: Change variable values to update entire site
