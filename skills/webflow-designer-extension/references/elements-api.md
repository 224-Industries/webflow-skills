---
name: "Elements API"
description: "Reference for element selection, insertion, removal, properties, presets, and the element builder for bulk operations."
tags: [elements, getSelectedElement, getAllElements, setSelectedElement, after, before, append, prepend, remove, children, textContent, setTextContent, getTextContent, setStyles, getStyles, elementPresets, elementBuilder, DivBlock, Section, Container, Grid, VFlex, HFlex, Paragraph, Heading, Image, Link, DOM, setTag, setAttribute, custom-html, element-type, element-id]
---

# Elements API Reference

## Element Selection

### Get Selected Element
```typescript
const el = await webflow.getSelectedElement();
// Returns: Element | null
```

### Get All Elements
```typescript
const elements = await webflow.getAllElements();
// Returns: Element[]
```

### Set Selected Element
```typescript
await webflow.setSelectedElement(element);
```

### Get Children
```typescript
if (element.children) {
  const children = await element.children;
  await webflow.setSelectedElement(children[0]);
}
```

## Inserting Elements

### After (Sibling)
```typescript
const newEl = await element.after(webflow.elementPresets.DivBlock);
```

### Before (Sibling)
```typescript
const newEl = await element.before(webflow.elementPresets.Paragraph);
```

### Append (Last Child)
```typescript
if (element.children) {
  const child = await element.append(webflow.elementPresets.Image);
}
```

### Prepend (First Child)
```typescript
if (element.children) {
  const child = await element.prepend(webflow.elementPresets.Heading);
}
```

### Bulk Add with Element Builder
```typescript
const section = webflow.elementBuilder(webflow.elementPresets.DOM);
section.setTag("section");

const container = section.append(webflow.elementPresets.DOM);
container.setTag("div");
container.setAttribute("class", "container");

const heading = container.append(webflow.elementPresets.DOM);
heading.setTag("h2");

// Add entire structure at once
if (parent.children) {
  await parent.append(section);
}

// Set content after adding to canvas
const elements = await webflow.getAllElements();
const headingEl = elements.find(el => el.id.element === heading.id);
if (headingEl) await headingEl.setTextContent("Hello World");
```

## Removing Elements

```typescript
await element.remove();
```

## Element Presets

Access via `webflow.elementPresets`:

| Category | Presets |
|----------|---------|
| Layout | `DivBlock`, `Section`, `Container`, `Grid`, `VFlex`, `HFlex` |
| Text | `Paragraph`, `Heading`, `TextBlock`, `RichText`, `BlockQuote` |
| Media | `Image`, `Video`, `YouTube`, `Lottie` |
| Forms | `FormForm`, `FormInput`, `FormButton`, `FormTextarea`, `FormSelect`, `FormCheckbox`, `FormRadio` |
| Navigation | `Link`, `LinkBlock`, `NavBar`, `NavMenu` |
| Lists | `List`, `ListItem` |
| Components | `Tabs`, `Slider`, `Lightbox`, `Dropdown` |
| Custom | `DOM` (for custom HTML tags) |

## Custom DOM Elements

For elements without presets:

```typescript
const custom = webflow.elementBuilder(webflow.elementPresets.DOM);
custom.setTag("article");  // Any valid HTML tag
custom.setAttribute("class", "my-class");
custom.setAttribute("data-custom", "value");
```

## Element Properties

### Text Content
```typescript
if (element.textContent !== undefined) {
  await element.setTextContent("New text content");
  const text = await element.getTextContent();
}
```

### Styles
```typescript
await element.setStyles([style1, style2]);
const styles = await element.getStyles();
```

### Element Type
```typescript
console.log(element.type);
// e.g., "DivBlock", "Paragraph", "Image", "ComponentInstance"
```

### Element ID
```typescript
console.log(element.id);
// { element: "unique-id" }
```

## Image Element

```typescript
const img = await element.after(webflow.elementPresets.Image);
await img.setAsset(asset);  // Asset from createAsset()
await img.setAltText("Description");
```

## Link Element

```typescript
const link = await element.after(webflow.elementPresets.Link);
await link.setUrl("https://example.com");
await link.setTarget("_blank");
```

## Best Practices

1. **Always check capabilities:**
   ```typescript
   if (element.children) { /* can have children */ }
   if (element.textContent !== undefined) { /* has text */ }
   ```

2. **Handle null elements:**
   ```typescript
   const el = await webflow.getSelectedElement();
   if (!el) {
     await webflow.notify({ type: 'Error', message: 'Select an element' });
     return;
   }
   ```

3. **Use element builder for complex structures** to minimize API calls
