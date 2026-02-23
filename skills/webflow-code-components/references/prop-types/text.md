---
name: "Text Prop Type"
description: "Reference for the Text prop type: single-line text input for designers to set titles, labels, or descriptions."
tags: [prop-types, text, string, declare-component, props]
---

# Text Prop Type

Add a Text property to your component for designers to input plain text content.

---

## Syntax

```tsx
// Prop definition
props.Text({
  name: string,
  group?: string,
  tooltip?: string,
  defaultValue?: string,
})

// Prop value
string
```

> `props.String` is an alias for `props.Text`.

## Definition Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | The name for the property |
| `group` | No | The group for this property |
| `tooltip` | No | Tooltip text shown for the property |
| `defaultValue` | No | Default value for all component instances |

## Declaration Example

```tsx
// MyComponent.webflow.tsx
import { declareComponent } from '@webflow/react';
import { props } from '@webflow/data-types';
import { MyComponent } from "./MyComponent";

export default declareComponent(MyComponent, {
  name: "MyComponent",
  description: "A component with a Text property",
  props: {
    title: props.Text({
      name: "Title",
      group: "Content",
      defaultValue: "Hello World!"
    })
  }
});
```

## Component Usage Example

```tsx
// MyComponent.tsx
import React from "react";

interface MyComponentProps {
  title?: string;
}

export const MyComponent = ({ title }: MyComponentProps) => {
  return (
    <h1 className="title">
      {title}
    </h1>
  );
};
```

## When to Use

Use a Text prop when designers need to:

- Input simple text content
- Set titles, labels, or descriptions

## Best Practices

- Provide meaningful default values so the component renders when added to the canvas
- Use descriptive prop names
