---
name: "FAQ & Troubleshooting"
description: "Frequently asked questions and troubleshooting for Designer Extensions, Marketplace Apps, and common issues."
tags: [faq, troubleshooting, testing, frameworks, iframe, serve, bundle, upload, permissions, admin, marketplace, private-app, install, credentials, client-secret, development-mode, css-conflicts, responsive, scopes, errors]
---

# FAQ & Troubleshooting

## Table of Contents

- [Designer Extensions](#designer-extensions)
- [Marketplace Apps](#marketplace-apps)
- [Troubleshooting](#troubleshooting)

---

## Designer Extensions

### Which frameworks and libraries can I use?

You can use any framework that outputs static resources and runs in a browser environment. Ensure your extension fits within the iframe dimensions provided by Webflow.

### How do I test my Designer Extension?

1. **Install on a test site** — In your workspace sidebar, navigate to Apps & Integrations > Develop. Click "..." next to your app and select Install App. Authorize it for the sites or workspace you want to test on.
2. **Run in development mode** — Navigate to your project folder and run:
   ```bash
   webflow extension serve
   ```
   This starts development mode locally (port 1337).
3. **Preview in the Designer** — Open the Apps pane on your test site, find your app, and click "Launch Development App" to interact with your locally hosted extension.

### Why isn't my extension interacting with Webflow as expected?

- Double-check your use of the Designer APIs and ensure you're using the correct methods
- Check the browser console for errors and review error handling patterns
- Designer APIs only access content on the current page, not other sites or pages
- Verify your app has the right permissions and scopes
- For Data API issues, confirm correct endpoints and valid tokens

### Why does my app look different in Webflow than expected?

- Designer Extensions run in an iframe with controlled dimensions — check your configuration and use `webflow.setExtensionSize()` if needed
- Use scoped CSS or scoped class names to avoid style conflicts with Webflow's native styles
- Test at different viewport sizes to ensure responsive behavior

### Why can't I upload a new version of my Designer Extension bundle?

Only Workspace admins can upload new bundles. Contact your Workspace administrator to upload or grant you the necessary permissions.

## Marketplace Apps

### Do I have to publicly share my app on the Marketplace?

No. You can publish as a **private app** and control who can install it. Select "Private" in the "Marketplace Visibility" section during submission. Private apps go through the same review process as public apps.

### Can I update my app after it's been published?

Yes. Submit updates at any time via the "Submit an App" form, selecting "App Update" as the submission type. Updates go through the same review process.

## Troubleshooting

### Why can't other users install my app?

Only apps published to the Marketplace (publicly or privately) can be installed by other users. Submit your app for review to make it available.

> **Testing before publishing:** Email developers@webflow.com with up to 5 Webflow user emails. The team can add them to a test group so they can install and use your app.

### Why isn't my app showing up in Webflow?

- Ensure you've bundled your app with the Webflow CLI and uploaded your Designer Extension via the Dashboard
- Confirm the app is installed on your site or workspace (check the App Development section)

### Why can't I view or update my app credentials?

Only Workspace admins can view client secrets, edit app details, or create new apps. Contact your Workspace administrator for access.
