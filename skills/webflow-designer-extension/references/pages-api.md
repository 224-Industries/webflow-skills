---
name: "Pages API"
description: "Reference for page and folder management including creation, page metadata (title/meta description), Open Graph settings, internal site search metadata, and URL structure."
tags: [pages, folders, getCurrentPage, getAllPagesAndFolders, createPage, createPageFolder, switchPage, getName, setName, getSlug, setSlug, getTitle, setTitle, getDescription, setDescription, setMetadata, getPublishPath, getKind, getCollectionID, getCollectionName, getUtilityPageKey, getSearchTitle, setSearchTitle, getSearchDescription, setSearchDescription, usesTitleAsSearchTitle, useTitleAsSearchTitle, usesDescriptionAsSearchDescription, useDescriptionAsSearchDescription, isExcludedFromSearch, excludeFromSearch, getSearchImage, setSearchImage, useOpenGraphImageAsSearchImage, getOpenGraphTitle, setOpenGraphTitle, getOpenGraphDescription, setOpenGraphDescription, getOpenGraphImage, setOpenGraphImage, usesTitleAsOpenGraphTitle, useTitleAsOpenGraphTitle, usesDescriptionAsOpenGraphDescription, useDescriptionAsOpenGraphDescription, isDraft, setDraft, isHomepage, isPasswordProtected, page-meta-description, open-graph, search-metadata, site-search, url-structure, page-settings, page-metadata]
---

# Pages API Reference

Manage site organizational structure, page settings, and metadata.

## Table of Contents

