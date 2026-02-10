---
name: "Designer APIs Reference"
description: "Quick reference table for all Webflow Designer API methods across elements, styles, components, pages, variables, assets, and utilities."
tags: [designer-api, quick-reference, getSelectedElement, getAllElements, setSelectedElement, getRootElement, createStyle, getStyleByName, getAllStyles, registerComponent, createInstance, enterComponent, exitComponent, createAsset, getAssetById, getAllAssets, createAssetFolder, getDefaultVariableCollection, getAllVariableCollections, createVariableCollection, getCurrentPage, getAllPages, createPage, getAllFolders, createFolder, notify, resizeExtension, elementBuilder, elementPresets, webflow-api, method-table]
---

# Designer APIs Reference

Quick reference for all Designer API methods. See linked files for detailed usage and examples.

## Table of Contents

- [Global Methods](#global-methods)
- [Elements API](#elements-api)
- [Styles API](#styles-api)
- [Components API](#components-api)
- [Pages API](#pages-api)
- [Variables API](#variables-api)
- [Assets API](#assets-api)
- [Utilities](#utilities)
- [Extension Utilities](#extension-utilities)

---

## Global Methods

Core `webflow.*` methods available globally.

| Method | Description |
|--------|-------------|
| `getSelectedElement()` | Get currently selected element |
| `setSelectedElement(el)` | Programmatically select an element |
| `getAllElements()` | Get all elements on current page |
| `getRootElement()` | Get root element (in component context) |
| `createStyle(name)` | Create a new style/class |
| `getStyleByName(name)` | Get style by name |
| `getAllStyles()` | Get all styles in project |
| `registerComponent(name, rootEl)` | Create component from element |
| `createInstance(component)` | Add component instance to page |
| `enterComponent(instance)` | Enter component editing context |
| `exitComponent()` | Exit component editing context |
| `createAsset(file)` | Upload asset from File object |
| `getAssetById(id)` | Get asset by ID |
| `getAllAssets()` | Get all assets |
| `createAssetFolder(name)` | Create asset folder |
| `getDefaultVariableCollection()` | Get default variable collection |
| `getAllVariableCollections()` | Get all variable collections |
| `createVariableCollection(name)` | Create new variable collection |
| `getCurrentPage()` | Get current page |
| `getAllPages()` | Get all pages |
| `createPage(options)` | Create new page |
| `getAllFolders()` | Get all page folders |
| `createFolder(name, parent?)` | Create page folder |
| `notify(options)` | Show notification to user |
| `resizeExtension(size)` | Resize extension panel |
| `elementBuilder(preset)` | Create element builder for bulk operations |
| `elementPresets.*` | Access element presets |

---

## Elements API

→ **[Detailed documentation](elements-api.md)**

### Element Selection & Retrieval

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.getSelectedElement()` | `Element \| null` | Get selected element |
| `webflow.setSelectedElement(el)` | `void` | Select an element |
| `webflow.getAllElements()` | `Element[]` | Get all page elements |

### Element Insertion

| Method | Returns | Description |
|--------|---------|-------------|
| `element.after(preset)` | `Element` | Insert sibling after |
| `element.before(preset)` | `Element` | Insert sibling before |
| `element.append(preset)` | `Element` | Insert as last child |
| `element.prepend(preset)` | `Element` | Insert as first child |
| `element.remove()` | `void` | Remove element |

### Element Properties

| Property/Method | Returns | Description |
|-----------------|---------|-------------|
| `element.id` | `{ element: string }` | Element identifier |
| `element.type` | `string` | Element type name |
| `element.children` | `Element[] \| undefined` | Child elements (if supported) |
| `element.textContent` | `string \| undefined` | Text content (if supported) |
| `element.setTextContent(text)` | `void` | Set text content |
| `element.getTextContent()` | `string` | Get text content |
| `element.setStyles(styles[])` | `void` | Apply styles |
| `element.getStyles()` | `Style[]` | Get applied styles |

### Element Presets

Access via `webflow.elementPresets.*`:

| Category | Presets |
|----------|---------|
| **Layout** | `DivBlock`, `Section`, `Container`, `Grid`, `VFlex`, `HFlex` |
| **Text** | `Paragraph`, `Heading`, `TextBlock`, `RichText`, `BlockQuote` |
| **Media** | `Image`, `Video`, `YouTube`, `Lottie` |
| **Forms** | `FormForm`, `FormInput`, `FormButton`, `FormTextarea`, `FormSelect` |
| **Navigation** | `Link`, `LinkBlock`, `NavBar`, `NavMenu` |
| **Custom** | `DOM` (custom HTML tags) |

### Element Builder (Bulk Operations)

| Method | Description |
|--------|-------------|
| `webflow.elementBuilder(preset)` | Create builder instance |
| `builder.setTag(tag)` | Set HTML tag (DOM elements) |
| `builder.setAttribute(name, value)` | Set attribute |
| `builder.append(preset)` | Append child to builder |

---

## Styles API

→ **[Detailed documentation](styles-api.md)**

### Style Management

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.createStyle(name)` | `Style` | Create new style |
| `webflow.getStyleByName(name)` | `Style \| null` | Get style by name |
| `webflow.getAllStyles()` | `Style[]` | Get all styles |

### Style Properties

| Method | Description |
|--------|-------------|
| `style.setProperty(prop, value, options?)` | Set single CSS property |
| `style.setProperties(propertyMap, options?)` | Set multiple CSS properties |
| `style.getProperty(prop, options?)` | Get property value |
| `style.getProperties(options?)` | Get all properties |

### Options Object

```typescript
{
  breakpoint?: "xxl" | "xl" | "large" | "main" | "medium" | "small" | "tiny",
  pseudo?: "hover" | "active" | "focus" | "visited" | "first-child" | ...
}
```

---

## Components API

→ **[Detailed documentation](components-api.md)**

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.registerComponent(name, rootEl)` | `Component` | Create component definition |
| `webflow.createInstance(component)` | `ComponentInstance` | Add instance to page |
| `webflow.enterComponent(instance)` | `void` | Enter component context |
| `webflow.exitComponent()` | `void` | Exit component context |
| `webflow.getRootElement()` | `Element` | Get root (in component context) |

---

## Pages API

→ **[Detailed documentation](pages-api.md)**

### Page Management

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.getCurrentPage()` | `Page` | Get current page |
| `webflow.getAllPages()` | `Page[]` | Get all pages |
| `webflow.createPage(options)` | `Page` | Create new page |

### Page Methods

| Method | Description |
|--------|-------------|
| `page.getName()` / `setName(name)` | Page name |
| `page.getSlug()` / `setSlug(slug)` | URL slug |
| `page.getTitle()` / `setTitle(title)` | Page title |
| `page.setMetaDescription(desc)` | SEO description |
| `page.setOgTitle(title)` | Open Graph title |
| `page.setOgDescription(desc)` | Open Graph description |
| `page.setOgImage(asset)` | Open Graph image |
| `page.setIndexable(bool)` | Allow search indexing |
| `page.setFolder(folder)` | Move to folder |
| `page.isDraft()` | Check if draft |
| `page.isPasswordProtected()` | Check if protected |

### Folder Management

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.getAllFolders()` | `Folder[]` | Get all folders |
| `webflow.createFolder(name, parent?)` | `Folder` | Create folder |

---

## Variables API

→ **[Detailed documentation](variables-api.md)**

### Collections

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.getDefaultVariableCollection()` | `Collection` | Get default collection |
| `webflow.getAllVariableCollections()` | `Collection[]` | Get all collections |
| `webflow.createVariableCollection(name)` | `Collection` | Create collection |

### Variable Creation (on Collection)

| Method | Returns | Description |
|--------|---------|-------------|
| `collection.createColorVariable(name, value)` | `ColorVariable` | Create color |
| `collection.createSizeVariable(name, value)` | `SizeVariable` | Create size |
| `collection.createFontFamilyVariable(name, value)` | `FontVariable` | Create font |
| `collection.createNumberVariable(name, value)` | `NumberVariable` | Create number |
| `collection.createPercentageVariable(name, value)` | `PercentageVariable` | Create percentage |

### Variable Retrieval

| Method | Returns | Description |
|--------|---------|-------------|
| `collection.getVariableByName(name)` | `Variable` | Get by name |
| `collection.getAllVariables()` | `Variable[]` | Get all |
| `collection.getColorVariables()` | `ColorVariable[]` | Get colors |
| `collection.getSizeVariables()` | `SizeVariable[]` | Get sizes |
| `collection.getFontFamilyVariables()` | `FontVariable[]` | Get fonts |

### Variable Methods

| Method | Description |
|--------|-------------|
| `variable.getValue()` | Get current value |
| `variable.setValue(value)` | Update value |

---

## Assets API

→ **[Detailed documentation](assets-api.md)**

### Asset Management

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.createAsset(file)` | `Asset` | Upload asset |
| `webflow.getAssetById(id)` | `Asset` | Get by ID |
| `webflow.getAllAssets()` | `Asset[]` | Get all assets |
| `webflow.createAssetFolder(name)` | `AssetFolder` | Create folder |

### Asset Methods

| Method | Description |
|--------|-------------|
| `asset.getUrl()` | Get hosted URL |
| `asset.getName()` | Get filename |
| `asset.getAltText()` / `setAltText(text)` | Alt text |
| `asset.getMimeType()` | Get MIME type |
| `asset.setFolder(folder)` | Move to folder |

### Image Element Methods

| Method | Description |
|--------|-------------|
| `imageElement.setAsset(asset)` | Set image asset |
| `imageElement.getAsset()` | Get current asset |

---

## Utilities

### Notifications

```typescript
await webflow.notify({
  type: 'Success' | 'Error' | 'Info' | 'Warning',
  message: 'Your message here'
});
```

### Extension Sizing

```typescript
await webflow.setExtensionSize({ width: 300, height: 400 });
```

### Error Handling

→ **[Detailed documentation](error-handling.md)**

| Error Tag | Description |
|-----------|-------------|
| `DuplicateValue` | Value must be unique |
| `Forbidden` | Permission denied |
| `InternalError` | System error |
| `InvalidElementPlacement` | Invalid element location |
| `InvalidRequest` | Invalid for current state |
| `InvalidStyle` | Style not recognized |
| `ResourceMissing` | Resource not found |
| `ResourceRemovalFailed` | Cannot remove (in use) |
| `VariableInvalid` | Invalid variable value |

---

## Extension Utilities

→ **[Detailed documentation](extension-utilities.md)**

### Site Information & Settings

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.getSiteInfo()` | `SiteInfo` | Get site metadata (ID, name, domains, workspace) |
| `webflow.setExtensionSize(size)` | `void` | Resize extension panel |
| `webflow.closeExtension()` | `void` | Close the extension |
| `webflow.getMediaQuery()` | `BreakpointId` | Get current breakpoint |

### User Events

| Method | Description |
|--------|-------------|
| `webflow.subscribe("selectedelement", cb)` | Listen for element selection changes |
| `webflow.subscribe("currentpage", cb)` | Listen for page changes |
| `webflow.subscribe("mediaquery", cb)` | Listen for breakpoint changes |
| `webflow.subscribe("mode", cb)` | Listen for Designer mode changes |

### Notifications

| Method | Description |
|--------|-------------|
| `webflow.notify({ type, message })` | Show notification (Success/Error/Info) |

### App Intents & Connections

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.getLaunchContext()` | `LaunchContext \| null` | Get how extension was launched |
| `element.setAppConnection(id)` | `void` | Create connection to element |
| `element.getAppConnections()` | `string[]` | Get element's connections |
| `element.removeAppConnection(id)` | `void` | Remove connection |

### User Authentication

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.getIdToken()` | `string` | Get JWT for user (valid 15 min) |

---

## Design Guidelines

→ **[Detailed documentation](design-guidelines.md)**

CSS variables for native Webflow look available in `assets/webflow-variables.css`.
