---
name: "Variant Prop Type"
description: "Reference for the Variant prop type: dropdown with predefined options for selecting visual styles, themes, or component variations."
tags: [prop-types, variant, options, dropdown, declare-component, props]
---

# Variant Prop Type

Add a Variant property to your component so designers can choose from a predefined list of options.

---

## Syntax

```tsx
// Prop definition
props.Variant({
  name: string,
  options: string[],
  group?: string,
  tooltip?: string,
  defaultValue?: string,
})

// Prop value
string
```

## Definition Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | The name for the property |
| `options` | Yes | Array of available variant options |
| `group` | No | The group for this property |
| `tooltip` | No | Tooltip text shown for the property |
| `defaultValue` | No | Default selected option (must match one of `options`) |

## Declaration Example

```tsx
// MyComponent.webflow.tsx
import { declareComponent } from '@webflow/react';
import { props } from '@webflow/data-types';
import { MyComponent } from "./MyComponent";

export default declareComponent(MyComponent, {
  name: "MyComponent",
  description: "A component with a Variant property",
  props: {
    style: props.Variant({
      name: "Button Style",
      group: "Style",
      options: ["Primary", "Secondary", "Tertiary"],
      defaultValue: "Primary"
    })
  }
});
```

## Component Usage Example

```tsx
// MyComponent.tsx
import React from "react";

interface MyComponentProps {
  style?: "Primary" | "Secondary" | "Tertiary";
}

export const MyComponent = ({ style }: MyComponentProps) => {
  return (
    <button className={`button button--${style?.toLowerCase()}`}>
      Click me
    </button>
  );
};
```

## When to Use

Use a Variant prop when designers need to:

- Choose from predefined visual styles
- Switch between component variations or themes
- Control component appearance

## Best Practices

- Use clear, descriptive option names
- Provide a sensible default value
- Keep the options list manageable
