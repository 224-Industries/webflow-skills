---
name: "Pages API"
description: "Reference for page and folder management including creation, SEO settings, Open Graph metadata, and URL structure."
tags: [pages, folders, getCurrentPage, getAllPages, createPage, getAllFolders, createFolder, getName, setName, getSlug, setSlug, getTitle, setTitle, setMetaDescription, setOgTitle, setOgDescription, setOgImage, setIndexable, setFolder, isDraft, isPasswordProtected, seo, open-graph, url-structure, page-settings, page-metadata, redirects]
---

# Pages & Folders API Reference

Manage site organizational structure, page settings, and metadata.

## Pages

### Get Current Page
```typescript
const page = await webflow.getCurrentPage();
```

### Get All Pages
```typescript
const pages = await webflow.getAllPages();
```

### Page Properties

```typescript
// Get page info
const name = await page.getName();
const slug = await page.getSlug();
const title = await page.getTitle();

// Update page info
await page.setName("New Page Name");
await page.setSlug("new-page-slug");
await page.setTitle("New Page Title | Site Name");
```

### SEO Settings

```typescript
// Meta description
await page.setMetaDescription("Page description for search engines");

// Meta keywords (if applicable)
await page.setMetaKeywords(["keyword1", "keyword2"]);

// Canonical URL
await page.setCanonicalUrl("https://example.com/page");

// Robots settings
await page.setIndexable(true);  // Allow indexing
await page.setFollowLinks(true);  // Allow following links
```

### Open Graph Settings

Control social media sharing appearance:

```typescript
await page.setOgTitle("Social Share Title");
await page.setOgDescription("Description shown on social media");
await page.setOgImage(asset);  // Asset for og:image
```

### Page Status

```typescript
// Check page settings
const isDraft = await page.isDraft();
const isPasswordProtected = await page.isPasswordProtected();
const isHomePage = await page.isHomePage();
```

### Create Page

```typescript
const newPage = await webflow.createPage({
  name: "New Page",
  slug: "new-page",
  title: "New Page Title"
});
```

## Folders

Folders organize pages into directories. Also known as "Page Folders" or subdirectories.

### Get All Folders
```typescript
const folders = await webflow.getAllFolders();
```

### Create Folder
```typescript
const folder = await webflow.createFolder("Blog Posts");
```

### Nested Folders
```typescript
// Create subfolder
const parentFolder = await webflow.createFolder("Resources");
const childFolder = await webflow.createFolder("Downloads", parentFolder);
```

### Move Page to Folder
```typescript
await page.setFolder(folder);
```

### URL Impact

> **Warning**: Moving pages or folders changes URLs. Old URLs return 404. Use 301 redirects to maintain SEO.

```
Before: example.com/old-page
After moving to "blog" folder: example.com/blog/old-page
```

## Workflow Examples

### Update Page SEO
```typescript
async function optimizePageSEO(page, title, description) {
  await page.setTitle(title);
  await page.setMetaDescription(description);
  await page.setOgTitle(title);
  await page.setOgDescription(description);
  await page.setIndexable(true);
  
  await webflow.notify({ type: 'Success', message: 'SEO updated' });
}
```

### Organize Pages into Folder
```typescript
async function organizePages(folderName, pageNames) {
  const folder = await webflow.createFolder(folderName);
  const allPages = await webflow.getAllPages();
  
  for (const pageName of pageNames) {
    const page = allPages.find(p => p.getName() === pageName);
    if (page) {
      await page.setFolder(folder);
    }
  }
}
```

## Best Practices

1. **Plan URL structure**: Consider folder hierarchy before moving pages
2. **Set up redirects**: Create 301 redirects after moving pages
3. **Complete SEO fields**: Fill title, description, and Open Graph for each page
4. **Use descriptive slugs**: Clean, keyword-rich URLs improve SEO
