---
name: "Code Components Introduction"
description: "Overview of Webflow code components (DevLink): importing React components into Webflow, key capabilities, and the end-to-end workflow from codebase to canvas."
tags: [introduction, overview, devlink, react, capabilities, workflow, libraries]
---

# Code Components Introduction

DevLink lets you import code components directly to Webflow, bridging the gap between code and visual development. Build advanced, interactive components in your codebase, and deploy them to Webflow. In Webflow, use code components directly on the canvas with props, slots, and variants for flexible composition.

---

## Get Started

- **[Quick Start](quick-start.md)** — Create a code component and share an example library to your workspace
- **[Installation & Configuration](installation.md)** — Update your existing library to work with DevLink and code components

---

## Key Capabilities

With code components, you get full control over your React development:

- **Develop in React** — Use hooks, state, effects, and context to build advanced components
- **Visual composition** — Expose props and slots for designers to design visually in Webflow
- **Shared library distribution** — Share, update, and install code components on any site in your Workspace with Libraries

See [Define a Code Component](define-code-component.md) for configuring your components for Webflow.

---

## How Code Components Work in Webflow

### 1. Build components in your codebase

Create React components with hooks, state management, and API integrations. Reference Webflow variables to allow components to adapt to an individual site's colors, typography, sizes, and spacing.

### 2. Declare a Webflow component in your codebase

Use `declareComponent` to wrap an existing React component, then define [prop types](prop-types.md) to make them available in the Webflow Designer.

### 3. Import components to Webflow

Use DevLink to bundle and publish your components as a shared library for users to install across a workspace.

### 4. Install components to a site

Install code components as a shared library on any Webflow site in your workspace.

### 5. Design visually

Drag and drop components onto the canvas, configure props and slots in the right panel, and customize styling through each site's variables to integrate with a specific design system.