- [Glossary](#glossary)
- [Pages](#pages)
- [Folders](#folders)
- [Workflow Examples](#workflow-examples)
- [Best Practices](#best-practices)

---

## Glossary

Commonly-confused page fields (what they mean, where they show up, and which API methods control them):

| Concept | What it is | Where it shows up | Primary methods |
|---|---|---|---|
| **Page Name** | Internal label for organizing pages in the Designer | Designer page list (not used for HTML `<title>` or SEO) | `getName()` / `setName()` / `setMetadata({ name })` |
| **Slug** | URL path segment for the page | Page URL (e.g. `/about`) | `getSlug()` / `setSlug()` / `setMetadata({ slug })` |
| **Page Title** | The page’s title field used for browser/SEO by default | Typically maps to HTML `<title>`; may be reused for SEO/OG depending on “use title as …” toggles | `getTitle()` / `setTitle()` / `setMetadata({ title })` |
| **Page Description** | The page meta description field | Search engine result snippets and other metadata consumers | `getDescription()` / `setDescription()` / `setMetadata({ description })` |
| **Search Title** | Custom title used for internal site search results | Internal site search result title | `getSearchTitle()` / `setSearchTitle()` / `useTitleAsSearchTitle(true/false)` |
| **Search Description** | Custom description used for internal site search results | Internal site search result description | `getSearchDescription()` / `setSearchDescription()` / `useDescriptionAsSearchDescription(true/false)` |
| **Open Graph Title** | Social sharing title when customized | Social link previews (Open Graph) | `getOpenGraphTitle()` / `setOpenGraphTitle()` / `useTitleAsOpenGraphTitle(true/false)` |
| **Open Graph Description** | Social sharing description when customized | Social link previews (Open Graph) | `getOpenGraphDescription()` / `setOpenGraphDescription()` / `useDescriptionAsOpenGraphDescription(true/false)` |
| **Open Graph Image** | Social sharing image | Social link previews (Open Graph) | `getOpenGraphImage()` / `setOpenGraphImage()` |

> **Tip**: If you want internal site search fields to follow the page title and meta description, call `useTitleAsSearchTitle(true)` and `useDescriptionAsSearchDescription(true)`.

## Pages

### Get Current Page
```typescript
const page = await webflow.getCurrentPage();
```

### Get All Pages and Folders
```typescript
const pagesAndFolders = await webflow.getAllPagesAndFolders();

// Filter pages
const pages = pagesAndFolders?.filter((i): i is Page => i.type === "Page");

// Filter folders
const folders = pagesAndFolders?.filter((i): i is Folder => i.type === "PageFolder");
```

### Switch to a Page
```typescript
await webflow.switchPage(page);
```

### Page Properties

```typescript
// Get Page Info
const name = await page.getName();
const slug = await page.getSlug();
const title = await page.getTitle();
const description = await page.getDescription();
const publishPath = await page.getPublishPath();

// Page Category
const category = await page.getKind();
// Available Categories: 'static', 'ecommerce', 'cms', 'utility', 'staticTemplate'

// Collection (cms) pages:
const collectionId = await page.getCollectionID();
const collectionName = await page.getCollectionName();

// Utility (utility) pages:
const utilityType = await page.getUtilityPageKey();
// Available Types: '401', '404', 'search', 'ecommerce-checkout', 'ecommerce-paypal-checkout', 'ecommerce-confirmation'
```

> **Note**: The page `name` is an internal Designer label. The page `description` is the page meta description. The `slug` is used in the page URL and should be unique within the site.

```typescript
// Update Page Info
await page.setName("New Page Name");
await page.setSlug("new-page-slug");
await page.setTitle("New Page Title | Site Name");
await page.setDescription("Page description text");

// Page Category cannot be changed as it is determined by the page template and functionality.
```

### Set Page Metadata (Bulk)

Update multiple page properties at once:

```typescript
page.setMetadata({
  name: "Product Features",
  slug: "product-features",
  title: "Awesome Product Features",
  description: "Discover our product's amazing features",
  isDraft: false,
  usesTitleAsOpenGraphTitle: true,
  openGraphTitle: "",
  usesDescriptionAsOpenGraphDescription: true,
  openGraphDescription: "",
  openGraphImage: "https://example.com/og-image.jpg",
  isExcludedFromSearch: false,
  usesTitleAsSearchTitle: true,
  searchTitle: "",
  usesDescriptionAsSearchDescription: true,
  searchDescription: "",
  usesOpenGraphImageAsSearchImage: true,
  searchImage: ""
});
```

### Search Metadata Settings

Control how the page appears in internal site search results:

```typescript
// Get search metadata properties
const searchTitle = await page.getSearchTitle();
const searchDescription = await page.getSearchDescription();

// Set search metadata properties
await page.setSearchTitle("Custom Search Title");
await page.setSearchDescription("Custom search description");

// Check if search metadata inherits the page title/description
const isSearchTitle = await page.usesTitleAsSearchTitle();
const isSearchDescription = await page.usesDescriptionAsSearchDescription();

// Use the page title/description for search metadata
await page.useTitleAsSearchTitle(true);
await page.useDescriptionAsSearchDescription(true);

// Check if page is excluded from site search
const isExcluded = await page.isExcludedFromSearch();

// Exclude page from site search
await page.excludeFromSearch(true);

// Get and set the search image
const searchImage = await page.getSearchImage();
await page.setSearchImage("https://example.com/search-image.jpg");

// Use the Open Graph image as the search image
const isSearchImage = await page.useOpenGraphImageAsSearchImage(true);
```

### Open Graph Metadata Settings

Control social media sharing (e.g. Facebook) appearance:

```typescript
// Get Open Graph properties
const ogTitle = await page.getOpenGraphTitle();
const ogDescription = await page.getOpenGraphDescription();
const ogImage = await page.getOpenGraphImage();

// Set Open Graph properties
await page.setOpenGraphTitle("Social Share Title");
await page.setOpenGraphDescription("Description shown on social media");
await page.setOpenGraphImage("https://example.com/og-image.jpg");

// Check if the page uses the page title/description for Open Graph metadata
const isOpenGraphTitle = await page.usesTitleAsOpenGraphTitle();
const isOpenGraphDescription = await page.usesDescriptionAsOpenGraphDescription();

// Use the page title/description for Open Graph metadata
await page.useTitleAsOpenGraphTitle(true);
await page.useDescriptionAsOpenGraphDescription(true);
```

### Page Status

```typescript
// Check page settings
const isDraft = await page.isDraft();
const isPasswordProtected = await page.isPasswordProtected();
const isHomepage = await page.isHomepage();

// Set draft status
await page.setDraft(true);
```

### Create Page

```typescript
const newPage = await webflow.createPage();
await newPage.setName("New Page");
await newPage.setSlug("new-page");
await newPage.setTitle("New Page Title");
await webflow.switchPage(newPage);
```

> **Note**: `createPage()` takes no parameters. Use setter methods to configure the page after creation. The method will error if the page limit for the user's plan is exceeded.

## Folders

Folders organize pages into directories. Also known as "Page Folders" or subdirectories (e.g. `example.com/legal/privacy-policy` where "legal" is a folder).  

### Create Folder
```typescript
const folder = await webflow.createPageFolder();
await folder.setName("Blog Posts");
```

### Folder Properties
```typescript
// Get folder info
const folderName = await folder.getName();
const folderSlug = await folder.getSlug();

// Update folder info
await folder.setName("New Folder Name");
await folder.setSlug("new-folder-slug");
```

### Nested Folders
```typescript
// Create parent and child folders
const parentFolder = await webflow.createPageFolder();
await parentFolder.setName("Resources");

const childFolder = await webflow.createPageFolder();
await childFolder.setName("Downloads");
await childFolder.setParent(parentFolder);
```

### Get Parent Folder
```typescript
const parent = await folder.getParent();
```

### URL Impact

> **Warning**: Moving pages or folders changes URLs. Old URLs return 404. Use 301 redirects to maintain SEO.

```
Before: example.com/privacy-policy
After moving to "legal" folder: example.com/legal/privacy-policy
```

## Workflow Examples

### Update Page Metadata
```typescript
async function updatePageMetadata(page, title, description) {

  // Get the current page if no page was provided
  const targetPage = page ?? await webflow.getCurrentPage();

  await targetPage.setTitle(title);
  await targetPage.setDescription(description);

  // Use the page title and description for site search results
  await targetPage.useTitleAsSearchTitle(true);
  await targetPage.useDescriptionAsSearchDescription(true);

  // Use the page title and description for the Open Graph tags
  await targetPage.useTitleAsOpenGraphTitle(true);
  await targetPage.useDescriptionAsOpenGraphDescription(true);

  await webflow.notify({ type: 'Success', message: `Page metadata updated for ${title}` });
}
```

### Organize Pages into Folder
```typescript
async function createOrganizedFolder(folderName, folderSlug) {
  const folder = await webflow.createPageFolder();
  await folder.setName(folderName);
  await folder.setSlug(folderSlug);
  return folder;
}
```

### Bulk Update Page Metadata
```typescript
async function updateAllPageMetadata() {
  const pagesAndFolders = await webflow.getAllPagesAndFolders();
  const pages = pagesAndFolders?.filter((i): i is Page => i.type === "Page");

  for (const page of pages) {
    // Use the page title and description for site search results
    await page.useTitleAsSearchTitle(true);
    await page.useDescriptionAsSearchDescription(true);

    // Use the page title and description for the Open Graph tags
    await page.useTitleAsOpenGraphTitle(true);
    await page.useDescriptionAsOpenGraphDescription(true);
  }
}
```

## Best Practices

1. **Set fields intentionally**: Treat `name` as internal labeling and `description` as the page meta description.
2. **Keep metadata in sync**: Use `useTitleAsSearchTitle(true)` and `useDescriptionAsSearchDescription(true)` when search metadata should mirror page metadata.
3. **Avoid URL breakage**: Plan folder/slug changes ahead and pair moves with 301 redirects.
4. **Prefer bulk updates when possible**: Use `setMetadata()` for coordinated updates to page, search, and Open Graph settings.
