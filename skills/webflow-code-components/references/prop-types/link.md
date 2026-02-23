---
name: "Link Prop Type"
description: "Reference for the Link prop type: URL input with target behavior and preload settings, plus wrapper pattern for mapping to separate href/target props."
tags: [prop-types, link, href, target, preload, declare-component, props]
---

# Link Prop Type

Add a Link property to your component so designers can control URL, target behavior, and preload settings for clickable links.

---

## Syntax

```tsx
// Prop definition
props.Link({
  name: string,
  group?: string,
  tooltip?: string,
})

// Prop value
{
  href: string,
  target?: "_self" | "_blank" | string,
  preload?: "prerender" | "prefetch" | "none" | string,
}
```

## Definition Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | The name for the property |
| `group` | No | The group for this property |
| `tooltip` | No | Tooltip text shown for the property |

## Prop Value Properties

The Link prop returns an object to your React component:

- `href` — The URL destination
- `target` — How the link opens (optional)
- `preload` — Preload behavior (optional)

## Example: Direct Mapping

```tsx
// Button.webflow.tsx
import { declareComponent } from '@webflow/react';
import { props } from '@webflow/data-types';
import { Button } from "./Button";

export default declareComponent(Button, {
  name: "Button",
  description: "A Button component with a Link property",
  props: {
    link: props.Link({
      name: "Button Link",
      group: "Navigation"
    }),
    text: props.Text({
      name: "Button Text",
      group: "Navigation"
    })
  }
});
```

```tsx
// Button.tsx
import React from "react";

export interface ButtonProps {
  text?: string;
  link?: {
    href: string;
    target?: "_self" | "_blank" | string;
    preload?: "prerender" | "prefetch" | "none" | string;
  };
}

export const Button = ({ text, link }: ButtonProps) => {
  if (!link) return null;

  return (
    <a
      href={link.href}
      target={link.target}
      rel={link.target === "_blank" ? "noopener noreferrer" : undefined}
    >
      {text}
    </a>
  );
};
```

## Example: Prop Mapping (Wrapper Pattern)

When your React component expects separate `href` and `target` props rather than a link object, use a wrapper:

```tsx
// Button.webflow.tsx
import { props, PropType, PropValues } from "@webflow/data-types";
import { declareComponent } from "@webflow/react";
import React from "react";
import { Button, ButtonProps } from "./Button";

type WebflowButtonProps = {
  link: PropValues[PropType.Link];
} & Omit<ButtonProps, "href" | "target">;

const WebflowButton = ({
  link: { href, target },
  ...props
}: WebflowButtonProps) => {
  return <Button href={href} target={target} {...props} />;
};

export default declareComponent(WebflowButton, {
  name: "Button",
  props: {
    text: props.Text({
      name: "Text",
      defaultValue: "Lorem ipsum",
    }),
    link: props.Link({ name: "Link" }),
  },
});
```

```tsx
// Button.tsx
import React from "react";

export interface ButtonProps {
  text?: string;
  href?: string;
  target?: "_self" | "_blank" | string;
}

export const Button = ({ text, href, target }: ButtonProps) => {
  if (!href) return null;

  return (
    <a
      href={href}
      target={target}
      rel={target === "_blank" ? "noopener noreferrer" : undefined}
    >
      {text}
    </a>
  );
};
```

## When to Use

Use a Link prop when designers need to:

- Set URLs for buttons or text links
- Control link behavior (same tab vs. new tab)
- Build navigation components

## Best Practices

- Handle missing links gracefully
- Add proper `rel` attributes for security
- Consider accessibility for link text
