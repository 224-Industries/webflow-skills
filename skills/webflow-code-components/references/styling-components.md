---
name: "Styling Components"
description: "How to style code components within Shadow DOM: site variables, inherited CSS properties, tag selectors, global styles, CSS modules, and what works vs. doesn't in Shadow DOM."
tags: [styling, css, shadow-dom, site-variables, tag-selectors, inherited-properties, global-styles, css-modules]
---

# Styling Components

Imported components support standard React styling approaches, but with important considerations for Shadow DOM isolation.

---

## How Shadow DOM Affects Styling

Code components render in Shadow DOM, which creates an isolated styling boundary. This means:

- Your component styles won't affect the rest of the page
- Page styles won't affect your component
- You need to explicitly connect to external styles

Rendering components in Shadow DOM prevents style conflicts to ensure your component looks and behaves as expected. However, this also means you need to explicitly connect to external styles like site variables, inherited properties, or tag selectors.

## Adding Styles to Your Code Components

To ensure your code components are styled correctly, you can import your styles directly into your `.webflow.tsx` file.

```tsx
// Button.webflow.tsx
import { props } from '@webflow/data-types';
import { declareComponent } from '@webflow/react';
import { Button } from './Button';
```

### Adding Global Styles

If you want to apply styles across all components, you can import your styles into a global decorators file.

```typescript
// globals.ts
import "./globals.css";
```

```css
/* globals.css */
:root {
  --primary-color: #007bff;
  --font-family: system-ui, sans-serif;
}
```

Then reference it in your `webflow.json`. Once applied, all components will inherit the styles from the global CSS file.

```json
{
  "library": {
    "globals": "./src/globals.ts"
  }
}
```

## CSS Capabilities

The following table shows which CSS features work within Shadow DOM:

| Feature | Works in Shadow DOM | How to use |
|---------|---------------------|------------|
| Site variables | Yes | `var(--background-primary, fallback)` |
| Inherited properties | Yes | `font-family: inherit` |
| Tag selectors | Yes | Enable with `applyTagSelectors: true` |
| Site classes | No | Use component-specific classes |

### Site Variables

Reference a site's variables in your components:

```css
/* Button.module.css */
.button {
  color: var(--background-primary, #000);
}
```

To get the exact variable name, click "Copy CSS" in the three-dot menu next to any variable in the Variables panel.

### Inherited Properties

CSS properties set to `inherit` work across Shadow DOM boundaries. Your component inherits styles from the parent HTML element:

```css
/* Button.module.css */
.button {
  color: var(--background-primary, #000);
  font-family: inherit;
}
```

For example, if your component is placed inside a `<div>` with `font-family: sans-serif`, setting `font-family: inherit` in your component will use sans-serif.

### Tag Selectors

Tag selectors (like `h1`, `p`, `button`) defined in your site's CSS can be automatically applied to your component. Enable this with the `applyTagSelectors` option in your component definition file.

```tsx
// Button.webflow.tsx
import { declareComponent } from '@webflow/react';
import { Button } from './Button';

export default declareComponent(Button, {
  name: 'Button',
  options: {
    applyTagSelectors: true,
  },
});
```

## Advanced Configuration

Code components support modern CSS frameworks and libraries, but some require specific configuration for Shadow DOM compatibility.

## Best Practices

- Import global styles once in a decorators file rather than in each component definition
- Always provide CSS variable fallback values (e.g., `var(--color-primary, #000)`) for resilience
- Use `inherit` for typography properties to match the surrounding page design
- Enable `applyTagSelectors` only when you want site-level tag styles to affect your component
- Use CSS Modules or scoped class names to avoid conflicts within your component
