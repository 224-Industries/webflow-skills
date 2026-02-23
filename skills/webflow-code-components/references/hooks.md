---
name: "Hooks Reference"
description: "Reference for Webflow code component hooks: declareComponent function for defining components, and useWebflowContext hook for accessing rendering mode, interactivity, and locale."
tags: [hooks, utilities, declare-component, use-webflow-context, mode, interactive, locale, webflow-react]
---

# Hooks Reference

Webflow provides two key hooks from the `@webflow/react` package: `declareComponent` for defining code components, and `useWebflowContext` for accessing the current Webflow environment at runtime.

---

## `declareComponent`

Creates a code component declaration that tells Webflow how to use your React component on the canvas.

### Syntax

```typescript
import { declareComponent } from '@webflow/react';

declareComponent(Component, data): void;
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `Component` | `React.ComponentType` | The React component to declare |
| `data` | `object` | Component metadata, prop definitions, and optional configurations |

### Data Object Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | `string` | Yes | The component's display name in the panel |
| `description` | `string` | No | Context for the component's purpose |
| `group` | `string` | No | Group in the component panel |
| `props` | `object` | No | Prop definitions mapping React props to Webflow prop types |
| `decorators` | `array` | No | Higher-order components to wrap the component |
| `options` | `object` | No | Configuration for tag selectors and SSR |

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `applyTagSelectors` | `boolean` | `false` | Apply site tag selectors inside Shadow DOM |
| `ssr` | `boolean` | `true` | Enable/disable server-side rendering |

### Example

```tsx
// Button.webflow.tsx
import { declareComponent } from '@webflow/react';
import { props } from '@webflow/data-types';
import { Button } from './Button';

export default declareComponent(Button, {
  name: "Button",
  description: "A button component with a text and a style variant",
  group: "Interactive",
  props: {
    text: props.Text({
      name: "Button Text",
      defaultValue: "Click me"
    }),
    variant: props.Variant({
      name: "Style",
      options: ["primary", "secondary"],
      defaultValue: "primary"
    }),
  },
  options: {
    applyTagSelectors: true,
  },
});
```

---

## `useWebflowContext`

A React hook that retrieves information about the current Webflow environment. Use it to adapt component behavior based on rendering mode, interactivity state, and locale.

### Syntax

```typescript
import { useWebflowContext } from '@webflow/react';

const context = useWebflowContext();
```

### Return Value

Returns a `WebflowContext` object:

```typescript
type WebflowContext = {
  mode: WebflowMode;
  interactive: boolean;
  locale: string | null;
};
```

| Property | Type | Description |
|----------|------|-------------|
| `mode` | `WebflowMode` | The current Webflow rendering mode |
| `interactive` | `boolean` | Whether the component is in an interactive state |
| `locale` | `string \| null` | ISO string for the current locale, or `null` if unset |

### Supported Modes

| Mode | Description |
|------|-------------|
| `design` | Designer is working on visual layout |
| `build` | Page building mode |
| `edit` | Content editing |
| `preview` | Live preview |
| `component-preview` | Previewing an isolated component |
| `comment` | Comment/review mode |
| `analyze` | Analytics mode |
| `publish` | Published/production state |

### Example: Conditional Rendering Based on Interactive State

An accordion that expands by default in design mode so designers can view full content:

```tsx
// ExpandableSection.tsx
import { useWebflowContext } from '@webflow/react';

const ExpandableSection = ({ title, content }: { title: string; content: string }) => {
  const { interactive } = useWebflowContext();

  return (
    <details open={!interactive}>
      <summary>{title}</summary>
      <p>{content}</p>
    </details>
  );
};

export default ExpandableSection;
```

### Example: Locale-Aware Content

A component that switches content based on the active locale:

```tsx
// LocalizedComponent.tsx
import { useWebflowContext } from '@webflow/react';

const translations: Record<string, { title: string; cta: string }> = {
  es: { title: 'Bienvenido a nuestro sitio', cta: 'Comenzar ahora' },
  fr: { title: 'Bienvenue sur notre site', cta: 'Commencer maintenant' },
  en: { title: 'Welcome to our site', cta: 'Get started' },
};

const LocalizedComponent = () => {
  const { locale } = useWebflowContext();
  const content = translations[locale ?? 'en'] ?? translations.en;

  return (
    <div>
      <h2>{content.title}</h2>
      <button>{content.cta}</button>
    </div>
  );
};

export default LocalizedComponent;
```

### When to Use

- **Adapt component behavior** — provide placeholders or expanded states for designers in non-interactive modes
- **Control interactivity** — disable animations or event handlers when `interactive` is `false`
- **Handle localization** — deliver locale-specific content and formatting based on the active Webflow locale

## Best Practices

- Always export `declareComponent` as the default export from `.webflow.tsx` files
- Provide `name`, `description`, and `group` for discoverability in the component panel
- Set `ssr: false` for components that rely on browser APIs (`window`, `document`, `localStorage`)
- Use `useWebflowContext` to show expanded or placeholder content in design mode so designers can see the full component
- Always provide a fallback when reading `locale` since it can be `null`
