---
name: "Quick Start Guide"
description: "Step-by-step quickstart for creating a React code component, declaring it for Webflow, sharing a library via DevLink CLI, and using it on the Webflow canvas."
tags: [quick-start, tutorial, setup, badge, declare-component, library-share, devlink-cli, workspace]
---

# Quick Start Guide

In this quickstart guide, we'll discuss how to import React components from an external codebase into Webflow using DevLink.

---

**What you'll accomplish:**

- Set up your development environment
- Declare a Webflow code component with props
- Import your component library to Webflow
- Use your component in a Webflow project

## Before You Start

Before running this quickstart, make sure you have:

- A Webflow account with either:
  - a Workspace on a Freelancer, Core, Growth, Agency, or Enterprise plan
  - a Webflow site with a CMS, Business, or Enterprise plan
- A Webflow site where you can test components
- Node.js 20+ and npm 10+ installed
- Basic familiarity with React components and TypeScript

## 1. Set Up Your Development Environment

Set up your local development environment to create and share React components. DevLink is compatible with a wide variety of React project setups.

### 1.1 Install the Webflow CLI and dependencies

Install the Webflow CLI globally and the necessary dependencies in your project:

```bash
# Install the Webflow CLI globally
npm install -g @webflow/webflow-cli

# Install dependencies in your project
npm i --save-dev @webflow/data-types @webflow/react
```

### 1.2 Create a Webflow configuration file

Create a `webflow.json` file in the root of your repository. This file will define the configuration for your code component library.

```json
{
  "library": {
    "name": "<Your Library Name>",
    "components": ["./src/**/*.webflow.@(js|jsx|mjs|ts|tsx)"]
  }
}
```

Give your library a name and specify the path to your code component files.

### 1.3 Add an example component to your library

In your editor, navigate to your `src` or components directory. Create a new file called `Badge.tsx`, and paste the following code. In the next step, you'll create a code component definition file to map this component to a Webflow component.

```tsx
// Badge.tsx
import * as React from "react";

interface BadgeProps {
  text: string;
  variant: 'Light' | 'Dark';
}

export const Badge = ({ text, variant }: BadgeProps) => (
  <span
    style={{
      backgroundColor: variant === 'Light' ? '#eee' : '#000',
      borderRadius: '1em',
      color: variant === 'Light' ? '#000' : '#fff',
      display: 'inline-block',
      fontSize: '14px',
      lineHeight: 2,
      padding: '0 1em',
    }}
  >
    {text}
  </span>
);
```

## 2. Define a Webflow Code Component

Create a code component definition file to map a React component to a Webflow component. In this step, you'll create a `Badge` component with two props mapping to an example `Badge.tsx` component.

### 2.1 Create a code component file

In your editor, navigate to your `src` or components directory where you added your Badge component. Create a new file called `Badge.webflow.tsx`. This file will define how your Badge component appears in Webflow.

### 2.2 Import the React component and Webflow functions

Import the necessary dependencies to create your code component: the React component, prop types and the `declareComponent` function.

```tsx
// Badge.webflow.tsx
import { Badge } from './Badge';
import { props } from '@webflow/data-types';
import { declareComponent } from '@webflow/react';
```

### 2.3 Declare the component

Declare the code component using the `declareComponent` function.

```tsx
// Badge.webflow.tsx
import { Badge } from './Badge';
import { props } from '@webflow/data-types';
import { declareComponent } from '@webflow/react';

export default declareComponent(Badge, {
  name: 'Badge',
  description: 'A badge with variants',
  group: 'Info',
});
```

The `declareComponent` function takes two parameters:

- Your React component (`Badge`)
- Configuration options:
  - `name`: The name of the component
  - `description?`: A description of the component (optional)
  - `group?`: The group the component belongs to (optional)
  - `props?`: The props of the component, **which we'll define in the next step.** (optional)
  - `options?`: The options of the component (optional)

For more information and detailed configuration options for code component imports, see [Define a Code Component](define-code-component.md).

### 2.4 Define the component props

Add configurable properties that users can edit in the Webflow designer.

Add a `props` object to the `declareComponent` function. This object defines which properties designers can configure in the Webflow editor, and maps them to appropriate Webflow prop types using the `props` constructor.

```tsx
// Badge.webflow.tsx
import { Badge } from './Badge';
import { props } from '@webflow/data-types';
import { declareComponent } from '@webflow/react';

export default declareComponent(Badge, {
  name: 'Badge',
  description: 'A badge with variants',
  group: 'Info',
  props: {
    text: props.Text({
      name: "Text",
      defaultValue: "Hello World",
    }),
    variant: props.Variant({
      name: "Variant",
      options: ["Light", "Dark"],
      defaultValue: "Light",
    }),
  },
});
```

This code component defines two props:

- `text`: A text field for the Badge content
- `variant`: A dropdown with predefined style options

## 3. Share Your Library to Webflow

In your terminal, run the following command to upload your library:

```bash
npx webflow library share
```

The Webflow CLI will:

- **Authorize your workspace:** The CLI will check for a Workspace authentication token in your `.env` file. If one is not found, the CLI will prompt you to authenticate by opening a browser window to the Workspace authorization page. **Authorize a workspace to continue.**
- **Bundle your library:** The CLI will bundle your library, and ask you to confirm the components you want to share.
- **Upload your library to your Workspace**

For more information and detailed configuration options for bundling and importing React components, see [Bundling and Import](bundling-and-import.md).

## 4. Use the Component on Your Webflow Site

Add your component to the canvas and update the props to customize the component.

### 4.1 Install the library on your Webflow site

Install the library on any site in your Workspace to start using your React components.

1. Open any Webflow site in your workspace.
2. Open the Libraries panel by pressing "L" or clicking the Resources icon in the left sidebar.
3. Find your library in the list of available libraries.
4. Install the library by clicking the **Install** icon next to your library.

### 4.2 Open the Components panel

Open the Components panel by pressing "Shift+C" or clicking the Components icon in the left sidebar.

Scroll to the section for the library you just installed. You should see your "Badge" component listed under the "Info" group.

### 4.3 Add the component to your page

Click and drag the Badge component from the components panel onto your page. The component will appear with its default text and styling.

### 4.4 Customize the component

Customize your component in the Properties panel on the right. You'll see two configurable properties:

- **Text**: Change the text content of the Badge
- **Variant**: Select from Light or Dark styling

Try changing the text to "Welcome!" and selecting a different variant to see your component update in real-time.

## Next Steps

Now that you've created your first code component, explore these resources to build more advanced components:

### Learn the fundamentals

- **[Define a Code Component](define-code-component.md)** — Learn how code components work and their architecture
- **[Prop Types Reference](prop-types.md)** — Explore all available prop types for creating configurable components

### Advanced configuration

- **[Installation & Configuration](installation.md)** — Learn how to configure your existing codebase for component import
- **[Bundling and Import](bundling-and-import.md)** — Explore advanced configuration options for bundling and importing React components
