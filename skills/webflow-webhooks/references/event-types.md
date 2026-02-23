---
name: "Webhook Event Types"
description: "Complete reference for all 14 Webflow webhook event types, including required scopes, payload properties, and example payloads for forms, site publishing, pages, ecommerce, comments, and CMS collection items."
tags: [events, trigger-types, form-submission, site-publish, page-created, page-deleted, page-metadata-updated, ecomm-new-order, ecomm-order-changed, ecomm-inventory-changed, comment-created, collection-item-created, collection-item-changed, collection-item-deleted, collection-item-unpublished, collection-item-published, payloads, scopes]
---

# Webhook Event Types

All Webflow webhook events follow a consistent envelope structure:

```json
{
  "triggerType": "event_name",
  "payload": {
    // Event-specific data
  }
}
```

## Quick Reference

| Event | Category | Required Scope | Description |
|-------|----------|----------------|-------------|
| `form_submission` | Forms | `forms:read` | Form submitted on site |
| `site_publish` | Site | `sites:read` | Site is published |
| `page_created` | Pages | `pages:read` | New page created |
| `page_metadata_updated` | Pages | `pages:read` | Page metadata changed and published |
| `page_deleted` | Pages | `pages:read` | Page deleted |
| `ecomm_new_order` | Ecommerce | `ecommerce:read` | New order placed |
| `ecomm_order_changed` | Ecommerce | `ecommerce:read` | Order status/details changed |
| `ecomm_inventory_changed` | Ecommerce | `ecommerce:read` | Product inventory changed |
| `comment_created` | Comments | `comments:read` | New comment thread or reply created |
| `collection_item_created` | CMS | `cms:read` | CMS item created |
| `collection_item_changed` | CMS | `cms:read` | CMS item updated |
| `collection_item_deleted` | CMS | `cms:read` | CMS item deleted |
| `collection_item_unpublished` | CMS | `cms:read` | CMS item unpublished |
| `collection_item_published` | CMS | `cms:read` | CMS item published (different payload — `items` array) |

> **Localization note:** If you delete a collection item across multiple locales, the webhook triggers once for each locale.

---

## Forms

### `form_submission`

Triggered when a form is submitted on a Webflow site.

**Required Scope:** `forms:read`

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | The name of the form |
| `siteId` | string | The id of the site the form was submitted from |
| `data` | object | Key-value pairs for each submitted field |
| `schema` | array | Array of field definitions with `fieldName`, `fieldType`, and `fieldElementId`. Valid `fieldType` values: `FormTextInput`, `FormTextarea`, `FormCheckboxInput`, `FormRadioInput`, `FormFileUploadInput` |
| `submittedAt` | string | ISO8601 timestamp of submission |
| `id` | string | Unique form submission id |
| `formId` | string | The id of the form definition |
| `formElementId` | string | The element id of the form in the Designer |

```json
{
  "triggerType": "form_submission",
  "payload": {
    "name": "Contact Us",
    "siteId": "65427cf400e02b306eaa049c",
    "data": {
      "First Name": "Zaphod",
      "Last Name": "Beeblebrox",
      "email": "zaphod@heartofgold.ai",
      "Phone Number": 15550000000
    },
    "schema": [
      {
        "fieldName": "First Name",
        "fieldType": "FormTextInput",
        "fieldElementId": "285042f7-d554-dc7f-102c-aa10d6a2d2c4"
      },
      {
        "fieldName": "Last Name",
        "fieldType": "FormTextInput",
        "fieldElementId": "285042f7-d554-dc7f-102c-aa10d6a2d2c5"
      },
      {
        "fieldName": "email",
        "fieldType": "FormTextInput",
        "fieldElementId": "285042f7-d554-dc7f-102c-aa10d6a2d2c6"
      },
      {
        "fieldName": "Phone Number",
        "fieldType": "FormTextInput",
        "fieldElementId": "285042f7-d554-dc7f-102c-aa10d6a2d2c7"
      }
    ],
    "submittedAt": "2022-09-14T12:35:16.117Z",
    "id": "6321ca84df3949bfc6752327",
    "formId": "65429eadebe8a9f3a30f62d0",
    "formElementId": "4e038d2c-6a1e-4953-7be9-a59a2b453177"
  }
}
```

