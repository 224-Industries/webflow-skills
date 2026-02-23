---
name: "Component Architecture"
description: "Runtime architecture of code components: Shadow DOM isolation, separate React roots, SSR and hydration, cross-component communication patterns (URL params, browser storage, Nano Stores, custom events), and data fetching."
tags: [architecture, shadow-dom, react-roots, ssr, hydration, state-management, custom-events, nano-stores, data-fetching, isolation]
---

# Component Architecture

**Code components run as isolated React applications.** Each one mounts in its own Shadow DOM container with a separate React root, creating a sandboxed environment that prevents conflicts with the main page or other components.

---

Because of this isolation, each imported React component manages its own dependencies, state, and context. When building, it's important to consider how your components handle state and communicate with each other.

### Key Concepts

- **Shadow DOM isolation** — Styles and DOM elements are contained
- **Separate React roots** — No shared state or context between components
- **Server-side rendering** — SSR provides initial HTML
- **Client-side execution** — All interactivity runs in the browser

This architecture affects how you handle state management, component communication, data fetching, and styling. Use the following patterns to manage these constraints when building your React components for import into Webflow.

## Shadow DOM and React Roots

Each code component runs in its own Shadow DOM container with a separate React root. This sandboxed environment prevents conflicts with the main page and other components:

- Your component's styles won't leak to the page
- Page styles won't override your component's styles
- You must explicitly import external styles (site variables, tag selectors, etc.)

**Composing components with slots**

When composing code components using slots, parent and child components may not share state through React context. Each child component renders in its own Shadow DOM container, which isolates component state sharing.

Shadow DOM impacts how you style components as well as your ability to use third-party libraries. See [Styling Components](styling-components.md) for more details.

## Server-Side Rendering (SSR)

Webflow supports server-side rendering (SSR) for code components. SSR generates initial HTML for the component on the server, which can improve perceived performance and SEO. After the page loads, Webflow automatically hydrates the component in the browser so that it becomes fully interactive.

Webflow enables SSR by default, but you can disable it by setting `ssr` to `false` in the component's definition file.

```typescript
// Chart.webflow.tsx
export default declareComponent(Component, {
  name: "Chart",
  description: "An interactive chart component",
  group: "Data Visualization",
  options: {
    ssr: false
  },
});
```

### When to Disable SSR

You'll want to turn off SSR for code components that rely on client-only behavior or that don't benefit from server-rendered HTML. Common cases include:

- **Browser APIs:** Components that use `window`, `document`, `localStorage`, or other APIs not available during SSR
- **Dynamic or personalized content:** User-specific dashboards, authenticated views, or components that need client data to render correctly
- **Heavy or interactive UI:** Charts, 3D scenes, maps, or animation-driven elements that would bloat the server-rendered HTML and be re-rendered anyway
- **Non-deterministic output:** Anything that renders differently on the server vs. client (for example, random numbers, time-based values)

> If the HTML output helps with SEO or improves the first paint, keep SSR on. If the component is purely interactive, client-specific, or browser-dependent, disable SSR.

> **Warning:** React Server Components are not supported in code components. All code components must use standard React components.

## Communicating Between Components

Because each code component runs in its own React root, they can't share React Context or state directly. Instead, use one of the following patterns to manage state across multiple components.

### URL Parameters

Store state in the URL using `URLSearchParams` for shareable, bookmarkable state. This is useful for search queries, filters, navigation state, or pagination.

```tsx
// Filter.tsx
// Set state
const url = new URL(window.location.href);
url.searchParams.set('filter', 'active');
window.history.pushState({}, '', url);

// Read state
const params = new URLSearchParams(window.location.search);
const filter = params.get('filter'); // 'active'
```

### Browser Storage

Use `localStorage` for persistent data or `sessionStorage` for session-only data. Only store non-sensitive information since this data is visible to users.

```tsx
// ThemePreference.tsx
// localStorage - persists across browser sessions
window.localStorage.setItem('userPreferences', JSON.stringify({ theme: 'dark' }));
const prefs = JSON.parse(localStorage.getItem('userPreferences'));

// sessionStorage - cleared when tab closes
window.sessionStorage.setItem('tempData', 'value');
```

Best for: user preferences, form data, temporary state.

