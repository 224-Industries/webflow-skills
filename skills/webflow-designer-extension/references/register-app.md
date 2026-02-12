---
name: "Register an App"
description: "Step-by-step guide to registering a Webflow App, configuring capabilities, OAuth settings, and managing app security."
tags: [register, app, workspace, admin, client-id, client-secret, oauth, redirect-uri, scopes, designer-extension, data-client, hybrid-app, installation, capabilities, publishing, troubleshooting, security, cors]
---

# Register an App

## Table of Contents

- [Prerequisites](#prerequisites)
- [Steps to Register](#steps-to-register)
- [App Visibility](#app-visibility)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## Prerequisites

- A Webflow account
- A Webflow Workspace with Admin permissions

> **Admin access required:** Only Workspace admins can create apps, view client secrets, upload bundles, and modify app settings.

## Steps to Register

### 1. Open the Webflow Dashboard

Login to your Webflow account and navigate to your Dashboard.

### 2. Choose a Workspace

Select the Workspace for your app. It's recommended to create a dedicated development workspace to keep apps organized and separate from production environments.

> **New to Webflow?** Get started with Webflow's free [Developer Workspace](https://developers.webflow.com/data/docs/developer-workspace.md) designed for testing and developing Apps.

### 3. Navigate to Workspace Settings

From the "Settings" menu on the left sidebar, select the "Apps & Integrations" tab. Scroll down to the "App Development" section and click the "Create an App" button.

### 4. Add App Details

Provide the following basic information:

| Field | Description |
|---|---|
| Name | The name of your app |
| Description | Brief summary of your app's purpose (140 characters max) |
| Icon | An icon to represent your app |
| Homepage URL | A valid HTTPS link to your app's website |

**Installation settings (optional):** You can restrict app installation to a specific site by toggling the "Restrict app installation to a specific site" option. When enabled, users authorize your app for a single site at a time. When disabled (default), users can authorize for multiple sites or their entire Workspace.

### 5. Define App Capabilities

Select the capabilities your app needs:

- **Designer Extension** — Enables your app to interact with the Webflow Designer
- **Data Client** — Enables your app to access and update data from Webflow's servers

You can select one or both (selecting both creates a hybrid app).

**Data Client OAuth configuration:** If you selected Data Client, configure:

- **Scopes** — Choose the specific API permissions your app requires (sites, collections, assets, etc.)
- **Redirect URI** — Enter a valid HTTPS URL where users are redirected after authorization. This is a critical security component of the OAuth flow. You can add or modify redirect URIs later.

Click "Create app" to finalize registration.

### 6. Review Your App

On successful registration, your app appears in the App Development section with your Client ID and Client Secret. From here you can update details, capabilities, and installation settings.

**Designer Extension details:**

- **Publish Extension Version** — Upload a new version of your Designer Extension with version notes
- **Designer Extension URI** — The URI where your extension is served within the Designer iframe (important for CORS configuration)
- **Versions** — View all previously published versions for tracking and rollback

> **App Security:**
> - Never commit your Client Secret to version control (e.g., GitHub)
> - Rotate your Client Secret if it's ever exposed. In other words, if you suspect it has been compromised then regenerate it immediately.
> - Store secrets in environment variables or a secure secret management system (e.g. Infisical)
> - Implement proper CORS policies for Designer Extensions

## App Visibility

New apps are only available to users in your app's workspace. External users can't install your app until it's approved and published in the Webflow Marketplace. You can invite external test users before submitting for review.

Want to test your app with a small group before going live? You can request to add up to 5 test users by emailing developers@webflow.com with their Webflow emails. Once added, share your app’s install URL so they can try it out.

## Troubleshooting

### Invalid Redirect URI error

- Ensure the redirect URI matches **exactly** what you registered
- Check for trailing slashes — `https://example.com/callback` and `https://example.com/callback/` are different URIs
- For localhost development, ensure the port number matches exactly
- For Ngrok or tunneling services, the URL changes on restart — update your registered URI accordingly

### Can't see App Development section

- Verify you're in the correct Workspace with Admin permissions
- Confirm your account is email-verified with 2FA enabled
- Navigate to Workspace Settings > App Development (not Site Settings)
- Your Webflow plan must support app development (Team and Enterprise plans)

### External users can't install

New apps are workspace-only until approved and published in the Marketplace. Invite external test users to your workspace for pre-submission testing.

## Next Steps

- **Data Client** — Access and manipulate Webflow site data (CMS collections, items, assets, form submissions) through API endpoints
- **Designer Extension** — Create extensions that automate design tasks, manipulate elements, and enhance the Designer
- **Hybrid App** — Use both Data Client and Designer Extension together
