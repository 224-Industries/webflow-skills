---
name: "Assets API"
description: "Reference for uploading, managing, and organizing media assets including images, documents, and Lottie animations."
tags: [assets, createAsset, getAssetById, getAllAssets, createAssetFolder, getUrl, getName, getAltText, setAltText, getMimeType, setFolder, setAsset, getAsset, upload, image, file, media, alt-text, accessibility, batch-upload, asset-folder, supported-file-types, lottie]
---

# Assets API Reference

Manage site media files through the Designer's Assets panel.

## Creating Assets

### From Remote URL
```typescript
const response = await fetch("https://example.com/image.jpg");
const blob = await response.blob();
const file = new File([blob], "image.jpg", { type: 'image/jpeg' });

const asset = await webflow.createAsset(file);
```

### From File Input
```typescript
const fileInput = document.getElementById('file-input') as HTMLInputElement;
const file = fileInput.files[0];

const asset = await webflow.createAsset(file);
```

### Set Alt Text
```typescript
await asset.setAltText('Description of the image');
```

## Getting Assets

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
const url = await asset.getUrl();        // Hosted URL
const name = await asset.getName();      // Filename
const altText = await asset.getAltText(); // Alt text
const mimeType = await asset.getMimeType();
```

## Supported File Types

### Images
```
image/jpeg, image/jpg, image/png, image/gif
image/svg+xml, image/bmp, image/webp
```

### Documents
```
application/pdf
application/msword
application/vnd.ms-excel
application/vnd.ms-powerpoint
application/vnd.openxmlformats-officedocument.wordprocessingml.document
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
application/vnd.openxmlformats-officedocument.presentationml.presentation
text/plain
text/csv
application/vnd.oasis.opendocument.text
application/vnd.oasis.opendocument.spreadsheet
application/vnd.oasis.opendocument.presentation
```

### Special
```
application/json  (for Lottie animations)
```

## Asset Folders

### Create Folder
```typescript
const folder = await webflow.createAssetFolder("Icons");
```

### Move Asset to Folder
```typescript
await asset.setFolder(folder);
```

## Workflow Example: Batch Upload

```typescript
async function uploadImages(urls: string[]) {
  const assets = [];
  
  for (const url of urls) {
    try {
      const response = await fetch(url);
      const blob = await response.blob();
      const filename = url.split('/').pop() || 'image.jpg';
      const file = new File([blob], filename, { type: blob.type });
      
      const asset = await webflow.createAsset(file);
      assets.push(asset);
    } catch (err) {
      console.error(`Failed to upload ${url}:`, err);
    }
  }
  
  await webflow.notify({ 
    type: 'Success', 
    message: `Uploaded ${assets.length} images` 
  });
  
  return assets;
}
```

## Workflow Example: Replace Element Image

```typescript
async function replaceImageAsset(imageUrl: string, altText: string) {
  const selected = await webflow.getSelectedElement();
  
  if (!selected || selected.type !== 'Image') {
    await webflow.notify({ type: 'Error', message: 'Select an image element' });
    return;
  }
  
  // Fetch and create asset
  const response = await fetch(imageUrl);
  const blob = await response.blob();
  const file = new File([blob], 'updated-image.jpg', { type: 'image/jpeg' });
  const asset = await webflow.createAsset(file);
  await asset.setAltText(altText);
  
  // Update element
  await selected.setAsset(asset);
  
  await webflow.notify({ type: 'Success', message: 'Image updated' });
}
```

## Privacy Note

> Assets uploaded to the Assets panel are publicly accessible via their URLs but are not automatically indexed by search engines unless linked on a public page.

## Best Practices

1. **Optimize images**: Compress images before upload
2. **Use descriptive names**: Name files semantically
3. **Always set alt text**: Important for accessibility and SEO
4. **Organize with folders**: Group related assets
5. **Use appropriate formats**: WebP for photos, SVG for icons