---

## Site

### `site_publish`

Triggered when a site is published.

**Required Scope:** `sites:read`

| Field | Type | Description |
|-------|------|-------------|
| `siteId` | string | The identifier for the published site |
| `publishedOn` | string | ISO8601 timestamp of the publish event |
| `domains` | string[] | Domains the site was published to |
| `publishedBy` | object | Contains `id` and `displayName` of the user who published |

```json
{
  "triggerType": "site_publish",
  "payload": {
    "siteId": "62749158efef318abc8d5a0f",
    "publishedOn": "2023-07-31T12:34:56.789Z",
    "domains": ["my-website.webflow.io"],
    "publishedBy": {
      "id": "545bbecb7bdd6769632504a7",
      "displayName": "Some One"
    }
  }
}
```

---

## Pages

### `page_created`

Triggered when a new page is created.

**Required Scope:** `pages:read`

| Field | Type | Description |
|-------|------|-------------|
| `siteId` | string | ID of the site the page is on |
| `pageId` | string | ID of the new page |
| `pageTitle` | string | Title of the page |
| `createdOn` | string | ISO8601 timestamp of creation |
| `publishedPath` | string | The published path of the page |

```json
{
  "triggerType": "page_created",
  "payload": {
    "siteId": "63499e4e6e9ed55a17e42b68",
    "pageId": "641371d477a18c936fe237cd",
    "pageTitle": "This is a New Page",
    "createdOn": "2023-03-16T19:45:24.311Z",
    "publishedPath": "/my-new-page"
  }
}
```

### `page_metadata_updated`

Triggered when page metadata is updated and published.

**Required Scope:** `pages:read`

| Field | Type | Description |
|-------|------|-------------|
| `siteId` | string | ID of the site the page is on |
| `pageId` | string | ID of the updated page |
| `pageTitle` | string | Title of the page |
| `lastUpdated` | string | ISO8601 timestamp of the update |
| `publishedPath` | string | The published path of the page |

```json
{
  "triggerType": "page_metadata_updated",
  "payload": {
    "siteId": "63499e4e6e9ed55a17e42b68",
    "pageId": "641371d477a18c936fe237cd",
    "pageTitle": "Home",
    "lastUpdated": "2023-03-16T19:48:48.499Z",
    "publishedPath": "/"
  }
}
```

### `page_deleted`

Triggered when a page is deleted.

**Required Scope:** `pages:read`

| Field | Type | Description |
|-------|------|-------------|
| `siteId` | string | ID of the site the page was on |
| `pageId` | string | ID of the deleted page |
| `pageTitle` | string | Title of the page |
| `deletedOn` | string | ISO8601 timestamp of deletion |
| `publishedPath` | string | The published path of the deleted page |

```json
{
  "triggerType": "page_deleted",
  "payload": {
    "siteId": "63499e4e6e9ed55a17e42b68",
    "pageId": "63499e4e6e9ed5abbfe42b69",
    "pageTitle": "Old contact page",
    "deletedOn": "2023-03-16T19:51:33.068Z",
    "publishedPath": "/contact"
  }
}
```

---

## Ecommerce

### `ecomm_new_order`

Triggered when a new ecommerce order is placed.

**Required Scope:** `ecommerce:read`

