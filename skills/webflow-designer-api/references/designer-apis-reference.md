---
name: "Designer APIs Reference"
description: "Quick reference table for all Webflow Designer API methods across elements, styles, components, pages, variables, assets, and utilities."
tags: [designer-api, quick-reference, getSelectedElement, getAllElements, setSelectedElement, getRootElement, createStyle, getStyleByName, getAllStyles, removeStyle, registerComponent, getAllComponents, enterComponent, exitComponent, createAsset, getAssetById, getAllAssets, getAllAssetFolders, createAssetFolder, getDefaultVariableCollection, getAllVariableCollections, getVariableCollectionById, createVariableCollection, getCurrentPage, getAllPages, createPage, getAllFolders, createFolder, notify, setExtensionSize, elementBuilder, elementPresets, webflow-api, method-table]
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
| `createStyle(name, options?)` | Create a new style/class |
| `getStyleByName(name)` | Get style by name |
| `getAllStyles()` | Get all styles in project |
| `removeStyle(style)` | Remove a style |
| `getAllComponents()` | Get all registered components |
| `registerComponent(name, root)` | Create component from element |
| `enterComponent(instance)` | Enter component editing context |
| `exitComponent()` | Exit component editing context |
| `createAsset(file)` | Upload asset from File object |
| `getAssetById(id)` | Get asset by ID |
| `getAllAssets()` | Get all assets |
| `getAllAssetFolders()` | Get all asset folders |
| `createAssetFolder(name)` | Create asset folder |
| `getDefaultVariableCollection()` | Get default variable collection |
| `getAllVariableCollections()` | Get all variable collections |
| `getVariableCollectionById(id)` | Get variable collection by ID |
| `createVariableCollection(name)` | Create new variable collection |
| `getCurrentPage()` | Get current page |
| `getAllPages()` | Get all pages |
| `createPage(options)` | Create new page |
| `getAllFolders()` | Get all page folders |
| `createFolder(name, parent?)` | Create page folder |
| `notify(options)` | Show notification to user |
| `setExtensionSize(size)` | Resize extension panel |
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
| `webflow.createStyle(name, options?)` | `Style` | Create new style (pass `{ parent }` for combo class) |
| `webflow.getStyleByName(name)` | `Style \| null` | Get style by name |
| `webflow.getAllStyles()` | `Style[]` | Get all styles |
| `webflow.removeStyle(style)` | `void` | Remove a style |

### Style Properties

| Method | Description |
|--------|-------------|
| `style.setProperty(prop, value, options?)` | Set single CSS property |
| `style.setProperties(propertyMap, options?)` | Set multiple CSS properties |
| `style.getProperty(prop, options?)` | Get property value |
| `style.getProperties(options?)` | Get all properties |
| `style.removeProperty(prop)` | Remove single CSS property |
| `style.removeProperties({ properties })` | Remove multiple CSS properties |
| `style.removeAllProperties()` | Remove all CSS properties |
| `style.isComboClass()` | Check if style is a combo class |

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

