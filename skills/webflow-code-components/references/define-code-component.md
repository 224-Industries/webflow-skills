---
name: "Define a Code Component"
description: "Complete reference for code component definition files (.webflow.tsx): declareComponent function, props, decorators, options (SSR, tag selectors), file naming, and best practices."
tags: [define, declare-component, webflow-tsx, props, decorators, options, ssr, tag-selectors, metadata, file-structure]
---

# Define a Code Component

A code component definition is a file that tells Webflow how to use your React component on the Webflow canvas. It defines which properties designers can configure and how they'll appear in the designer.

Every code component definition is a `.webflow.tsx` file that uses the `declareComponent` function to define the component.

---

### Example: Button definition file

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

### Example: Corresponding React component

```tsx
// Button.tsx
import React from 'react';
import styles from './Button.module.css';

interface ButtonProps {
  text: string;
  variant: 'primary' | 'secondary';
}

export const Button: React.FC<ButtonProps> = ({ text, variant }) => {
  return (
    <button
      className={`${styles.button} ${styles[variant]}`}
      type="button"
    >
      {text}
    </button>
  );
};
```

## File Structure and Naming

Code component definition files follow specific extension and naming patterns:

- **File extension**: `.webflow.tsx` or `.webflow.ts`
- **Naming pattern**: `ComponentName.webflow.tsx` (where `ComponentName` matches your React component)
- **Location**: Typically alongside your React component file

If you have specific naming needs, you can configure this pattern in `webflow.json`. It's recommended to create your code component file alongside your React component, adding `.webflow` to the name. For example, `Button.webflow.tsx` for `Button.tsx`.

> **Warning:** File names are the unique identifier of your code component. Renaming a definition file creates a new component and removes the old one from your library. If designers are already using the old component in their projects, those instances will break and need to be manually replaced.

## Imports

Every code component definition file needs to import your React component, Webflow functions, and any styles you want to apply to the component.

```tsx
// Button.webflow.tsx
import { declareComponent } from '@webflow/react';
import { props } from '@webflow/data-types';
import { Button } from './Button';
```

> **Note:** To apply global styles or integrate CSS-in-JS libraries, configure a global decorators file with [component decorators](#component-decorators).

## Declare Component

The `declareComponent` function creates a code component definition. It takes two arguments: the React component and a configuration object.

```tsx
// Button.webflow.tsx
import { declareComponent } from '@webflow/react';
import { Button } from './Button';
import { styledComponentsShadowDomDecorator } from "@webflow/styled-components-utils";
import { props } from '@webflow/data-types';

export default declareComponent(Button, {
  name: "Button",
  description: "A button component with a text and a style variant",
  group: "Interactive",
  decorators: [styledComponentsShadowDomDecorator],
  props: {
    text: props.Text({
      name: "Button Text",
      defaultValue: "Click me"
    }),
  },
});
```

- **`name`**: The name designers see in the component panel
- **`description?`**: Description to provide context for the component's purpose (optional)
- **`group?`**: Organize components into groups in the component panel (optional)
- **`props?`**: Object defining the props of the component (optional)
- **`decorators?`**: Array of decorators to apply to the component (optional)
- **`options?`**: Object defining the options of the component (optional)

## Prop Definitions

The `props` object defines which properties of your React component a designer can edit in Webflow. Declare a prop for each editable property in your React component and provide metadata that will appear in the designer. To see a list of all available prop types and their configuration options, see [Prop Types Reference](prop-types.md).

The below examples show a React component and its corresponding code component definition file.

### React component

This React component expects a `text` property, and a `variant` property.

```tsx
// Button.tsx
import React from 'react';
import styles from './Button.module.css';

interface ButtonProps {
  text: string;
  variant: 'primary' | 'secondary';
}

export const Button: React.FC<ButtonProps> = ({ text, variant }) => {
  return (
    <button
      className={`${styles.button} ${styles[variant]}`}
      type="button"
    >
      {text}
    </button>
  );
};
```

### Code component definition

This code component definition file declares a `text` and `variant` prop for the `Button` component.

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
});
```

Once shared with designers, the component will appear in the component panel and can be added to a page with editable props.

See more examples in [Prop Types Reference](prop-types.md).

## Component Decorators

Decorators are functions that wrap your React component with providers or other wrapper components. Use them to provide context like themes, internationalization, or feature flags, or to integrate CSS-in-JS libraries.

### Global Styles

To apply global styles across all components, import your CSS in a global decorators file and reference it in `webflow.json`:

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

```json
{
  "library": {
    "globals": "./src/globals.ts"
  }
}
```

### Custom Decorators

Create a custom decorator when you need to wrap components with additional behavior. A decorator is a higher-order component that takes a component and returns a wrapped version. This example wraps a data-fetching component with an error boundary to handle API failures gracefully:

```tsx
// ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("Component error:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong. Please refresh the page.</div>;
    }
    return this.props.children;
  }
}

