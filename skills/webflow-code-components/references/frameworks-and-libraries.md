---
name: "Frameworks & Libraries"
description: "Configuration guides for CSS frameworks (Tailwind, Sass, Less), CSS-in-JS libraries (styled-components, Emotion), and component libraries (Material UI, Shadcn/UI) within Shadow DOM."
tags: [frameworks, libraries, tailwind, styled-components, emotion, material-ui, shadcn, sass, less, shadow-dom, decorators, css-in-js, webpack]
---

# Frameworks & Libraries

Code components run inside Shadow DOM, which means tools that inject styles into `document.head` require extra configuration. Webflow provides utility packages for CSS-in-JS libraries to inject styles directly into the Shadow Root.

---

## CSS Frameworks

### Tailwind CSS

Install Tailwind and its PostCSS plugin:

```bash
npm install tailwindcss @tailwindcss/postcss postcss
```

Create a PostCSS config:

```javascript
// postcss.config.mjs
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

Create a CSS file that imports Tailwind:

```css
/* globals.css */
@import "tailwindcss";
```

Import it in your globals file and reference it in `webflow.json`:

```typescript
// globals.ts
import "./globals.css";
```

```json
{
  "library": {
    "globals": "./src/globals.ts"
  }
}
```

Components can then use Tailwind utility classes directly. Global styles apply automatically to all components.

## CSS-in-JS Libraries

### styled-components

Install the Webflow utility and peer dependencies:

```bash
npm i @webflow/styled-components-utils
npm i styled-components react react-dom
```

Set up the global decorator to inject styles into Shadow DOM:

```typescript
// globals.ts
import { styledComponentsShadowDomDecorator } from "@webflow/styled-components-utils";

export const decorators = [styledComponentsShadowDomDecorator];
```

Reference the globals file in `webflow.json`:

```json
{
  "library": {
    "globals": "./src/globals.ts"
  }
}
```

The decorator automatically wraps all components, injecting styles into each Shadow Root.

### Emotion

Install the Webflow utility and peer dependencies:

```bash
npm i @webflow/emotion-utils
npm i @emotion/cache @emotion/react react react-dom
```

Set up the global decorator:

```typescript
// globals.ts
import { emotionShadowDomDecorator } from "@webflow/emotion-utils";

export const decorators = [emotionShadowDomDecorator];
```

Reference in `webflow.json` the same way as styled-components.

## Component Libraries

### Material UI

Material UI uses Emotion internally, so it follows the same Emotion setup:

```bash
npm i @webflow/emotion-utils
npm i @mui/material @emotion/react @emotion/cache
```

Use the `emotionShadowDomDecorator` global decorator. MUI components will then render correctly inside Shadow DOM.

### Shadcn/UI

Shadcn/UI is built on Tailwind CSS. Set up Tailwind first (see above), then add a path alias for the `@` import pattern:

```javascript
// webpack.webflow.js
module.exports = {
  resolve: {
    alias: {
      "@": process.cwd(),
    },
  },
};
```

Reference the webpack config in `webflow.json`:

```json
{
  "library": {
    "bundleConfig": "./webpack.webflow.js"
  }
}
```

## CSS Preprocessors

### Sass

Install Sass and its webpack loader:

```bash
npm install --save-dev sass sass-loader
```

Add a webpack override to handle `.scss` files:

```javascript
// webpack.webflow.js
module.exports = {
  module: {
    rules: (currentRules) => {
      return [
        ...currentRules,
        {
          test: /\.scss$/i,
          use: ["style-loader", "css-loader", "sass-loader"],
        },
      ];
    },
  },
};
```

Reference `bundleConfig` in `webflow.json` and import `.scss` files directly in your component definition files.

### Less

Install Less and its webpack loader:

```bash
npm install --save-dev less less-loader
```

Same webpack pattern as Sass, targeting `.less` files:

```javascript
// webpack.webflow.js
module.exports = {
  module: {
    rules: (currentRules) => {
      return [
        ...currentRules,
        {
          test: /\.less$/i,
          use: ["style-loader", "css-loader", "less-loader"],
        },
      ];
    },
  },
};
```

## Compatibility Summary

| Tool | Mechanism | Configuration |
|------|-----------|---------------|
| Tailwind CSS | PostCSS | Globals import |
| styled-components | CSS-in-JS | Shadow DOM decorator (`@webflow/styled-components-utils`) |
| Emotion | CSS-in-JS | Shadow DOM decorator (`@webflow/emotion-utils`) |
| Material UI | Emotion-based | Shadow DOM decorator (`@webflow/emotion-utils`) |
| Shadcn/UI | Tailwind-based | Tailwind setup + path alias in webpack |
| Sass | Webpack loader | Custom webpack config |
| Less | Webpack loader | Custom webpack config |

## Troubleshooting

- **Styles not rendering:** CSS-in-JS libraries inject styles into `document.head` by default, which won't reach Shadow DOM. Use the appropriate Webflow decorator to redirect style injection.
- **Errors when sharing:** Ensure the Webflow CLI is installed locally within the project. If a global installation exists, use `npx` to guarantee the correct version runs.

## Best Practices

- Use global decorators for CSS-in-JS libraries so all components automatically get Shadow DOM style injection
- Set up Tailwind via the globals file rather than importing in each component definition
- Always reference custom webpack configs via `bundleConfig` in `webflow.json`
- Test locally with `npx webflow library bundle` after adding framework configuration to catch build issues early
