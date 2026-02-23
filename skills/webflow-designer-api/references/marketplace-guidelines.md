---
name: "Marketplace Guidelines"
description: "Webflow Marketplace review guidelines covering safety, legal, performance, technical, design, usability, and business/branding requirements."
tags: [marketplace, guidelines, review, safety, legal, compliance, privacy, performance, technical, design, usability, accessibility, branding, monetization, submission, rejection, policy, security, data-protection, advertising]
---

# Marketplace Guidelines

Guidelines used by Webflow's review team to evaluate app submissions.

## Table of Contents

- [Safety / Legal](#safety--legal)
- [Performance / Technical](#performance--technical)
- [Design / Usability](#design--usability)
- [Business / Branding](#business--branding)

---

## Safety / Legal

1. **Malicious, Damaging, or Objectionable Content**
   - Apps that harm or compromise user security or their projects are not allowed
   - Offensive, insensitive, or disgusting content is prohibited
   - Apps must adhere to Webflow's [Acceptable Use Policy](https://webflow.com/legal/aup)

2. **Intellectual Property**
   - Only use content you have rights, licenses, or permissions for
   - Do not infringe trademarks, copyrights, or patents

3. **Compliance**
   - Comply with all applicable laws and regulations in jurisdictions where your app is available
   - Do not engage in or promote illegal activities

4. **Privacy and Data Protection**
   - Respect user privacy and handle personal data per relevant privacy laws
   - Provide clear information about data collection, storage, and use
   - Implement appropriate security measures to protect user data
   - Apps that misuse data will be removed

## Performance / Technical

**All Webflow Apps:**

1. **Performance**
   - Optimize for efficient resource usage and smooth user experience
   - Avoid long-running background processes that impact performance
   - Monitor and address performance issues regularly
   - Apps with persistent performance issues may be removed

2. **Technical**
   - Only use official Webflow APIs — do not require users to install packages that manipulate Webflow
   - Maintain well-organized source code following industry standards

**Additional requirements for Designer API apps:**

1. **Code Quality**
   - Use meaningful variable/function names, proper indentation, and appropriate comments
   - Do not use patterns that introduce vulnerabilities (e.g., `eval()`, direct DOM manipulation, excessive global variables)
   - Avoid externally hosted iframes for anything beyond authentication

## Design / Usability

**All Marketplace Apps:**

1. **Consistency** — Maintain consistent design and UI throughout the app
2. **Usability**
   - Provide comprehensive, user-friendly documentation (Webflow site recommended for hosting docs)
   - Deliver a fully functional experience free of placeholder content and test data
3. **Accessibility**
   - Design with accessibility in mind for users with disabilities
   - Follow [WCAG best practices](https://www.w3.org/WAI/standards-guidelines/wcag/) — alt text, keyboard navigation, sufficient color contrast
4. **User Feedback and Testing**
   - Gather feedback and conduct usability testing
   - Address reported issues promptly
   - Error-prone or unmaintained apps will be removed

**Additional requirements for Designer API apps:**

1. **Consistency**
   - Align visual style, typography, and color palette with Webflow's [App design guidelines](references/design-guidelines.md)
   - Maintain consistency with established Designer patterns (e.g., use component icons only for components, follow existing interaction patterns)
   - Avoid new UI patterns that conflict with Designer functionality
2. **Usability**
   - Design with intuitive navigation, clear labeling, and logical flow
   - Minimize user input requirements and strive for simplicity
   - Avoid intrusive or disruptive features
   - Do not use keyboard shortcuts to invoke your app or its functionality

## Business / Branding

1. **Monetization** — Be transparent about fees, subscriptions, and in-app purchases. No deceptive pricing.
2. **Advertising** — Do not display ads to users
3. **Branding**
   - No unauthorized use of others' trademarks, logos, or copyrighted materials
   - Disclose affiliations and partnerships truthfully
   - Impersonating a company will result in rejection
4. **One Developer Account Policy**
   - One developer account per developer for active marketplace listings
   - Using multiple accounts is prohibited and will result in enforcement actions
