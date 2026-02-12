---
name: "Code Examples"
description: "Cross-API workflow examples combining elements, styles, variables, assets, components, and pages in realistic scenarios."
tags: [examples, workflows, cross-api, elements, styles, variables, assets, components, pages, card, gallery, image, seo, design-tokens, picsum, batch-upload, grid, responsive, metadata]
---

# Code Examples

End-to-end examples that combine multiple Designer APIs in realistic workflows.

## Table of Contents

- [Build a Styled Card Section](#build-a-styled-card-section)
- [Upload and Insert an Image Gallery](#upload-and-insert-an-image-gallery)
- [Create a Reusable Styled Component](#create-a-reusable-styled-component)
- [Page Setup with SEO and Design Tokens](#page-setup-with-seo-and-design-tokens)

---

## Build a Styled Card Section

**APIs used:** [Elements](./elements-api.md), [Styles](./styles-api.md), [Variables](./variables-api.md)

Creates a card section with a heading, paragraph, and button, styled using design token variables for consistent theming. Includes responsive font sizing for smaller breakpoints.

```typescript
async function buildStyledCardSection() {
  const selected = await webflow.getSelectedElement();
  if (!selected) {
    await webflow.notify({ type: 'Error', message: 'Select an element first' });
    return;
  }

  // --- Variables: create design tokens ---

  const collection = await webflow.getDefaultVariableCollection();

  const primaryColor = await collection.createColorVariable('card-primary', '#146EF5');
  const textColor = await collection.createColorVariable('card-text', '#1E1E1E');
  const bgColor = await collection.createColorVariable('card-bg', '#FFFFFF');
  const spacingMd = await collection.createSizeVariable('card-spacing', { unit: 'px', value: 24 });
  const radiusVar = await collection.createSizeVariable('card-radius', { unit: 'px', value: 12 });

  // --- Styles: create card styles using variables ---

  const cardStyle = await webflow.createStyle('CardSection');
  await cardStyle.setProperties({
    'background-color': bgColor,
    'padding-top': spacingMd,
    'padding-bottom': spacingMd,
    'padding-left': spacingMd,
    'padding-right': spacingMd,
    'border-radius': radiusVar,
  });

  const headingStyle = await webflow.createStyle('CardHeading');
  await headingStyle.setProperties({
    'color': textColor,
    'font-size': '32px',
    'font-weight': '700',
    'margin-bottom': '12px',
  });
  await headingStyle.setProperties(
    { 'font-size': '24px' },
    { breakpoint: 'medium' }
  );
  await headingStyle.setProperties(
    { 'font-size': '20px' },
    { breakpoint: 'small' }
  );

  const paragraphStyle = await webflow.createStyle('CardParagraph');
  await paragraphStyle.setProperties({
    'color': textColor,
    'font-size': '16px',
    'line-height': '1.6',
    'margin-bottom': '20px',
  });

  const buttonStyle = await webflow.createStyle('CardButton');
  await buttonStyle.setProperties({
    'background-color': primaryColor,
    'color': '#FFFFFF',
    'padding-top': '12px',
    'padding-bottom': '12px',
    'padding-left': '24px',
    'padding-right': '24px',
    'border-radius': '8px',
    'font-weight': '600',
    'font-size': '16px',
  });

  const primaryBinding = await primaryColor.getBinding();
  await buttonStyle.setProperties(
    { 'background-color': `color-mix(in srgb, ${primaryBinding}, black 15%)` },
    { pseudo: 'hover' }
  );

  // --- Elements: build the card structure ---

  const section = await selected.after(webflow.elementPresets.Section);
  await section.setStyles([cardStyle]);

  if (!section.children) return;

  const wrapper = await section.append(webflow.elementPresets.DivBlock);
  if (!wrapper.children) return;

  const heading = await wrapper.append(webflow.elementPresets.Heading);
  await heading.setTextContent('Ready to get started?');
  await heading.setStyles([headingStyle]);

  const paragraph = await wrapper.append(webflow.elementPresets.Paragraph);
  await paragraph.setTextContent('Build beautiful, responsive websites with the power of design tokens and reusable styles.');
  await paragraph.setStyles([paragraphStyle]);

  const button = await wrapper.append(webflow.elementPresets.Button);
  await button.setTextContent('Get started');
  await button.setStyles([buttonStyle]);

  await webflow.notify({ type: 'Success', message: 'Card section created' });
}
```

## Upload and Insert an Image Gallery

**APIs used:** [Assets](./assets-api.md), [Elements](./elements-api.md), [Styles](./styles-api.md)

Fetches images from [picsum.photos](https://picsum.photos), uploads them as assets with alt text, then builds a responsive grid gallery on the page.

```typescript
async function uploadAndInsertGallery() {
  const selected = await webflow.getSelectedElement();
  if (!selected) {
    await webflow.notify({ type: 'Error', message: 'Select an element first' });
    return;
  }

  // --- Assets: fetch and upload images ---

  const imageCount = 4;

  const assets = [];
  for (let i = 0; i < imageCount; i++) {
    try {
      const response = await fetch(`https://picsum.photos/800/600?random=${i}`);
      const blob = await response.blob();
      const file = new File([blob], `gallery-${i + 1}.jpg`, { type: 'image/jpeg' });

      const asset = await webflow.createAsset(file);
      await asset.setAltText(`Gallery image ${i + 1}`);
      assets.push(asset);
    } catch (err) {
      await webflow.notify({ type: 'Error', message: `Failed to upload image ${i + 1}` });
    }
  }

  if (assets.length === 0) {
    await webflow.notify({ type: 'Error', message: 'No images uploaded' });
    return;
  }

  // --- Styles: create gallery and image styles ---

  // Webflow requires the full name for CSS properties in the API, so we use 'padding-top' instead of 'padding', and 'row-gap'/'column-gap' for grid gaps.
  const galleryStyle = await webflow.createStyle('ImageGallery');
  await galleryStyle.setProperties({
    'padding-top': '24px',
    'padding-bottom': '24px',
    'padding-left': '24px',
    'padding-right': '24px',
    'row-gap': '16px',
    'column-gap': '16px',
  });

  const imageStyle = await webflow.createStyle('GalleryImage');
  await imageStyle.setProperties({
    'width': '100%',
    'border-radius': '8px',
  });

  // --- Elements: build the gallery using Grid preset ---

    /**
   * This example uses presets so we can use Webflow-native elements like `Section`, `Grid`, and `Image`. The `elementBuilder()` API only supports `webflow.elementPresets.DOM` (custom DOM elements), so it’s best used when you’re inserting a larger DOM-only tree and want to reduce API calls. Refer to the 'Using Element Builder' section in the [Elements API reference](./elements-api.md) for more details and examples on how to use `elementBuilder()` effectively.
   */

  const section = await selected.after(webflow.elementPresets.Section);
  if (!section.children) return;

  const grid = await section.append(webflow.elementPresets.Grid);
  await grid.setStyles([galleryStyle]);

  if (!grid.children) return;

  for (const asset of assets) {
    const img = await grid.append(webflow.elementPresets.Image);
    await img.setAsset(asset);
    await img.setStyles([imageStyle]);
  }

  await webflow.notify({ type: 'Success', message: `Gallery created with ${assets.length} images` });
}
```

## Create a Reusable Styled Component

**APIs used:** [Elements](./elements-api.md), [Styles](./styles-api.md), [Components](./components-api.md)

Builds a testimonial card element tree, styles it, and registers the structure as a reusable component.

```typescript
async function createTestimonialComponent() {
  const selected = await webflow.getSelectedElement();
  if (!selected) {
    await webflow.notify({ type: 'Error', message: 'Select an element first' });
    return;
  }

  // --- Styles: create testimonial styles ---

  const cardStyle = await webflow.createStyle('TestimonialCard');
  await cardStyle.setProperties({
    'background-color': '#F9FAFB',
    'padding-top': '32px',
    'padding-bottom': '32px',
    'padding-left': '24px',
    'padding-right': '24px',
    'border-radius': '12px',
  });

  const quoteStyle = await webflow.createStyle('TestimonialQuote');
  await quoteStyle.setProperties({
    'font-size': '18px',
    'line-height': '1.6',
    'color': '#374151',
    'font-style': 'italic',
    'margin-bottom': '16px',
  });
  await quoteStyle.setProperties(
    { 'font-size': '16px' },
    { breakpoint: 'small' }
  );

  const authorStyle = await webflow.createStyle('TestimonialAuthor');
  await authorStyle.setProperties({
    'font-size': '14px',
    'font-weight': '600',
    'color': '#6B7280',
  });

  // --- Elements: build the styled testimonial on the canvas ---

  /**
   * This example uses presets so we can use Webflow-native elements like `DivBlock` and `Paragraph`. The `elementBuilder()` API only supports `webflow.elementPresets.DOM` (custom DOM elements), so it's best used when you're inserting a larger DOM-only tree and want to reduce API calls. Refer to the 'Using Element Builder' section in the [Elements API reference](./elements-api.md) for more details and examples on how to use `elementBuilder()` effectively.
   */

  const card = await selected.after(webflow.elementPresets.DivBlock);
  await card.setStyles([cardStyle]);

  if (!card.children) return;

  const quote = await card.append(webflow.elementPresets.Paragraph);
  await quote.setTextContent('"This product completely transformed how our team works. Highly recommended."');
  await quote.setStyles([quoteStyle]);

  const author = await card.append(webflow.elementPresets.Paragraph);
  await author.setTextContent('— Jane Smith, CEO at Acme Corp');
  await author.setStyles([authorStyle]);

  // --- Components: register as component (converts the elements into a component instance in-place) ---

  const component = await webflow.registerComponent('Testimonial Card', card);
  const name = await component.getName();

  await webflow.notify({ type: 'Success', message: `Element "${name}" also created as component` });
}
```

## Page Setup with SEO and Design Tokens

**APIs used:** [Pages](./pages-api.md), [Variables](./variables-api.md), [Styles](./styles-api.md), [Elements](./elements-api.md)

Creates a new page, sets SEO metadata and Open Graph fields, creates design token variables, and inserts a styled hero heading on the page.

```typescript
async function setupPageWithSEO() {
  // --- Pages: create and configure page ---
  const pageName = 'Demo Page';
  const slug = 'demo-page';

  const page = await webflow.createPage();
  await page.setName(pageName);
  await page.setSlug(slug);
  await page.setTitle(`${pageName} | My Site`);
  await page.setDescription(`Learn more about ${pageName.toLowerCase()} and what we offer.`);

  // Sync SEO fields
  await page.useTitleAsSearchTitle(true);
  await page.useDescriptionAsSearchDescription(true);

  // Set Open Graph
  await page.useTitleAsOpenGraphTitle(true);
  await page.useDescriptionAsOpenGraphDescription(true);

  // Set OG image using a placeholder
  await page.setOpenGraphImage('https://picsum.photos/1200/630');

  // Navigate to the new page
  await webflow.switchPage(page);

  // --- Variables: create page-specific design tokens ---

  const collection = await webflow.getDefaultVariableCollection();

  const headingColor = await collection.createColorVariable('hero-heading-color', '#111827');
  const heroSize = await collection.createSizeVariable('hero-heading-size', {
    type: 'custom',
    value: 'clamp(2rem, 5vw, 3.5rem)',
  });

  // --- Styles: create hero heading style ---

  const heroStyle = await webflow.createStyle('HeroHeading');
  await heroStyle.setProperties({
    'color': headingColor,
    'font-size': heroSize,
    'font-weight': '800',
    'line-height': '1.1',
    'margin-bottom': '24px',
  });

  // --- Elements: insert a hero heading on the new page ---

    /**
   * This example uses presets so we can use Webflow-native elements like `Section`, `DivBlock`, and `Heading`. The `elementBuilder()` API only supports `webflow.elementPresets.DOM` (custom DOM elements), so it's best used when you're inserting a larger DOM-only tree and want to reduce API calls. Refer to the 'Using Element Builder' section in the [Elements API reference](./elements-api.md) for more details and examples on how to use `elementBuilder()` effectively.
   */

  const root = await webflow.getRootElement();
  if (!root?.children) return;

  const section = await root.append(webflow.elementPresets.Section);
  if (!section.children) return;

  const container = await section.append(webflow.elementPresets.DivBlock);
  if (!container.children) return;

  const heading = await container.append(webflow.elementPresets.Heading);
  await heading.setTextContent(pageName);
  await heading.setStyles([heroStyle]);

  await webflow.notify({ type: 'Success', message: `Page "${pageName}" created with SEO and hero` });
}
```
