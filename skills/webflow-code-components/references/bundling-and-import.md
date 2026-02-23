---
name: "Bundling and Import"
description: "How code components are bundled with Webpack and imported to Webflow via DevLink CLI. Covers CI/CD, bundle limits, debugging, CSS modules config, webpack overrides, and local bundling."
tags: [bundling, import, webpack, devlink, cli, cicd, bundle-limits, debugging, css-modules, webpack-config]
---

# Bundling and Import

This reference covers bundling your React components and importing them to Webflow.

---

## Import

Import your components to Webflow using DevLink. DevLink bundles your component files and uploads them to your Workspace as a shared library.

Use the following command to import your components to Webflow:

```bash
npx webflow library share
```

### CI/CD Pipelines

For automated workflows, add the `--no-input` flag to skip interactive prompts:

```bash
npx webflow library share --no-input
```

**Important:** Add change detection to prevent inadvertently removing components:

- Compare current library state with previous import
- Only share when components have actually changed

## Bundling

Webflow uses Webpack to bundle your component libraries. During this process, the bundler handles TypeScript compilation, resolves all dependencies and imports, optimizes your code for production, and generates bundles ready for import.

The default configuration handles most use cases automatically. Extend it when you need:

- **Custom CSS processing**
- **Specialized file handling** (SVG, images, fonts)
- **Build optimizations** (tree shaking, code splitting)

> **Note:** If you're using a CSS framework or component library, you may need to configure your project to handle the framework's CSS. See [Styling Components](styling-components.md) for more information.

### Bundle Limits

Maximum bundle size: **50MB**

## Overriding the Default Webpack Configuration

Create a `webpack.webflow.js` file and reference it in `webflow.json` via the `bundleConfig` property:

```json
{
  "library": {
    "name": "My Library",
    "components": ["./src/components/**/*.webflow.{js,ts,tsx}"],
    "bundleConfig": "./webpack.webflow.js"
  }
}
```

## Debugging

This section provides common debugging techniques for troubleshooting the bundling process and resolving configuration issues.

### Disable Minification

By default, the bundler minifies your code to reduce file size for production. To troubleshoot issues, you can disable minification in your webpack configuration.

This keeps your bundled code readable and ensures that any errors you see in the browser's developer console will have accurate line numbers that map back to your original source code.

```javascript
// webpack.webflow.js
module.exports = {
  mode: "development",
};
```

> **Warning:** When using a custom webpack configuration file, you must include the file in your `webflow.json` by passing the path in the `bundleConfig` property.

### CSS Modules

CSS Modules scope styles by generating unique class names, preventing conflicts between components.

By default, you must use bracket notation to access CSS classes:

```tsx
// Button.tsx
import * as styles from "./Button.module.css";

export const Button = (text: string) => {
  return (
    <a className={(styles as any)["my-button"]}>
      {text}
    </a>
  );
};
```

To enable dot notation and use the default import syntax for CSS modules, update the `css-loader` configuration:

```javascript
// webpack.webflow.js
module.exports = {
  module: {
    rules: (currentRules) => {
      return currentRules.map((rule) => {
        if (
          rule.test instanceof RegExp &&
          rule.test.test("test.css") &&
          Array.isArray(rule.use)
        ) {
          for (const [index, loader] of rule.use.entries()) {
            if (typeof loader === "object" && loader?.ident === "css-loader") {
              const options =
                typeof loader.options === "object" ? loader.options : {};
              rule.use[index] = {
                ...loader,
                options: {
                  ...options,
                  modules: {
                    exportLocalsConvention: "as-is",
                    namedExport: false,
                  },
                },
              };
            }
          }
        }
        return rule;
      });
    },
  },
};
```

## Bundle Locally

To test and debug your React components locally, you can bundle your library using the Webflow CLI command.

```bash
npx webflow library bundle --public-path http://localhost:4000/
```

The public path is the URL where you can serve your bundled library. The CLI will generate a `dist` folder with your bundled library.

To inspect the final configuration being used by webpack, use the `--debug-bundler` option.

## Best Practices

- Use `--no-input` in CI/CD pipelines to skip interactive prompts
- Add change detection before sharing to avoid accidentally removing components
- Keep bundle size well under the 50MB limit for faster uploads and installs
- Use `--debug-bundler` to inspect the final webpack configuration when troubleshooting
- Test bundles locally with `npx webflow library bundle` before sharing to production
