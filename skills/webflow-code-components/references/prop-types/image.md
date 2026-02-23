---
name: "Image Prop Type"
description: "Reference for the Image prop type: asset library image selection with src and alt text, plus wrapper pattern for mapping to separate props."
tags: [prop-types, image, src, alt, assets, declare-component, props]
---

# Image Prop Type

Add an Image property to your component so designers can select images from their Webflow asset library.

---

## Syntax

```tsx
// Prop definition
props.Image({
  name: string,
  group?: string,
  tooltip?: string,
})

// Prop value
{
  src: string,
  alt?: string,
}
```

## Definition Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | The name for the property |
| `group` | No | The group for this property |
| `tooltip` | No | Tooltip text shown for the property |

## Prop Value Properties

The Image prop returns an object to your React component:

- `src` — The source URL of the image
- `alt` — The alt text for the image (optional)

## Example: Direct Mapping

```tsx
// Hero.webflow.tsx
import { declareComponent } from '@webflow/react';
import { props } from '@webflow/data-types';
import { Hero } from "./Hero";

export default declareComponent(Hero, {
  name: "Hero",
  description: "A Hero component with an Image property",
  props: {
    image: props.Image({
      name: "Hero Image",
      group: "Content"
    })
  }
});
```

```tsx
// Hero.tsx
import React from "react";

interface HeroProps {
  image?: {
    src: string;
    alt?: string;
  };
}

export const Hero = ({ image }: HeroProps) => {
  if (!image) return null;

  return (
    <div className="image-container">
      <img
        src={image.src}
        alt={image.alt || ""}
        className="component-image"
      />
    </div>
  );
};
```

## Example: Prop Mapping (Wrapper Pattern)

When your React component expects separate `src` and `alt` props:

```tsx
// Hero.webflow.tsx
import { props, PropType, PropValues } from "@webflow/data-types";
import { declareComponent } from "@webflow/react";
import React from "react";
import { Hero, HeroProps } from "./Hero";

type HeroWebflowComponentProps = {
  image: PropValues[PropType.Image];
} & Omit<HeroProps, "src" | "alt">;

const HeroWebflowComponent = ({
  image: { src, alt },
  ...props
}: HeroWebflowComponentProps) => {
  return <Hero src={src} alt={alt} {...props} />;
};

export default declareComponent(HeroWebflowComponent, {
  name: "Hero",
  props: {
    image: props.Image({ name: "Image" }),
  },
});
```

```tsx
// Hero.tsx
import React from "react";

export interface HeroProps {
  src?: string;
  alt?: string;
}

export const Hero = ({ src, alt }: HeroProps) => {
  if (!src) return null;

  return (
    <div className="image-container">
      <img src={src} alt={alt || ""} className="component-image" />
    </div>
  );
};
```

## When to Use

Use an Image prop when designers need to:

- Select images from their asset library
- Swap images without modifying code
- Set alt text for accessibility

## Best Practices

- Handle cases where images are missing
- Always use alt text for accessibility
- Plan for responsive design requirements
