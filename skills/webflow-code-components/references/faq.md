---
name: "FAQ"
description: "Frequently asked questions about code components: setup, styling in Shadow DOM, imports, updates, state management, troubleshooting, performance, and advanced topics."
tags: [faq, troubleshooting, shadow-dom, styling, state-management, bundle-size, third-party-libraries, debugging, typescript, responsive]
---

# FAQ

Frequently asked questions about building, styling, importing, and troubleshooting Webflow code components.

---

## Getting Started

### How do I create my first code component?

1. Install the CLI globally (`npm install -g @webflow/webflow-cli`) and dependencies (`npm i --save-dev @webflow/react @webflow/data-types`)
2. Create a `.webflow.tsx` file that uses `declareComponent` to map your React component to Webflow
3. Run `npx webflow library share` to bundle and upload

See [Quick Start](quick-start.md) for a full walkthrough.

### Which frameworks are supported?

React with TypeScript. Code components support hooks, functional components, popular React libraries, and CSS-in-JS solutions. React Server Components are **not** supported.

### Is there a component count limit?

No strict limit on the number of components. Keep the total bundle under **50MB**.

## Development & Styling

### Why aren't my styles showing?

Components render inside Shadow DOM, which isolates styles from the rest of the page. Site classes won't penetrate the boundary — use component-specific CSS classes instead. CSS-in-JS libraries may need additional configuration for Shadow DOM compatibility.

See [Styling Components](styling-components.md) for details.

### How do I use site variables?

Reference site variables with CSS custom properties and always provide a fallback:

```css
.my-component {
  color: var(--background-primary, #000);
}
```

Get exact variable names from the Variables panel in the Webflow Designer (click "Copy CSS" in the three-dot menu next to any variable).

### Can I fetch data from external APIs?

Yes, but only client-side with public APIs. Never embed API keys or auth tokens in component code — all JavaScript is visible to users. APIs must support CORS.

```tsx
useEffect(() => {
  fetch("/api/public-data")
    .then((res) => res.json())
    .then(setData);
}, []);
```

See [Component Architecture](component-architecture.md) for data fetching patterns.

## Imports & Updates

### How do I update a component?

Edit the component locally, then run `npx webflow library share`. The entire library is deployed as one unit — you cannot update individual components separately.

### How do I test locally?

Bundle your library locally without uploading:

```bash
npx webflow library bundle --public-path http://localhost:4000/ --dev
```

### Is there versioning support?

No. Each import overwrites the previous library. Use Git to track changes to your component source code.

## Troubleshooting

### My component isn't rendering

Check for:

- Build or compilation errors
- Missing dependencies
- Bundle exceeding the 50MB limit
- Components must have one root element (fragments are not supported)

### Styles aren't applying

Shadow DOM isolation is the most common cause. To fix:

- Use component-specific classes instead of site classes
- Configure CSS-in-JS libraries for Shadow DOM compatibility
- Use `font-family: inherit` and other inherited properties for cross-boundary styling
- Enable `applyTagSelectors: true` in your component options for tag-level styles

### State isn't persisting between components

Each code component runs in its own React root. React Context and Redux won't share state across components. Use one of these alternatives:

- URL parameters (`URLSearchParams`)
- Browser storage (`localStorage` / `sessionStorage`)
- Nano Stores or other external state libraries
- Custom events (`window.dispatchEvent`)

See [Component Architecture](component-architecture.md) for cross-component communication patterns.

### Library import fails

Verify:

- Valid Workspace API token in `.env` (must be a Workspace token, not a Site token)
- Bundle is under 50MB
- No compilation errors
- Network connectivity to Webflow

Run with `--verbose` for additional debug output, or use `npx webflow library log` to retrieve logs from the most recent import.

## Performance

### How do I reduce bundle size?

The maximum bundle size is **50MB**. To optimize:

- Enable tree shaking to remove unused code
- Minimize third-party dependencies
- Remove unused imports and dead code
- Use `--debug-bundler` to inspect the final webpack configuration

### Do third-party libraries work?

Most React libraries work, but issues can arise with:

- Libraries that ship multiple entry points (ESM + CJS conflicts)
- CSS-in-JS libraries that inject styles outside Shadow DOM
- Libraries that directly modify `window` or `document`

## Advanced Topics

### How do I debug components?

1. Inspect the Shadow DOM via browser developer tools
2. Add `console.log` statements for runtime debugging
3. Use the `--dev` flag to disable minification for clearer error messages
4. Enable source maps in your webpack configuration

### Is TypeScript supported?

Yes. Use `.tsx` files for components and `.webflow.tsx` for definitions. Configure `tsconfig.json` as needed for your project.

### Do media queries work?

Yes. Standard CSS media queries work normally inside Shadow DOM for responsive design.

### Do CSS animations work?

Yes. CSS animations and `@keyframes` work normally within Shadow DOM boundaries.
