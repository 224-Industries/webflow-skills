---
name: "Boolean Prop Type"
description: "Reference for the Boolean prop type: true/false toggle with custom panel labels for each state."
tags: [prop-types, boolean, toggle, true-label, false-label, declare-component, props]
---

# Boolean Prop Type

Add a Boolean property to your component so designers can toggle features, styling, or behavior on and off.

---

## Syntax

```tsx
// Prop definition
props.Boolean({
  name: string,
  group?: string,
  tooltip?: string,
  defaultValue?: boolean,
  trueLabel?: string,
  falseLabel?: string,
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
| `defaultValue` | No | Default boolean for all component instances |
| `trueLabel` | No | Panel label for the `true` state |
| `falseLabel` | No | Panel label for the `false` state |

> `trueLabel` and `falseLabel` only affect how options appear in Webflow's props panel — they do not alter the underlying `true`/`false` values passed to the component.

## Declaration Example

```tsx
// MyComponent.webflow.tsx
import { declareComponent } from '@webflow/react';
import { props } from '@webflow/data-types';
import { MyComponent } from "./MyComponent";

export default declareComponent(MyComponent, {
  name: "MyComponent",
  description: "A component with boolean and text properties",
  props: {
    showDetails: props.Boolean({
      name: "Show Details",
      group: "Content",
      defaultValue: false,
      trueLabel: "Show Details",
      falseLabel: "Hide Details"
    })
  }
});
```

## Component Usage Example

```tsx
// MyComponent.tsx
import React from "react";

interface MyComponentProps {
  showDetails?: boolean;
}

export const MyComponent = ({ showDetails }: MyComponentProps) => {
  return (
    <div>
      <h3>Welcome</h3>
      <p>Unlock your potential with our amazing features.</p>

      {showDetails && (
        <div style={{ marginTop: '12px', padding: '12px', backgroundColor: '#f0f8ff', borderRadius: '4px' }}>
          <p><strong>Additional details here</strong></p>
          <ul>
            <li>Feature one</li>
            <li>Feature two</li>
            <li>Feature three</li>
          </ul>
        </div>
      )}
    </div>
  );
};
```

## When to Use

Use a Boolean prop when designers need to:

- Enable or disable a feature
- Toggle styling variations
- Show or hide content sections
- Create behavior variations

## Best Practices

- Provide a sensible default value
- Use `trueLabel`/`falseLabel` for clarity in the designer panel
- Handle both states gracefully in your component