| Field | Type | Description |
|-------|------|-------------|
| `orderId` | string | Order id (6 or 9 hex characters) |
| `status` | string | One of `pending`, `unfulfilled`, `fulfilled`, `disputed`, `dispute-lost`, `refunded` |
| `comment` | string | API-editable comment for the order |
| `orderComment` | string | Customer's comment on the order |
| `acceptedOn` | string \| null | ISO8601 timestamp when order was placed |
| `disputedOn` | string \| null | ISO8601 timestamp if disputed |
| `disputeUpdatedOn` | string \| null | ISO8601 timestamp of last dispute update |
| `disputeLastStatus` | string \| null | Stripe dispute status if disputed. One of `warning_needs_response`, `warning_under_review`, `warning_closed`, `needs_response`, `under_review`, `charge_refunded`, `won`, `lost` |
| `fulfilledOn` | string \| null | ISO8601 timestamp if fulfilled |
| `refundedOn` | string \| null | ISO8601 timestamp if refunded |
| `customerPaid` | OrderAmount | Amount the customer paid (`unit`, `value`, `string`) |
| `netAmount` | OrderAmount | Net amount after fees (`unit`, `value`, `string`) |
| `applicationFee` | OrderAmount | Application fee assessed by the platform |
| `isShippingRequired` | boolean | Whether order contains one or more items that require shipping |
| `shippingProvider` | string \| null | Shipping provider name (API-editable, not used by Webflow) |
| `shippingTracking` | string \| null | Shipping tracking number (API-editable, not used by Webflow) |
| `shippingTrackingURL` | string \| null | Shipping tracking URL |
| `customerInfo` | object | Customer `fullName` and `email` |
| `allAddresses` | OrderAddress[] | All addresses (billing + shipping) |
| `shippingAddress` | OrderAddress | Shipping address |
| `billingAddress` | OrderAddress | Billing address |
| `purchasedItems` | OrderPurchasedItem[] | Array of purchased items with product/variant details |
| `purchasedItemsCount` | number | Sum of all `count` fields in `purchasedItems` |
| `stripeDetails` | object | Stripe `subscriptionId`, `paymentMethod`, `paymentIntentId`, `customerId`, `chargeId`, `disputeId`, `refundId`, `refundReason` (all nullable) |
| `stripeCard` | object | Card `last4`, `brand`, `ownerName`, `expires`. Brand is one of `Visa`, `American Express`, `MasterCard`, `Discover`, `JCB`, `Diners Club`, `Unknown` |
| `paypalDetails` | object | PayPal `orderId`, `payerId`, `captureId`, `refundId`, `refundReason`, `disputeId` |
| `totals` | OrderTotals | Subtotal, extras (tax, shipping, discounts), and total |
| `customData` | object[] | Custom order fields (`textInput`, `textArea`, `checkbox`) |
| `metadata` | object | Contains `isBuyNow` boolean |
| `isCustomerDeleted` | boolean | Whether the customer has been deleted from the site |
| `hasDownloads` | boolean | Whether the order contains downloadable items |
| `paymentProcessor` | string | Payment processor used for this order |
| `downloadFiles` | object[] | Downloadable file objects with `id`, `name`, `url` |

**Shared Types:**

- **OrderAmount**: `{ unit: string, value: string, string: string }` — `unit` is a three-letter ISO currency code, `value` is the numeric amount in the base unit of the currency
- **OrderAddress**: `{ type, japanType, addressee, line1, line2, city, state, country, postalCode }` — `type` is `shipping` or `billing`; `japanType` (`kana` | `kanji` | null) only appears on orders placed from Japan
- **OrderPurchasedItem**: `{ count, rowTotal, productId, productName, productSlug, variantId, variantName, variantSlug, variantSKU, variantImage, variantPrice, height, length, weight, width }`
- **OrderTotals**: `{ subtotal: OrderAmount, extras: [{ type, name, description, price }], total: OrderAmount }` — extras `type` is one of `discount`, `discount-shipping`, `shipping`, `tax`

