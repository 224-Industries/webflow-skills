---
name: "Rich Text Prop Type"
description: "Reference for the Rich Text prop type: formatted HTML content input for headings, lists, bold, italic, and links."
tags: [prop-types, rich-text, reactnode, html, declare-component, props]
---

# Rich Text Prop Type

Add a Rich Text property to your component so designers can create formatted content with HTML markup.

---

## Syntax

```tsx
// Prop definition
props.RichText({
  name: string,
  group?: string,
  tooltip?: string,
  defaultValue?: string,
})

// Prop value
ReactNode
```

## Definition Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | The name for the property |
| `group` | No | The group for this property |
| `tooltip` | No | Tooltip text shown for the property |
| `defaultValue` | No | Default content for all component instances |

## Declaration Example

```tsx
// MyComponent.webflow.tsx
import { declareComponent } from '@webflow/react';
import { props } from '@webflow/data-types';
import { MyComponent } from "./MyComponent";

export default declareComponent(MyComponent, {
  name: "MyComponent",
  description: "A component with a Rich Text property",
  props: {
    content: props.RichText({
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
  content?: React.ReactNode;
}

export const MyComponent = ({ content }: MyComponentProps) => {
  return (
    <div className="content-wrapper">
      {content}
    </div>
  );
};
```

## When to Use

Use a Rich Text prop when designers need to:

- Create formatted content with bold, italic, and links
- Add structured content like headings and lists
- Include HTML markup in their content

## Best Practices

- Provide meaningful default values so the component renders when added to the canvas
- Handle missing content gracefully
- Consider content styling and layout implications
- Test with various HTML structures