### Nano Stores

Nano Stores is a lightweight state management library for cross-component communication, and is a useful alternative to React Context for sharing state between components.

#### 1. Install Nano Stores

In your React project, install Nano Stores by running the following command in your terminal:

```bash
npm install nanostores @nanostores/react
```

#### 2. Create a store

A store represents external shared state: any component can access, modify, or subscribe to it. Use Nano Stores' `atom()` to make a shared, reactive variable.

```tsx
// Store.tsx
import { atom } from 'nanostores';

// Shared state store - any component can read/write to this
export const $counter = atom(0);
```

> This example uses an atomic store with a single value. See the [Nano Stores documentation](https://github.com/nanostores/nanostores) for more information on the different types of stores.

#### 3. Read a store in a component

In your component, subscribe to the store using the `useStore()` hook to automatically update when the value changes:

```tsx
// Counter.tsx
import React from 'react';
import { useStore } from '@nanostores/react';
import { $counter } from './store';

// Displays the current count - automatically updates when store changes
export const Counter = () => {
  const count = useStore($counter);

  return (
    <div style={{ backgroundColor: 'lightblue', padding: '10px', borderRadius: '5px' }}>
      <p>Count: {count}</p>
    </div>
  );
};
```

#### 4. Update the store from a separate component

In the `Clicker` component, update the store using `set()` to change the value:

```tsx
// Clicker.tsx
import React from 'react';
import { Button } from './Button';
import { $counter } from './Store';

interface ClickerProps {
  text: string;
  variant: 'primary' | 'secondary';
}

// Button that increments the shared counter when clicked
export const Clicker = ({ text, variant }: ClickerProps) => {
  const clicked = React.useCallback(() => $counter.set($counter.get() + 1), []);
  return <Button
    text={text}
    variant={variant}
    onClick={clicked} />;
};
```

> This example uses the `useCallback` hook to update the store when the button is clicked.

### Custom Events

To notify a component of an event or update another component, use custom events to communicate across React components in Webflow:

```tsx
// ThemeToggle.tsx
import React from 'react';

export const ThemeToggle = () => {
  const handleClick = () => {
    // Dispatch custom event that other components can listen to
    window.dispatchEvent(new CustomEvent('theme-changed', {
      detail: { theme: 'dark' },
    }));
  };

  return <button onClick={handleClick}>Switch to Dark Mode</button>;
};
```

```tsx
// ThemeDisplay.tsx
import { useState, useEffect } from 'react';

export const ThemeDisplay = () => {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    const handleThemeChange = (event: Event) => {
      const customEvent = event as CustomEvent<{ theme: string }>;
      setTheme(customEvent.detail.theme);
    };

    window.addEventListener('theme-changed', handleThemeChange);
    return () => window.removeEventListener('theme-changed', handleThemeChange);
  }, []);

  return <div>Current theme: {theme}</div>;
};
```

## Data Fetching

Code components support client-side data fetching. This means your React component can request live or real-time data from a public API after it renders in the browser.

To fetch data, use React's `useEffect` hook when the component mounts:

```tsx
// MyComponent.tsx
import React, { useEffect, useState } from "react";

interface ApiResponse {
  message: string;
}

export const MyComponent = () => {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/public-data")
      .then((res) => res.json())
      .then((json: ApiResponse) => setData(json))
      .catch((err) => console.error("Fetch failed:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  if (!data) return <div>No data available</div>;

  return <div>{data.message}</div>;
};
```

### Key Considerations

- **Public APIs only:** Never include secrets or sensitive API keys in your component code. All JavaScript runs in the browser and is visible to users.
- **CORS support required:** The API must accept cross-origin requests from your Webflow-hosted site.
- **No environment variables:** `.env` files aren't supported. If you need to pass configuration values (like endpoint URLs, IDs, or feature flags), provide them as props instead of embedding them directly.

## Best Practices

- Use Nano Stores or custom events for cross-component communication instead of trying to share React Context
- Disable SSR for components that rely on browser-only APIs or personalized content
- Always handle loading and error states in data-fetching components
- Never embed API keys or secrets in component code — all client-side JavaScript is visible to users
- Use URL parameters for state that should be shareable or bookmarkable
