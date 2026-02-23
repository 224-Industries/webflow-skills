---
name: "ID Prop Type"
description: "Reference for the ID prop type: text input for setting unique HTML element identifiers for CSS or JavaScript targeting."
tags: [prop-types, id, element-id, css-targeting, declare-component, props]
---

# ID Prop Type

Add an ID property to your component so designers can set unique identifiers on HTML elements for CSS or JavaScript targeting.

---

## Syntax

```tsx
// Prop definition
props.Id({
  name: string,
  group?: string,
  tooltip?: string,
})

// Prop value
string
```

## Definition Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | The label shown for the property |
| `group` | No | Groups the property within a panel section |
| `tooltip` | No | Tooltip text displayed to designers |

## Declaration Example

```tsx
// MyComponent.webflow.tsx
import { declareComponent } from '@webflow/react';
import { props } from '@webflow/data-types';
import { MyComponent } from "./MyComponent";

export default declareComponent(MyComponent, {
  name: "MyComponent",
  description: "A component with an ID property",
  props: {
    id: props.Id({
      name: "Element ID",
      group: "Info"
    })
  }
});
```

## Component Usage Example

```tsx
// MyComponent.tsx
import React from "react";

interface MyComponentProps {
  id?: string;
}

export const MyComponent = ({ id }: MyComponentProps) => {
  return (
    <div id={id}>
      {/* Component content */}
    </div>
  );
};
```

## When to Use

Use an ID prop when designers need to:

- Assign unique identifiers for CSS targeting
- Link form labels to their corresponding inputs
- Enable JavaScript-driven interactions

## Best Practices

- Use descriptive ID naming conventions
- Avoid duplicate IDs across a page
- Consider accessibility when using IDs for form associations
