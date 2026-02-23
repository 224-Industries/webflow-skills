---
name: "Number Prop Type"
description: "Reference for the Number prop type: numeric input with min, max, and decimal precision controls."
tags: [prop-types, number, min, max, decimals, declare-component, props]
---

# Number Prop Type

Add a Number property to your component so designers can input numeric values with optional range and precision constraints.

---

## Syntax

```tsx
// Prop definition
props.Number({
  name: string,
  group?: string,
  tooltip?: string,
  defaultValue?: number,
  min?: number,
  max?: number,
  decimals?: number,
})

// Prop value
number
```

## Definition Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | The name for the property |
| `group` | No | The group for this property |
| `tooltip` | No | Tooltip text shown for the property |
| `defaultValue` | No | Default value for all component instances |
| `min` | No | Minimum value allowed |
| `max` | No | Maximum value allowed |
| `decimals` | No | Maximum number of decimal places |

## Declaration Example

```tsx
// MyComponent.webflow.tsx
import { declareComponent } from '@webflow/react';
import { props } from '@webflow/data-types';
import { MyComponent } from "./MyComponent";

export default declareComponent(MyComponent, {
  name: "MyComponent",
  description: "A component with a Number property",
  props: {
    count: props.Number({
      name: "Item Count",
      group: "Settings",
      defaultValue: 5,
      min: 1,
      max: 100,
      decimals: 0
    })
  }
});
```

## Component Usage Example

```tsx
// MyComponent.tsx
import React from "react";

interface MyComponentProps {
  count?: number;
}

export const MyComponent = ({ count }: MyComponentProps) => {
  return (
    <div className="counter">
      <span>Count: {count}</span>
    </div>
  );
};
```

## When to Use

Use a Number prop when designers need to:

- Set numeric values like counts, sizes, or durations
- Control values within specific ranges
- Limit decimal precision for cleaner data

## Best Practices

- Set appropriate `min`/`max` values for your use case
- Use `decimals: 0` for whole numbers, `1-2` for currency or percentages
- Provide meaningful default values
- Consider the full range designers will realistically need