### Component Management

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.getAllComponents()` | `Component[]` | Get all registered components |
| `webflow.registerComponent(name, root)` | `Component` | Create component definition |
| `webflow.enterComponent(instance)` | `null` | Enter component editing context |
| `webflow.exitComponent()` | `null` | Exit component context |
| `webflow.getRootElement()` | `Element \| null` | Get root element of current context |

### Component Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `component.getName()` | `string` | Get component name |
| `component.getRootElement()` | `Element` | Get component's root element |

### Creating Instances

Instances are created using element insertion methods with a `Component` object:

| Method | Description |
|--------|-------------|
| `element.before(component)` | Insert instance as sibling before |
| `element.after(component)` | Insert instance as sibling after |
| `element.append(component)` | Insert instance as last child |
| `element.prepend(component)` | Insert instance as first child |

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
| `webflow.getVariableCollectionById(id)` | `Collection` | Get collection by ID |
| `webflow.createVariableCollection(name)` | `Collection` | Create collection |

### Variable Creation (on Collection)

| Method | Returns | Description |
|--------|---------|-------------|
| `collection.createColorVariable(name, value, options?)` | `ColorVariable` | Create color |
| `collection.createSizeVariable(name, value, options?)` | `SizeVariable` | Create size |
| `collection.createFontFamilyVariable(name, value, options?)` | `FontFamilyVariable` | Create font |
| `collection.createNumberVariable(name, value, options?)` | `NumberVariable` | Create number |
| `collection.createPercentageVariable(name, value, options?)` | `PercentageVariable` | Create percentage |

### Variable Retrieval

| Method | Returns | Description |
|--------|---------|-------------|
| `collection.getVariableByName(name)` | `Variable` | Get by name |
| `collection.getVariable(id)` | `Variable` | Get by ID |
| `collection.getAllVariables()` | `Variable[]` | Get all |

### Variable Methods

| Method | Description |
|--------|-------------|
| `variable.set(value)` | Update value |
| `variable.setName(name)` | Rename variable |
| `variable.getBinding()` | Get CSS `var()` reference string |

---

## Assets API

→ **[Detailed documentation](assets-api.md)**

### Asset Management

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.createAsset(file)` | `Asset` | Upload asset |
| `webflow.getAssetById(id)` | `Asset` | Get by ID |
| `webflow.getAllAssets()` | `Asset[]` | Get all assets |
| `webflow.getAllAssetFolders()` | `AssetFolder[]` | Get all asset folders |
| `webflow.createAssetFolder(name)` | `AssetFolder` | Create folder |

### Asset Methods

| Method | Description |
|--------|-------------|
| `asset.getUrl()` | Get hosted URL |
| `asset.getName()` / `setName(name)` | Get or set filename |
| `asset.getAltText()` / `setAltText(text)` | Alt text |
| `asset.getMimeType()` | Get MIME type |
| `asset.setFile(file)` | Replace asset file |
| `asset.getParent()` | Get asset's folder |
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
  type: 'Success' | 'Error' | 'Info',
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

### Site Information & Extension

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.getSiteInfo()` | `SiteInfo` | Get site metadata (ID, name, domains, workspace) |
| `webflow.setExtensionSize(size)` | `null` | Resize extension panel |
| `webflow.closeExtension()` | `null` | Close the extension |
| `webflow.getMediaQuery()` | `BreakpointId` | Get current breakpoint |
| `webflow.getElementSnapshot(element)` | `string \| null` | Capture element as base64 PNG |

### User Events

| Method | Description |
|--------|-------------|
| `webflow.subscribe("selectedElement", cb)` | Listen for element selection changes |
| `webflow.subscribe("currentpage", cb)` | Listen for page changes |
| `webflow.subscribe("mediaquery", cb)` | Listen for breakpoint changes |
| `webflow.subscribe("currentcmsitem", cb)` | Listen for CMS item selection |
| `webflow.subscribe("currentappmode", cb)` | Listen for Designer mode changes |
| `webflow.subscribe("pseudomode", cb)` | Listen for pseudo-state changes |

### Notifications

| Method | Description |
|--------|-------------|
| `webflow.notify({ type, message })` | Show notification (Success/Error/Info) |

### App Intents & Connections

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.getLaunchContext()` | `LaunchContext \| null` | Get how extension was launched (AppIntent/AppConnection/AppsPanel) |
| `element.setAppConnection(id)` | `null` | Create connection to element |
| `element.getAppConnections()` | `string[]` | Get element's connections (own app only) |
| `element.removeAppConnection(id)` | `null` | Remove connection |

### User Authentication

| Method | Returns | Description |
|--------|---------|-------------|
| `webflow.getIdToken()` | `string` | Get JWT for user (valid 15 min) |

---

## Design Guidelines

→ **[Detailed documentation](design-guidelines.md)**

CSS variables for native Webflow look available in `assets/webflow-variables.css`.