export const errorBoundaryDecorator = <P extends object>(
  Component: React.ComponentType<P>
): React.ComponentType<P> => {
  return (props: P) => (
    <ErrorBoundary>
      <Component {...props} />
    </ErrorBoundary>
  );
};
```

```tsx
// UserCard.tsx
import React, { useEffect, useState } from "react";

interface User {
  name: string;
  email: string;
}

interface UserCardProps {
  userId: string;
}

export const UserCard: React.FC<UserCardProps> = ({ userId }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetch(`https://api.example.com/users/${userId}`)
      .then((res) => res.json() as Promise<User>)
      .then((data) => setUser(data));
  }, [userId]);

  if (!user) return <div>Loading...</div>;

  return (
    <div>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
};
```

```tsx
// UserCard.webflow.tsx
import { declareComponent } from "@webflow/react";
import { props } from "@webflow/data-types";
import { UserCard } from "./UserCard";
import { errorBoundaryDecorator } from "./ErrorBoundary";

export default declareComponent(UserCard, {
  name: "User Card",
  decorators: [errorBoundaryDecorator],
  props: {
    userId: props.Text({
      name: "User ID",
      defaultValue: "123",
    }),
  },
});
```

To apply decorators globally, export a `decorators` array from your decorators file:

```typescript
// src/globals.ts
import "./globals.css";
import { errorBoundaryDecorator } from "./ErrorBoundary";

export const decorators = [errorBoundaryDecorator];
```

> **Note:** Code components render in Shadow DOM, encapsulating them from the rest of the page, which impacts several CSS capabilities. See [Styling Components](styling-components.md) for more details.

## Options

The `options` object is used to configure the component for more advanced use cases.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `applyTagSelectors` | boolean | `false` | Whether to apply tag selectors to the component |
| `ssr` | boolean | `true` | Whether to enable server-side rendering |

### Tag Selectors

Styles targeting a tag selector (for example, `h1`, `p`, `button`) can be automatically provided to the Shadow DOM with the `applyTagSelectors` option. This is helpful for styling components with CSS selectors.

See [Styling Components](styling-components.md) for more details.

### Server-Side Rendering (SSR)

By default, Webflow will load your component on the server. This means that the component will be rendered on the server, but the DOM will be hydrated on the client-side. This is helpful for improving the performance of your component.

You can disable this behavior by setting `ssr` to `false`.

## Best Practices

- **Use consistent naming**: `ComponentName.webflow.tsx` for all code component definitions
- **Keep code component definitions close**: Place `.webflow.tsx` files next to their React components
- **Use clear names**: Make it obvious what the component does
- **Add descriptions**: Help designers understand the component's purpose
- **Group logically**: Use groups to organize components in the panel
- **Provide helpful defaults**: Make components work immediately when added
- **Use descriptive names**: The `name` property appears in the designer
- **Import CSS once**: Use a global decorators file rather than importing CSS in each component, then reference it in `webflow.json`

## Next Steps

- **[Styling Components](styling-components.md)** — Learn about how to style your components
- **[Prop Types Reference](prop-types.md)** — Learn about all available prop types
- **[Bundling and Import](bundling-and-import.md)** — Set up your build process and share your components
