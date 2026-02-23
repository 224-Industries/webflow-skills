---
name: "App Submission & Listing"
description: "Complete guide to submitting a Webflow App and creating an effective Marketplace listing, including technical requirements, assets, categories, and installation configuration."
tags: [submission, listing, marketplace, publish, review, app-name, description, screenshots, logo, categories, assets, installation-url, oauth, demo-video, update, technical-requirements, two-factor-auth, submission-form, private-app, bundle, deep-link]
---

# App Submission & Listing

## Table of Contents

- [Submission Process Overview](#submission-process-overview)
- [Technical Requirements](#technical-requirements)
- [Submission Preparation](#submission-preparation)
- [Submit Your App](#submit-your-app)
- [App Listing](#app-listing)
- [Installation Configuration](#installation-configuration)
- [Post-Submission](#post-submission)

---

## Submission Process Overview

1. Prepare technical requirements and submission assets
2. Submit for review via the [Webflow App submission form](https://developers.webflow.com/submit)
3. Respond to feedback (if needed)
4. Publicize and share your app upon approval

## Technical Requirements

Your app must meet these requirements to be listed on the Webflow Marketplace:

- Two-factor authentication enabled for an admin account on the workspace
- App has been thoroughly tested and is fully functional
- App has clear documentation and error handling
- App follows Webflow's security best practices and privacy guidelines

## Submission Preparation

### 1. Test your app and onboarding flow

Ensure your app is fully functional and meets all technical requirements. For Data Client or Hybrid Apps, verify your onboarding flow works as expected and provide an installation URL for users to connect your service with Webflow.

To test with users outside your registered workspace, submit your app for review as a private app.

### 2. Upload your Designer Extension bundle

For Designer Extensions, upload the `bundle.zip` file created using the Webflow CLI via the App version manager within the Webflow Designer.

### 3. Grant Webflow access to your app

Provide Webflow with complete access to test all features:

- An active demo account with full functionality
- Access to any gated or premium features
- Required test credentials (e.g., API keys, login details)
- Sample data or resources needed to evaluate core functionality
- Additional materials needed to test edge cases or special features

### 4. Enable backend services

Backend services and APIs must be fully operational and accessible throughout the review process, including third-party integrations, databases, and microservices.

### 5. Create a demo video

Create a comprehensive demo video (2-5 min) demonstrating key features and a complete walkthrough from installation to usage. Host via Loom (private link), YouTube (unlisted/private), or Google Drive (shared link).

For Data Client apps, include a working OAuth flow showing users approving and denying the request.

### 6. Document complex features and pricing

Document any complex features, pricing tiers, and in-app purchases in your review notes and demo video. Include relevant visuals and external documentation links.

### 7. Create marketplace listing assets

Prepare all required information and visual assets (see sections below).

## Submit Your App

Submit via the [Webflow App submission form](https://developers.webflow.com/submit). A complete submission with all required details will expedite the review process.

## App Listing

Your app appears in two key locations:

1. **Webflow Marketplace** — The primary discovery hub where users browse and explore apps
2. **Apps pane in the Webflow Designer** — Where users search and install apps while building

### Required Information

| Asset | Requirements | Tips |
|---|---|---|
| App name | Max 30 characters | Keep it clear and memorable |
| Publisher name | Max 20 characters | Keep it clear and memorable |
| Short description | Max 100 characters | Focus on core value proposition |
| Long description | Max 10,000 characters | Supports Markdown but not links |
| Feature list | Max 5 features | Highlight key capabilities |
| Website URL | Valid URL | Link to your app's website |
| Privacy policy URL | Valid URL | Link to your privacy policy |
| Terms of service URL | Valid URL | Link to your terms of service |
| Support email | Valid email | Provide a way for users to get support |

### Visual Assets

| Asset | Requirements | Tips |
|---|---|---|
| App logo | 900x900px, 1:1 ratio | Logomarks (pictoral marks) accepted; logotypes (text) not accepted |
| Promo video | 1-2 min | Optional — host on YouTube |
| Publisher logo | 20x20px | Must be recognizable at small size |
| Screenshots | 1280x846px | Min. 4 recommended, show key workflows |

> **Publisher branding:** Your publisher logo and name are inherited from your publishing Workspace. Update them in your workspace settings.

### Categories

Select up to **5 categories** that best describe your app's functionality:

| Category | Description |
|---|---|
| AI | AI and machine learning for content generation, data analysis, and more |
| Analytics | Track, analyze, and report website metrics and user behavior |
| Asset Management | Organize, store, and manage digital assets (images, videos, documents) |
| Automation | Automate tasks, workflows, and processes |
| Compliance | Legal, security, and regulatory compliance (GDPR, CCPA, accessibility) |
| Content Management | Create, manage, and organize website content and CMS integrations |
| Customer Support | Help desk, chat support, and customer communication |
| Data Sync | Synchronize data between Webflow and other platforms |
| Design | UI components, templates, and design resources |
| Development and Coding | Developer tools, custom code, and programming utilities |
| Ecommerce | Payment processing, inventory management, shopping cart |
| Forms and Surveys | Create, manage, and process forms and surveys |
| Icons | Icon libraries and visual asset collections |
| Localization | Multi-language content and regional adaptations |
| Marketing | Marketing automation, email, social media, and campaigns |
| Scheduling | Calendar management, booking, and scheduling automation |
| SEO | Metadata management, sitemap generation, and SEO analysis |
| User Management | User accounts, authentication, permissions, and roles |
| Utilities | General purpose tools and utilities |

### Listing Best Practices

**Short description:**
- Focus on immediate value — state how your app solves a specific problem
- Use action-oriented language with strong verbs
- Highlight the primary use case

**Long description:**
- Start with a 2-3 sentence overview of purpose and benefits
- List key features and how they benefit users
- Include setup requirements and prerequisites
- Add real-world usage examples
- Link to documentation and support resources

**Visual presentation:**
- Showcase primary workflows in screenshots
- Highlight unique features
- Ensure text is readable in all screenshots
- Maintain consistent styling across screenshots

## Installation Configuration

Your app's installation URL defines where users are directed after choosing to install from the Marketplace.

### Data Client Apps

**Option 1 — Direct to Webflow OAuth (Recommended):**
Immediately initiates the OAuth flow on install.

```
https://webflow.com/oauth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&scope=YOUR_SCOPES
```

After authorization, redirect users to your platform to call the Get User Info endpoint and create/match accounts.

**Option 2 — Direct to your platform first:**
Users complete setup on your platform before initiating OAuth.

```
https://your-app.com/signup
```

> **Scopes:** Verify that scopes in the Install URL are equal to or a subset of scopes configured in app settings. Mismatched scopes will prevent installation.

### Hybrid Apps

**Option 1 — Direct to Webflow OAuth (Recommended):**
Same as Data Client, but after authorization users are redirected to the Designer with your app installed. Use the Get ID Token method and Resolve Token endpoint for authentication. See the Authenticating Hybrid Apps guide for details.

**Option 2 — Direct to your platform first:**
Same as Data Client — users authenticate with your service first, then initiate OAuth.

### Designer Extensions

No installation URL needed — Webflow handles the installation flow automatically. Users authorize the app to their site(s)/workspace.

### Installation Best Practices

- Test the full installation flow end-to-end
- For Hybrid Apps, consider directing users to the Designer via your app's deep link
- Minimize the number of steps users need to take
- Provide clear guidance at each step
- Handle error cases gracefully with helpful messages

## Post-Submission

Expect a decision within **10-15 business days** via the email associated with your Webflow account. Rejected apps receive an explanation with the opportunity to address feedback and resubmit.

> **Warning:** Attempts to exploit Webflow APIs or the review process (false information, plagiarism, data theft) will result in immediate removal and a ban from publishing.

For more context, see the [Developer Terms of Service](https://webflow.com/legal/developer-terms-of-service).

### Updating Your Listing

1. Go to the [App submission form](https://developers.webflow.com/submit)
2. Select "App Update" as Submission Type
3. Include your App Name or Client ID
4. Provide only the fields you want to update

App updates follow the same review process as initial submissions.
