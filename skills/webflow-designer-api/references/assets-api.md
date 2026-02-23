---
name: "Assets API"
description: "Reference for uploading, managing, and organizing media assets including images, documents, and Lottie animations."
tags: [assets, createAsset, getAssetById, getAllAssets, createAssetFolder, getAllAssetFolders, getUrl, getName, setName, getAltText, setAltText, getMimeType, setFile, setFolder, getParent, setAsset, getAsset, upload, image, file, media, alt-text, accessibility, batch-upload, asset-folder, supported-file-types, lottie]
---

# Assets API Reference

Manage site assets including images, documents, and Lottie animations. Upload new assets, organize with folders, and set properties like alt text for accessibility.

## Table of Contents

- [Creating Assets](#creating-assets)
- [Retrieving Assets](#retrieving-assets)
- [Using Assets on Elements](#using-assets-on-elements)
- [Asset Properties](#asset-properties)
- [Supported File Types](#supported-file-types)
- [Asset Folders](#asset-folders)
- [Workflow Examples](#workflow-examples)
- [Best Practices](#best-practices)

---

## Creating Assets

### From Remote URL
```typescript
const response = await fetch("https://picsum.photos/400/300");
const blob = await response.blob();
const file = new File([blob], "image.jpg", { type: 'image/jpeg' });

const asset = await webflow.createAsset(file);
```

### From File Input
```typescript
const fileInput = document.getElementById('file-input') as HTMLInputElement;
const file = fileInput.files?.[0];

if (!file) {
  await webflow.notify({ type: 'Error', message: 'Select a file to upload' });
  return;
}

const asset = await webflow.createAsset(file);
```

> **Note**: Images must not exceed 4MB and documents must not exceed 10MB.

## Retrieving Assets

### By ID
```typescript
const asset = await webflow.getAssetById(assetId);
```

### All Assets
```typescript
const assets = await webflow.getAllAssets();
```

## Using Assets on Elements

### Add Image with Asset
```typescript
// Create asset
const response = await fetch("https://picsum.photos/400/300");
const blob = await response.blob();
const file = new File([blob], "photo.jpg", { type: 'image/jpeg' });
const asset = await webflow.createAsset(file);
await asset.setAltText('Placeholder image');

// Insert image element
const selected = await webflow.getSelectedElement();
if (selected) {
  const img = await selected.after(webflow.elementPresets.Image);
  await img.setAsset(asset);
}
```

## Asset Properties

```typescript
const assets = await webflow.getAllAssets()
const asset = assets[0];

// Name
const name = await asset.getName();
await asset.setName("New asset name");

// Alt Text
const altText = await asset.getAltText();
await asset.setAltText("Updated alt text"); // Pass null to mark asset as decorative

// MIME Type
const mimeType = await asset.getMimeType();

// URL
const url = await asset.getUrl();

// Replace the file of an existing asset with a new file
const newFile = new File([blob], "updated-photo.jpg", { type: 'image/jpeg' });
await asset.setFile(newFile);
```

## Supported File Types
```
'image/jpeg'
'image/jpg'
'image/png'
'image/gif'
'image/svg+xml'
'image/bmp'
'image/webp'
'application/pdf'
'application/msword'
'application/vnd.ms-excel'
'application/vnd.ms-powerpoint'
'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
'application/vnd.openxmlformats-officedocument.presentationml.presentation'
'text/plain'
'text/csv'
'application/vnd.oasis.opendocument.text'
'application/vnd.oasis.opendocument.spreadsheet'
'application/vnd.oasis.opendocument.presentation'
'application/json'
```

## Asset Folders

### Get All Folders
```typescript
const folders = await webflow.getAllAssetFolders();
```

### Create Folder
```typescript
const folder = await webflow.createAssetFolder("Icons");
```

### Get Folder Name
```typescript
const folderName = await folder.getName();
```

### Get Folder of Asset
```typescript
const folder = await asset.getParent();
```

### Move Asset to Folder
```typescript
await asset.setFolder(folder);
```

## Workflow Examples

### Get Selected Image Asset

```typescript
async function getSelectedImage() {

  const selected = await webflow.getSelectedElement();
  
  if (selected?.type === 'Image') {

    const asset = await selected.getAsset();
    const name = await asset.getName();

    await webflow.notify({ type: 'Info', message: `Selected image: ${name}` });

    return asset;

  } else {

    await webflow.notify({ type: 'Error', message: 'No image element selected' });
    return null;

  }

}
```

### Batch Upload Assets from File Input

```typescript
async function batchUploadAssets() {
  const fileInput = document.getElementById('file-input') as HTMLInputElement;
  const files = fileInput.files;

  if (!files || files.length === 0) {
    await webflow.notify({ type: 'Error', message: 'Select files to upload' });
    return;
  }

  for (const file of files) {
    try {
      await webflow.createAsset(file);
      await webflow.notify({ type: 'Success', message: `Uploaded ${file.name}` });
    } catch (err) {
      await webflow.notify({ type: 'Error', message: `Failed to upload ${file.name}` });
    }
  }
}
```

### Set Alt Text for Accessibility

```typescript
async function setAltTextForSelectedImage(altText: string) {
  const selected = await webflow.getSelectedElement();
  
  if (selected?.type === 'Image') {
    const asset = await selected.getAsset();
    await asset.setAltText(altText);
    await webflow.notify({ type: 'Success', message: 'Alt text updated' });
  } else {
    await webflow.notify({ type: 'Error', message: 'No image element selected' });
  }
}
```

## Best Practices

1. **Optimize images**: Compress images before upload
2. **Use descriptive names**: Name files semantically
3. **Always set alt text**: Important for accessibility and SEO
4. **Organize with folders**: Group related assets
5. **Use appropriate formats**: WebP for photos, SVG for icons