```json
{
  "triggerType": "ecomm_new_order",
  "payload": {
    "orderId": "dfa-3f1",
    "status": "unfulfilled",
    "acceptedOn": "2018-12-03T22:06:15.761Z",
    "customerPaid": { "unit": "USD", "value": 6099, "string": "$60.99" },
    "netAmount": { "unit": "USD", "value": 5892, "string": "$58.92" },
    "isShippingRequired": true,
    "customerInfo": {
      "fullName": "Customerio Namen",
      "email": "renning+customer@webflow.com"
    },
    "purchasedItems": [
      {
        "count": 1,
        "rowTotal": { "unit": "USD", "value": 5500, "string": "$55.00" },
        "productId": "5eb9fd05caef491eb9757183",
        "productName": "White Cup",
        "productSlug": "white-cup",
        "variantId": "5eb9fcace279761d8199790c",
        "variantName": "white-cup_default_sku",
        "variantPrice": { "unit": "USD", "value": 5500, "string": "$55.00" }
      }
    ],
    "totals": {
      "subtotal": { "unit": "USD", "value": 5500, "string": "$55.00" },
      "extras": [
        { "type": "tax", "name": "State Taxes", "description": "CA Taxes (6.25%)", "price": { "unit": "USD", "value": 344, "string": "$3.44" } },
        { "type": "shipping", "name": "Flat Rate", "price": { "unit": "USD", "value": 599, "string": "$5.99" } },
        { "type": "discount", "name": "Discount (SAVE5)", "price": { "unit": "USD", "value": -500, "string": "-$ 5.00 USD" } }
      ],
      "total": { "unit": "USD", "value": 6122, "string": "$61.22" }
    }
  }
}
```

### `ecomm_order_changed`

Triggered when an order's status or details change. Payload structure is identical to `ecomm_new_order`.

**Required Scope:** `ecommerce:read`

### `ecomm_inventory_changed`

Triggered when product inventory changes.

**Required Scope:** `ecommerce:read`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the SKU item |
| `quantity` | number | Remaining inventory count (if finite) |
| `inventoryType` | string | `infinite` or `finite` |

```json
{
  "triggerType": "ecomm_inventory_changed",
  "payload": {
    "id": "5bfedb42bab0ad90fa7dad39",
    "quantity": 83,
    "inventoryType": "finite"
  }
}
```

---

## Comments

### `comment_created`

Triggered when a new comment thread is created or a reply is added.

> **Note:** There may be a delay of up to 5 minutes before new comments appear in the system and trigger the webhook notification.

**Required Scope:** `comments:read`

| Field | Type | Description |
|-------|------|-------------|
| `threadId` | string | Unique identifier for the comment thread |
| `commentId` | string | Unique identifier for the comment reply |
| `type` | string | The type of comment payload (thread or reply) |
| `siteId` | string | The site unique identifier |
| `pageId` | string | The page unique identifier |
| `localeId` | string \| null | The locale unique identifier |
| `itemId` | string \| null | The item unique identifier |
| `breakpoint` | string | The breakpoint the comment was left on |
| `url` | string | The URL of the page the comment was left on |
| `content` | string | The content of the comment |
| `isResolved` | boolean | Whether the comment thread is resolved |
| `author` | object | Contains `userId`, `email`, and `name` of the author |
| `mentionedUsers` | array | Array of mentioned users, each with `userId`, `email`, `name`. Empty until email notifications are sent (up to 5 minutes after creation) |
| `createdOn` | string | ISO8601 timestamp of creation |
| `lastUpdated` | string | ISO8601 timestamp of last update |

```json
{
  "triggerType": "comment_created",
  "payload": {
    "threadId": "64a7f5e2b3c1d2e4f5a6b7c8",
    "commentId": "64a7f5e2b3c1d2e4f5a6b7c9",
    "type": "thread",
    "siteId": "63499e4e6e9ed55a17e42b68",
    "pageId": "641371d477a18c936fe237cd",
    "localeId": null,
    "itemId": null,
    "breakpoint": "main",
    "url": "https://my-website.webflow.io/about",
    "content": "Can we update the hero image here?",
    "isResolved": false,
    "author": {
      "userId": "545bbecb7bdd6769632504a7",
      "email": "designer@example.com",
      "name": "Some One"
    },
    "mentionedUsers": [],
    "createdOn": "2024-01-15T10:30:00.000Z",
    "lastUpdated": "2024-01-15T10:30:00.000Z"
  }
}
```

---

## CMS Collection Items

The events `collection_item_created`, `collection_item_changed`, `collection_item_deleted`, and `collection_item_unpublished` all share an identical payload structure. The `collection_item_published` event differs — it wraps items in an `items` array.

### `collection_item_created`

Triggered when a CMS collection item is created.

