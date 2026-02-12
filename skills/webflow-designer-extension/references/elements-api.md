---
name: "Elements API"
description: "Reference for element selection, insertion, removal, properties, presets, and the element builder for bulk operations."
tags: [elements, getSelectedElement, getAllElements, setSelectedElement, after, before, append, prepend, remove, children, elementPresets, elementBuilder, DivBlock, Section, Grid, VFlex, HFlex, QuickStack, Row, Paragraph, Heading, TextLink, LinkBlock, Image, DOM, setTag, setAttribute, getAllCustomAttributes, setCustomAttribute, getCustomAttribute, removeCustomAttribute, textContent, setTextContent, getTextContent, createStyle, setProperties, setStyles, getStyles, getAllAttributes, getAttribute, removeAttribute, getHeadingLevel, setHeadingLevel, getAsset, setAltText, getTarget, setSettings, getRequired, setRequired, getInputType, setInputType]
---

# Elements API Reference

Reference for selecting, inserting, removing, and updating elements on the current page.

## Table of Contents

- [Element Selection](#element-selection)
- [Inserting and Removing Elements](#inserting-and-removing-elements)
- [Element Presets](#element-presets)
- [Custom DOM Elements](#custom-dom-elements)
- [Element Properties](#element-properties)
- [Element Types and Methods](#element-types-and-methods)
- [Workflow Examples](#workflow-examples)
- [Best Practices](#best-practices)

---

## Element Selection

### Get Selected Element
```typescript
const el = await webflow.getSelectedElement();
```

### Get All Elements
```typescript
const elements = await webflow.getAllElements();
```

### Set Selected Element
```typescript
await webflow.setSelectedElement(elementToSelect);
```

### Get Children and Set Selected to First Child
```typescript
const element = await webflow.getSelectedElement();
if (element?.children && element.children.length > 0) {
  await webflow.setSelectedElement(element.children[0]);
}
```

## Inserting and Removing Elements

### After (Sibling)
```typescript
const element = await webflow.getSelectedElement();
if (!element) throw new Error('No element selected');

// Add a new element after the current element
const newEl = await element.after(webflow.elementPresets.DivBlock);
```

### Before (Sibling)
```typescript
const element = await webflow.getSelectedElement();
if (!element) throw new Error('No element selected');

// Add a new element before the current element
const newEl = await element.before(webflow.elementPresets.Paragraph);
```

### Append (Last Child)
```typescript
// Add a new element as the last child of the current element
const parentElement = await webflow.getSelectedElement();
if (parentElement?.children) {
  const child = await parentElement.append(webflow.elementPresets.Image);
}
```

### Prepend (First Child)
```typescript
// Add a new element as the first child of the current element
const parentElement = await webflow.getSelectedElement();
if (parentElement?.children) {
  const child = await parentElement.prepend(webflow.elementPresets.Heading);
}
```

### Removing Elements

```typescript
const element = await webflow.getSelectedElement();
if (!element) throw new Error('No element selected');

await element.remove();
```

### Using Element Builder
```typescript
const parentElement = await webflow.getSelectedElement();

// Use only webflow.elementPresets.DOM elements with the builder
const section = webflow.elementBuilder(webflow.elementPresets.DOM);
section.setTag("section");

const container = section.append(webflow.elementPresets.DOM);
container.setTag("div");
container.setAttribute("class", "container");

const heading = container.append(webflow.elementPresets.DOM);
heading.setTag("h1");

const subheading = container.append(webflow.elementPresets.DOM);
subheading.setTag("h2");

if (parentElement?.children) {
  await parentElement.append(section);
}

const elements = await webflow.getAllElements();
const headingEl = elements.find(el => el.id.element === heading.id);
if (headingEl) { await headingEl.setTextContent("Hello World"); }
const subheadingEl = elements.find(el => el.id.element === subheading.id);
if (subheadingEl) { await subheadingEl.remove(); }
```

> **Note**: The 'element builder' is similar to using a document fragment in JavaScript, you can build out a complex structure in memory and then add it to the canvas in a single operation, which is more efficient than adding multiple elements one at a time. Only DOM elements can be used with the element builder, not presets that create specific element types like `Image` or `Heading`.

## Element Presets

Access via `webflow.elementPresets`:

| Category | Presets |
|----------|---------|
| Layout & Structure | `DivBlock`, `DOM`, `Grid`, `HFlex`, `QuickStack`, `Row`, `Section`, `VFlex` |
| Typography & Content | `Blockquote`, `Heading`, `List`, `ListItem`, `Paragraph`, `RichText`, `TextBlock` |
| Navigation & Interactive | `Button`, `DropdownWrapper`, `LightboxWrapper`, `LinkBlock`, `NavbarWrapper`, `Pagination`, `SliderWrapper`, `TabsWrapper`, `TextLink` |
| Forms | `FormBlockLabel`, `FormButton`, `FormCheckboxInput`, `FormFileUploadWrapper`, `FormForm`, `FormRadioInput`, `FormReCaptcha`, `FormSelect`, `FormTextarea`, `FormTextInput` |
| Pre-built Layouts | `LayoutFeaturesList`, `LayoutFeaturesMetrics`, `LayoutFeaturesTable`, `LayoutFooterDark`, `LayoutFooterLight`, `LayoutFooterSubscribe`, `LayoutGalleryOverview`, `LayoutGalleryScroll`, `LayoutGallerySlider`, `LayoutHeroHeadingCenter`, `LayoutHeroHeadingLeft`, `LayoutHeroHeadingRight`, `LayoutHeroStack`, `LayoutHeroSubscribeLeft`, `LayoutHeroSubscribeRight`, `LayoutHeroWithoutImage`, `LayoutLogosQuoteBlock`, `LayoutLogosQuoteDivider`, `LayoutLogosTitleLarge`, `LayoutLogosTitleSmall`, `LayoutLogosWithoutTitle`, `LayoutNavbarLogoCenter`, `LayoutNavbarLogoLeft`, `LayoutNavbarNoShadow`, `LayoutPricingComparison`, `LayoutPricingItems`, `LayoutPricingOverview`, `LayoutTeamCircles`, `LayoutTeamSlider`, `LayoutTestimonialColumnDark`, `LayoutTestimonialColumnLight`, `LayoutTestimonialImageLeft`, `LayoutTestimonialSliderLarge`, `LayoutTestimonialSliderSmall`, `LayoutTestimonialStack`, `StructureLayoutQuickStack1plus2`, `StructureLayoutQuickStack1x1`, `StructureLayoutQuickStack2plus1`, `StructureLayoutQuickStack2x1`, `StructureLayoutQuickStack2x2`, `StructureLayoutQuickStack3x1`, `StructureLayoutQuickStack4x1`, `StructureLayoutQuickStackMasonry` |
| E-commerce | `CommerceAddToCartWrapper`, `CommerceCartQuickCheckoutActions`, `CommerceCartWrapper`, `CommerceCheckoutAdditionalInfoSummaryWrapper`, `CommerceCheckoutAdditionalInputsContainer`, `CommerceCheckoutCustomerInfoSummaryWrapper`, `CommerceCheckoutDiscounts`, `CommerceCheckoutFormContainer`, `CommerceCheckoutOrderItemsWrapper`, `CommerceCheckoutOrderSummaryWrapper`, `CommerceCheckoutPaymentSummaryWrapper`, `CommerceCheckoutShippingSummaryWrapper`, `CommerceDownloadsWrapper`, `CommerceOrderConfirmationContainer`, `CommercePayPalCheckoutButton`, `CommercePaypalCheckoutFormContainer` |
| CMS & Dynamic Content | `DynamoWrapper` |
| Media & Embeds | `BackgroundVideoWrapper`, `Facebook`, `HtmlEmbed`, `Image`, `MapWidget`, `Spline`, `Twitter`, `Video`, `YouTubeVideo` |
| Advanced & Miscellaneous | `Animation`, `BlockContainer`, `CodeBlock`, `IX2InstanceFactoryOnClass`, `IX2InstanceFactoryOnElement`, `SearchForm` |

## Custom DOM Elements

For elements without presets:

```typescript
const custom = webflow.elementBuilder(webflow.elementPresets.DOM);
custom.setTag("article");
custom.setAttribute("class", "my-class");
custom.setAttribute("data-custom", "value");

const parentElement = await webflow.getSelectedElement();
if (parentElement?.children) {
  await parentElement.append(custom);
}
```

## Element Properties

### Custom Attributes
```typescript
const element = await webflow.getSelectedElement();
if (!element) {
  await webflow.notify({ type: 'Error', message: 'Select an element' });
  return;
}

const customAttributes = await element.getAllCustomAttributes();
await element.setCustomAttribute("data-test", "123");
const attrValue = await element.getCustomAttribute('data-test');
await element.removeCustomAttribute('data-test');
```

### Text Content
```typescript
const element = await webflow.getSelectedElement();
if (!element) {
  await webflow.notify({ type: 'Error', message: 'Select an element' });
  return;
}

await element.setTextContent("New text content");
const text = await element.getTextContent();
```

### Styles
```typescript
const element = await webflow.getSelectedElement();
if (!element) {
  await webflow.notify({ type: 'Error', message: 'Select an element' });
  return;
}

const newStyle = await webflow.createStyle("MyCustomStyle");

await newStyle.setProperties({
  'background-color': "blue",
  'font-size': "32px",
  'font-weight': "bold",
});

await element.setStyles([newStyle]);
const styles = await element.getStyles();
```

See [Styles API Reference](./styles-api.md) for more on creating and managing styles.

## Element Types and Methods

### DOM Elements
```typescript
const elements = await webflow.getAllElements()
const DOMElement = elements.find(element => element.type === "DOM")

if (!DOMElement) {
  await webflow.notify({ type: 'Error', message: 'No DOM element found on the page' });
  return;
}

const tag = await DOMElement.getTag();
await DOMElement.setTag("section");

// 'Custom attributes' are only used for existing element presets. For DOM elements, use the generic get/set/removeAttribute methods instead.
await DOMElement.getAllAttributes();
await DOMElement.setAttribute("data-test", "value");
await DOMElement.getAttribute("data-test");
await DOMElement.removeAttribute("data-test");
```

### String Elements
```typescript
const elements = await webflow.getAllElements()
const stringElement = elements.find(element => element.type === "String")

if (!stringElement) {
  await webflow.notify({ type: 'Error', message: 'No String element found on the page' });
  return;
}

const text = await stringElement.getText();
await stringElement.setText("Updated text content");
```

### Components
```typescript
const elements = await webflow.getAllElements()
const componentInstance = elements.find(element => element.type === "ComponentInstance")

if (!componentInstance) {
  await webflow.notify({ type: 'Error', message: 'No ComponentInstance found on the page' });
  return;
}

const component = await componentInstance.getComponent();
const componentName = await component.getName();
```

See the [Components API Reference](./components-api.md) for more information on creating and managing components.

### Heading Elements
```typescript
const elements = await webflow.getAllElements()
const heading = elements.find(element => element.type === "Heading")

if (!heading) {
  await webflow.notify({ type: 'Error', message: 'No Heading element found on the page' });
  return;
}

const level = await heading.getHeadingLevel(); // 1-6
await heading.setHeadingLevel(2);
```

### Image Elements
```typescript
const elements = await webflow.getAllElements()
const image = elements.find(element => element.type === "Image")

if (!image) {
  await webflow.notify({ type: 'Error', message: 'No Image element found on the page' });
  return;
}

const asset = await image.getAsset();
const altText = await asset.getAltText();
await asset.setAltText(null); // Mark image as decorative
```

See the [Assets API Reference](./assets-api.md) for more information on managing assets and using them with elements.

### Link Elements
```typescript
const elements = await webflow.getAllElements()
const link = elements.find(element => element.type === "Link")

if (!link) {
  await webflow.notify({ type: 'Error', message: 'No Link element found on the page' });
  return;
}

// The target value can be a string, Page, Element, or an Asset object.
const target = await link.getTarget();

// Available settings: element.setSettings( mode: 'url' | 'page' | 'pageSection' | 'email' | 'phone' | 'attachment'; target: string | Page | Element | Asset; metadata?: {openInNewTab?: boolean; subject?: string;} ): Promise<null>
await link.setSettings('url', 'https://www.example.com', { openInNewTab: true });
```

### Form Elements
```typescript
const elements = await webflow.getAllElements()
const form = elements.find(element => element.type === "FormForm" || element.type === "FormWrapper")

if (!form) {
  await webflow.notify({ type: 'Error', message: 'No form element found on the page' });
  return;
}

const name = await form.getName();
await form.setName("Contact form");

const formSettings = await form.getSettings();

/** Available settings:
{
  state: FormState; (‘normal’, ‘success’, or ‘error’)
  name: string;
  redirect: string;
  action: string;
  method: FormMethod; (‘get’ or ‘post’)
}
*/

await form.setSettings({ ...formSettings, redirect: "https://www.example.com/thank-you" });

// See below for managing form fields, which have their own applicable methods and properties.
```

#### Form Fields
```typescript
const elements = await webflow.getAllElements()

const formInputTypes = [
  'FormCheckboxInput',
  'FormFileUploadWrapper', 
  'FormRadioInput',
  'FormSelect',
  'FormTextarea',
  'FormTextInput'
];

const formField = elements.find(element => formInputTypes.includes(element.type));

if (!formField) {
  await webflow.notify({ type: 'Error', message: 'No form field element found on the page' });
  return;
}

const isRequired = await formField.getRequired();
await formField.setRequired(true);

const name = await formField.getName();
await formField.setName("Updated label");

const type = await formField.getInputType(); // 'text' | 'email' | 'password' | 'tel' | 'number' | 'url'
await formField.setInputType('email');
```

## Workflow Examples

### Insert a Simple CTA Section

Inserts a new `Section` after the selected element, then adds a heading, paragraph, and button.

> **Note**: This example uses presets because it needs Webflow-native elements like `Section` and `Button`. The `elementBuilder()` API only supports `webflow.elementPresets.DOM` (custom DOM elements), so it’s best used when you’re inserting a larger DOM-only tree and want to reduce API calls.

```typescript
async function insertCtaSection() {
  const selected = await webflow.getSelectedElement();
  if (!selected) {
    await webflow.notify({ type: 'Error', message: 'Select an element to insert after' });
    return;
  }

  const section = await selected.after(webflow.elementPresets.Section);
  if (!section.children) {
    await webflow.notify({ type: 'Error', message: 'Inserted section cannot contain children' });
    return;
  }

  const wrapper = await section.append(webflow.elementPresets.DivBlock);
  if (!wrapper.children) return;

  const heading = await wrapper.append(webflow.elementPresets.Heading);
  await heading.setTextContent('Ready to get started?');

  const paragraph = await wrapper.append(webflow.elementPresets.Paragraph);
  await paragraph.setTextContent('Add a short supporting message here.');

  const button = await wrapper.append(webflow.elementPresets.Button);
  await button.setTextContent('Get started');
  await button.setSettings('url', 'https://example.com', { openInNewTab: true });

  await webflow.notify({ type: 'Success', message: 'CTA section inserted' });
}
```

### Set Alt Text for Selected Image

Updates the selected image's asset alt text. (Alt text is stored on the asset.)

```typescript
async function setSelectedImageAltText(altText: string | null) {
  const selected = await webflow.getSelectedElement();
  if (!selected || selected.type !== 'Image') {
    await webflow.notify({ type: 'Error', message: 'Select an Image element' });
    return;
  }

  const asset = await selected.getAsset();
  await asset.setAltText(altText);

  await webflow.notify({ type: 'Success', message: 'Alt text updated' });
}
```

### Normalize All Headings to H2

```typescript
async function normalizeHeadingsToH2() {
  const elements = await webflow.getAllElements();
  const headings = elements.filter((el) => el.type === 'Heading');

  for (const heading of headings) {
    await heading.setHeadingLevel(2);
  }

  await webflow.notify({ type: 'Success', message: `Updated ${headings.length} headings` });
}
```

## Best Practices

1. **Always check capabilities:**
   ```typescript
   if (element.children) { /* can have children */ }
   if (element.textContent !== undefined) { /* has text */ }
   ```

2. **Handle null elements:**
   ```typescript
   const el = await webflow.getSelectedElement();
   if (!el) {
     await webflow.notify({ type: 'Error', message: 'Select an element' });
     return;
   }
   ```

3. **Use element builder for complex structures** to minimize API calls
