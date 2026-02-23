---
name: "Visibility Prop Type"
description: "Reference for the Visibility prop type: boolean toggle for showing or hiding elements conditionally."
tags: [prop-types, visibility, show-hide, conditional, declare-component, props]
---

# Visibility Prop Type

Add a Visibility property to your component so designers can show or hide elements.

---

## Syntax

```tsx
// Prop definition
props.Visibility({
  name: string,
  group?: string,
  tooltip?: string,
  defaultValue?: boolean,
})

// Prop value
boolean
```

## Definition Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | The name for the property |
| `group` | No | The group for this property |
| `tooltip` | No | Tooltip text shown for the property |
| `defaultValue` | No | Default visibility state |

## Declaration Example

```tsx
// MyComponent.webflow.tsx
import { declareComponent } from '@webflow/react';
import { props } from '@webflow/data-types';
import { MyComponent } from "./MyComponent";

export default declareComponent(MyComponent, {
  name: "MyComponent",
  description: "A component with a Visibility property",
  props: {
    isVisible: props.Visibility({
      name: "Show Element",
      group: "Display",
      defaultValue: true
    })
  }
});
```

## Component Usage Example

```tsx
// MyComponent.tsx
import React from "react";

interface MyComponentProps {
  isVisible?: boolean;
}

export const MyComponent = ({ isVisible }: MyComponentProps) => {
  if (!isVisible) return null;

  return (
    <div className="element">
      This element is visible
    </div>
  );
};
```

## When to Use

Use a Visibility prop when designers need to:

- Show or hide elements conditionally
- Control component display states
- Create toggled content
- Build conditional layouts

## Best Practices

- Provide sensible default values
- Handle hidden states gracefully
- Consider accessibility implications
