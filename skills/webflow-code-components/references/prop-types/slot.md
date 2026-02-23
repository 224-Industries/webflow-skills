---
name: "Slot Prop Type"
description: "Reference for the Slot prop type: content areas where designers can insert child components for flexible composition."
tags: [prop-types, slot, children, reactnode, composition, declare-component, props]
---

# Slot Prop Type

Add a Slot property to your component so designers can insert child components.

---

## Syntax

```tsx
// Prop definition
props.Slot({
  name: string,
  group?: string,
  tooltip?: string,
})

// Prop value
ReactNode
```

> `props.Children` is an alias for `props.Slot`.

## Definition Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | The name for the property |
| `group` | No | The group for this property |
| `tooltip` | No | Tooltip text shown for the property |

## Declaration Example

```tsx
// MyComponent.webflow.tsx
import { declareComponent } from '@webflow/react';
import { props } from '@webflow/data-types';
import { MyComponent } from "./MyComponent";

export default declareComponent(MyComponent, {
  name: "MyComponent",
  description: "A component with a Slot property",
  props: {
    children: props.Slot({
      name: "Content",
      group: "Content"
    })
  }
});
```

## Component Usage Example

```tsx
// MyComponent.tsx
import React from "react";

interface MyComponentProps {
  children?: React.ReactNode;
}

export const MyComponent = ({ children }: MyComponentProps) => {
  return (
    <div className="container">
      {children}
    </div>
  );
};
```

## When to Use

Use a Slot prop when designers need to:

- Insert child components
- Create flexible layout containers
- Build wrapper components

## Best Practices

- Handle missing children gracefully
- Consider layout and spacing for child content
- Test with various component types
