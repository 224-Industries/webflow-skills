---
name: playground-workflow
description: How to use the Webflow Designer API Playground to write and run standalone code snippets directly inside the Designer. Great for prototyping, testing API methods, and one-off automations.
tags: [playground, snippets, prototyping, testing, quick-start]
---

# Designer API Playground Workflow

The **Designer API Playground** is an official Webflow app built and maintained by the Webflow team. It provides a mini code editor inside the Designer where you can write and execute Designer API code on the spot — no project setup, no bundling, no deployment.

Ideal for quick prototyping, learning the API, testing individual methods, and running one-off automations.

## Getting Started

> The setup steps below happen in the user's browser and Webflow account. Walk the user through each step, don't attempt to perform them yourself. If the user has the Claude Chrome Extension or uses Claude Cowork, offer to provide a ready-made prompt that automates the install flow. The prompt is in [assets/install-playground-prompt.md](../assets/install-playground-prompt.md), fill in the `{site_name}` placeholder with the user's site name before sharing.

1. Visit the install link: [Install Designer API Playground](https://webflow.com/oauth/authorize?response_type=code&client_id=19511de1ec410f9228d8dcbc9420e67916dea80d86d18f0c9a533eb475ea0f62)
2. Select the individual Webflow site you want to use, then click **"Authorize App"** in the bottom right
3. You'll be redirected straight into the Designer for that site with the Playground app open and ready to use
4. Write your snippet in the editor and run it
5. Click the 'Code Playground' tab inside the app, where you can add and run snippets

## Writing Snippets

Snippets are standalone async JavaScript. The `webflow` global is already available — no imports needed.

### Basic Example

```js
// Get the currently selected element and log its type
const el = await webflow.getSelectedElement();

if (el) {
  await webflow.notify({ type: "Success", message: `Selected: ${el.type}` });
} else {
  await webflow.notify({ type: "Error", message: "No element selected" });
}
```

### Creating Elements

```js
// Insert a heading and paragraph into the selected element
const selected = await webflow.getSelectedElement();
if (!selected?.children) {
  await webflow.notify({ type: "Error", message: "Select a container element" });
  return;
}

const heading = await selected.append(webflow.elementPresets.Heading);
await heading.setTextContent("Hello from the Playground!");

const paragraph = await selected.append(webflow.elementPresets.Paragraph);
await paragraph.setTextContent("This was added via the Designer API.");

await webflow.notify({ type: "Success", message: "Elements added!" });
```
See [Elements API Reference](elements-api.md) for more on creating and managing elements.

### Working with Styles

```js
// Create a style and apply it to the selected element
const selected = await webflow.getSelectedElement();
if (!selected) {
  await webflow.notify({ type: "Error", message: "Select an element first" });
  return;
}

// Webflow requires the full name for CSS properties in the API
const style = await webflow.createStyle("playground-card-style");
await style.setProperties({
  "background-color": "#f0f0f0",
  "padding-top": "20px",
  "padding-bottom": "20px",
  "padding-left": "20px",
  "padding-right": "20px",
  "border-radius": "8px",
});

await selected.setStyles([style]);
await webflow.notify({ type: "Success", message: "Style applied!" });
```

See [Styles API Reference](styles-api.md) for more on creating and managing styles.

## Snippet Guidelines

- **Top-level `await`** — Snippets run as async code, so you can `await` at the top level
- **No imports** — The `webflow` global is pre-injected; you don't need to import anything
- **Use `webflow.notify()`** — Always surface feedback since there's no custom UI
- **Keep it focused** — Each snippet should do one thing well; chain operations in sequence
- **Error handling** — Wrap operations in try/catch for reliability:

```js
try {
  const el = await webflow.getSelectedElement();
  if (!el) throw new Error("Select an element first");

  // ... your operations
  await webflow.notify({ type: "Success", message: "Done!" });
} catch (err) {
  await webflow.notify({ type: "Error", message: err.message });
}
```

## When to Use the Playground vs. an Extension

| Playground | Extension |
|---|---|
| Testing a single API method | Building a multi-feature tool |
| Quick one-off automation | Reusable app with UI controls |
| Learning how the API works | Distributing via Marketplace |
| No setup required | Needs scaffolding and bundling |

If you find yourself building something complex in the Playground, it might be time to scaffold a full extension — see [Designer Extension Workflow](designer-extension-workflow.md).

## Related References

- [Designer APIs Reference](designer-apis-reference.md): All Webflow Designer API methods
- [Error Handling](error-handling.md): Error structure and best practices for handling API errors
- [Code Examples](code-examples.md): Cross-API examples that can be used in both the Playground and Extensions