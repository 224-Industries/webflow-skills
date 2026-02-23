---
name: "Prop Types Reference"
description: "Reference for all available code component prop types: Text, Rich Text, Text Node, Link, Image, Number, Boolean, Variant, Visibility, Slot, and ID. Includes prop values, wrapper patterns, and best practices."
tags: [prop-types, props, text, rich-text, link, image, number, boolean, variant, visibility, slot, id, declare-component]
---

# Prop Types Reference

Prop types define the configurable properties that designers can edit in the Webflow designer. When you create a code component, you specify which React component properties to expose to designers, and how they should appear in Webflow.

---

## Defining Props in Your Code Component

In your `declareComponent` function, include a `props` property that maps your React component's properties to Webflow prop types. This tells Webflow:

- Which properties designers can configure
- How each property should appear in the designer
- Which values are valid for each property
- Default values for each property (for certain prop types)

## Basic Usage

```tsx
// Button.webflow.tsx
import { Button } from './Button';
import { props } from '@webflow/data-types';
import { declareComponent } from '@webflow/react';

export default declareComponent(Button, {
  name: 'Button',
  description: 'A button component',
  group: 'Interaction',
  props: {
    // Expose the 'text' prop as a text field
    text: props.Text({
      name: 'Button text',
      defaultValue: 'Hello World!',
    }),

    // Expose the 'variant' prop as a dropdown named 'Style'
    variant: props.Variant({
      name: 'Style',
      options: ['primary', 'secondary'],
    }),
  },
});
```

## Available Prop Types

Choose the appropriate prop type based on what you want designers to configure:

### Text and Content

- **[Text](prop-types/text.md)** — Single line text input
- **[Rich Text](prop-types/rich-text.md)** — Multi-line text with formatting
- **[Text Node](prop-types/text-node.md)** — Single and multi-line text that designers can edit on the canvas
- **[Link](prop-types/link.md)** — URL input with validation

### Assets and Data

- **[Image](prop-types/image.md)** — Image upload and selection
- **[Number](prop-types/number.md)** — Numeric input with validation
- **[Boolean](prop-types/boolean.md)** — True/false toggle

### Structure and Styles

- **[Variant](prop-types/variant.md)** — Dropdown with predefined options
- **[Visibility](prop-types/visibility.md)** — Show/hide controls
- **[Slot](prop-types/slot.md)** — Content areas for other components
- **[ID](prop-types/id.md)** — HTML Element ID

## Prop Values

Each prop type returns a value to your React component. For example, `props.Text` returns a string, while `props.Link()` returns an object with `href` and `target` properties.

Most times, you can map the prop values directly. For example, if your React component expects `text` as a string, you can map it to a `props.Text` prop.

However, if your React component expects specific properties from the returned object, you need to create a wrapper component that transforms the data. For example, the `props.Link()` prop type returns the following object:

```typescript
{
  href: string;
  target?: "_self" | "_blank" | string;
  preload?: "prerender" | "prefetch" | "none" | string;
}
```

If your React component expects `href` and `target` separately, you need to create a wrapper component that transforms the data:

### Wrapper definition file

```tsx
// Button.webflow.tsx
import { props, PropType, PropValues } from "@webflow/data-types";
import { declareComponent } from "@webflow/react";
import React from "react";
import Button, { ButtonProps } from "./Button";

// Remove href and target from the props to prevent conflicts
type WebflowButtonProps = {
  link: PropValues[PropType.Link];
} & Omit<ButtonProps, "href" | "target">;

// Wrapper that destructures the object returned from `props.Link`
// and passes the href and target to the button component as expected.
const WebflowButton = ({
  link: { href, target },
  ...props
}: WebflowButtonProps) => {
  return (
    <Button href={href} target={target} {...props} />
  );
};

export default declareComponent(WebflowButton, {
  name: "Button",
  props: {
    buttonText: props.Text({
      name: "Text",
      defaultValue: "Lorem ipsum"
    }),
    link: props.Link({ name: "Link" }),
  },
});
```

### Corresponding React component

```tsx
// Button.tsx
interface ButtonProps {
  buttonText: string;
  href: string;
  target: string;
}

export const Button = ({ buttonText, href, target }: ButtonProps) => {
  return <a href={href} target={target}>{buttonText}</a>;
};
```

This example definition file:

- Imports the `PropType` and `PropValues` types from the `@webflow/data-types` package
- Defines a link prop for the `Button` component. This will provide a link picker in Webflow and return the `href` and `target` values
- Adjusts the TypeScript types of the `Button` component to include the `link` object returned from the `props.Link` prop type
- Wraps the `Button` component in a new component that gets the `href` and `target` values from the `link` object and passes them to the `Button` component as expected

## Best Practices

### Provide Helpful Defaults

Always set meaningful default values so components work immediately when added to a page. Some prop types have default values built in, like `props.Text` which defaults to an empty string. However, you may want to set a default value in your React component as well.

```tsx
title: props.Text({
  name: 'Button Text',
  defaultValue: 'Click me', // Component works out of the box
}),
```

### Use Succinct Names

The `name` property appears in the Webflow designer — keep them short and title case. Use descriptions to provide more context.

### Group Related Props

Consider how props will appear together in the designer. Use the `group` property to group related props together.

```tsx
props: {
  heroTitle: props.Text({ name: 'Hero Title', group: 'Content' }),
  text: props.Text({ name: 'Text', group: 'Button' }),
  style: props.Variant({ name: 'Style', group: 'Button' }),
  size: props.Variant({ name: 'Size', group: 'Button' }),
}
```

## Example: Complete Component

Here's how you might define props for a card component:

```tsx
// Card.webflow.tsx
import { props } from '@webflow/data-types';
import { declareComponent } from '@webflow/react';
import Card from './Card';

export default declareComponent(Card, {
  name: 'Card',
  description: 'A card component',
  group: 'Content',
  props: {
    variant: props.Variant({
      name: 'Variant',
      options: ['Horizontal', 'Vertical'],
    }),
    title: props.Text({
      name: 'Title',
      defaultValue: 'Card title',
    }),
    text: props.Text({
      name: 'Text',
      defaultValue: 'Hello World!'
    }),
    buttonVisible: props.Visibility({
      group: 'Button',
      name: 'Visibility',
      defaultValue: true,
    }),
    buttonVariant: props.Variant({
      group: 'Button',
      name: 'Variant',
      options: ['Primary', 'Secondary', 'Outline'],
    }),
    buttonText: props.Text({
      group: 'Button',
      name: 'Text',
      defaultValue: 'Click me',
    }),
    buttonLink: props.Link({
      group: 'Button',
      name: 'Link',
    }),
  },
});
```
