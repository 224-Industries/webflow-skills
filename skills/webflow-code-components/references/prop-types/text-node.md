---
name: "Text Node Prop Type"
description: "Reference for the Text Node prop type: on-canvas editable text with optional multiline support."
tags: [prop-types, text-node, reactnode, canvas-editing, multiline, declare-component, props]
---

# Text Node Prop Type

Add a Text Node property to enable designers to edit text content directly on the canvas or via the properties panel.

---

## Syntax

```tsx
// Prop definition
props.TextNode({
  name: string,
  group?: string,
  tooltip?: string,
  defaultValue?: string,
  multiline?: boolean,
})

// Prop value
ReactNode
```

## Definition Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | The name for the property |
| `multiline` | No | Whether the property allows multiple lines of text |
| `group` | No | The group for this property |
| `tooltip` | No | Tooltip text shown for the property |
| `defaultValue` | No | Default value for all component instances |

## Declaration Example

```tsx
// InfoSection.webflow.tsx
import { declareComponent } from "@webflow/react";
import { props } from "@webflow/data-types";
import { InfoSection } from "./InfoSection";

export default declareComponent(InfoSection, {
  name: "Info Section",
  description: "A component with a Text Node property",
  props: {
    title: props.TextNode({
      name: "Title",
      group: "Content",
      defaultValue: "Hello World",
    }),
    description: props.TextNode({
      name: "Description",
      multiline: true,
      group: "Content",
      defaultValue: "This is my first Webflow Code Component",
    }),
  },
});
```

## Component Usage Example

The prop delivers formatted HTML content to your React component as a `ReactNode`.

```tsx
// InfoSection.tsx
import React from "react";

interface InfoSectionProps {
  title: React.ReactNode;
  description: React.ReactNode;
}

export const InfoSection = ({ title, description }: InfoSectionProps) => {
  return (
    <>
      <h2>{title}</h2>
      <p>{description}</p>
    </>
  );
};
```

## When to Use

Use a Text Node prop when designers need to:

- Edit text content directly on the Webflow canvas
- Work with text content that may include HTML markup
- Add structured content like headings and lists

## Best Practices

- Provide meaningful default values so components render immediately on the canvas
- Handle missing content gracefully in your component logic
- Account for content styling and layout considerations
- Test with various HTML structures