**Required Scope:** `cms:read`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the item |
| `siteId` | string | Site ID where the collection lives |
| `workspaceId` | string | Workspace ID where the site lives |
| `collectionId` | string | Collection ID the item belongs to |
| `cmsLocaleId` | string \| null | Locale identifier for the item (null if localization is not enabled) |
| `lastPublished` | string \| null | ISO8601 timestamp of last publish (null if never published) |
| `lastUpdated` | string | ISO8601 timestamp of last update |
| `createdOn` | string | ISO8601 timestamp of creation |
| `isArchived` | boolean | Whether the item is archived |
| `isDraft` | boolean | Whether the item is a draft |
| `fieldData` | object | Item data structured per the collection's schema. Always includes required `name` and `slug` fields, plus any custom fields defined on the collection. For localized items, contains data per locale. |

```json
{
  "triggerType": "collection_item_created",
  "payload": {
    "id": "582b900cba19143b2bb8a759",
    "siteId": "1111111",
    "workspaceId": "1111111",
    "collectionId": "1111111",
    "cmsLocaleId": "699b93f1a6406af4b29614b4",
    "lastPublished": null,
    "lastUpdated": "2023-03-27T22:26:40.926Z",
    "createdOn": "2023-03-27T22:26:40.926Z",
    "isArchived": false,
    "isDraft": true,
    "fieldData": {
      "name": "hello world",
      "slug": "hello-world",
      "favoriteColor": "#ff00ff"
    }
  }
}
```

### `collection_item_changed`

Triggered when a CMS item is updated. Identical payload structure to `collection_item_created`.

**Required Scope:** `cms:read`

### `collection_item_deleted`

Triggered when a CMS item is deleted. Identical payload structure to `collection_item_created`.

**Required Scope:** `cms:read`

### `collection_item_unpublished`

Triggered when a CMS item is unpublished. Identical payload structure to `collection_item_created`.

**Required Scope:** `cms:read`

### `collection_item_published`

Triggered when a CMS item is published. Unlike other CMS events, the payload wraps items in an `items` array.

> **Note:** This event is not listed on Webflow's official [All Events](https://developers.webflow.com/data/reference/all-events) documentation page, but is a valid `triggerType` accepted by the API. The official OpenAPI spec incorrectly shows a flat payload structure identical to the other CMS events — in practice, the payload wraps items in an `items` array as documented below.

**Required Scope:** `cms:read`

| Field | Type | Description |
|-------|------|-------------|
| `items` | array | Array of published item objects |
| `items[].id` | string | Unique identifier for the item |
| `items[].siteId` | string | Site ID where the collection lives |
| `items[].workspaceId` | string | Workspace ID where the site lives |
| `items[].collectionId` | string | Collection ID the item belongs to |
| `items[].cmsLocaleId` | string \| null | Locale identifier for the item (null if localization is not enabled) |
| `items[].lastPublished` | string \| null | ISO8601 timestamp of last publish |
| `items[].lastUpdated` | string | ISO8601 timestamp of last update |
| `items[].createdOn` | string | ISO8601 timestamp of creation |
| `items[].isArchived` | boolean | Whether the item is archived |
| `items[].isDraft` | boolean | Whether the item is a draft |
| `items[].fieldData` | object | Item data structured per the collection's schema |

```json
{
  "triggerType": "collection_item_published",
  "payload": {
    "items": [
      {
        "id": "699b9529a9f8b010bafa9671",
        "siteId": "6876e40ec4e60da1478fdc0f",
        "workspaceId": "6875887fa03e727e0e0dd03d",
        "collectionId": "699b93f1d1611a428291c333",
        "cmsLocaleId": "699b93f1a6406af4b29614b4",
        "lastPublished": null,
        "lastUpdated": "2026-02-22T23:45:45.885Z",
        "createdOn": "2026-02-22T23:45:45.885Z",
        "isArchived": false,
        "isDraft": true,
        "fieldData": {}
      }
    ]
  }
}
```

---

## Webhook Limits

| Criteria | Limit |
|----------|-------|
| Max webhooks per trigger type per site | 75 |
| Retry attempts on failure | 3 (at 10-minute intervals) |
| Required response status | 200 (anything else = failure) |

**Failure conditions:** Non-200 HTTP status, redirects, or SSL certificate issues.