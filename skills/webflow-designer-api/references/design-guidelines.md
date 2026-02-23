---
name: "Design Guidelines"
description: "UI/UX guidelines for building native-feeling Webflow Designer Extensions including layout, typography, colors, and CSS variables."
tags: [design, ui, ux, guidelines, css-variables, typography, colors, layout, spacing, dark-mode, light-mode, Inter, font, border-radius, box-shadow, background, text-color, border, action-primary, action-secondary, semantic-colors, figma, accessibility, design-principles, webflow-variables]
---

# Design Guidelines Reference

Build extensions that feel native to Webflow's Designer.

## Table of Contents

- [Design Principles](#design-principles)
- [Layout Guidelines](#layout-guidelines)
- [Typography](#typography)
- [Border Radius](#border-radius)
- [Color System](#color-system)
- [Box Shadows](#box-shadows)
- [Usage in CSS](#usage-in-css)
- [Resources](#resources)

---

## Design Principles

1. **Customer-focused**: Solve real problems for Webflow users
2. **Simple & approachable**: Minimize learning curve
3. **Consistent**: Match Webflow's design language
4. **Foster creative flow**: Don't interrupt user momentum
5. **Clear language**: Concise, actionable copy
6. **Accessible**: Follow accessibility standards

## Layout Guidelines

1. **Vertical stacking**: Arrange components vertically in narrow panel
2. **Full-width elements**: Buttons and inputs span full width
3. **No horizontal scroll**: Fit content within iframe width
4. **Consistent spacing**: Use 4px rhythm (4, 8, 12, 16, 20, 24, 32px)
5. **Sentence case**: All text including headings and buttons

## Typography

**Font**: Inter (Google Fonts or bundled)

```css
--font-stack: 'Inter', sans-serif;
--font-size-small: 11.5px;
--font-size-small-letter-spacing: -0.115px;
--font-size-large: 12.5px;
--font-weight-normal: 400;
--font-weight-medium: 600;
```

## Border Radius

```css
--border-radius: 4px;
```

## Color System

Colors auto-adjust based on user's Appearance settings (dark/light mode).

### Backgrounds
```css
--background1: #1E1E1E;
--background2: #2E2E2E;
--background3: #383838;
--background4: #373737;
--background5: #444444;
--backgroundInactive: #2E2E2E;
--backgroundInverse: #EBEBEB;
--backgroundInput: rgba(0, 0, 0, 0.15);
```

### Text
```css
--text1: #F5F5F5;
--text2: #BDBDBD;
--text3: #A3A3A3;
--textInactive: #757575;
--textInverse: #1E1E1E;
```

### Borders
```css
--border1: rgba(255, 255, 255, 0.13);
--border2: rgba(255, 255, 255, 0.14);
--border3: rgba(255, 255, 255, 0.19);
```

### Primary Actions
```css
--actionPrimaryBackground: #006ACC;
--actionPrimaryBackgroundHover: #187CD9;
--actionPrimaryText: #FFFFFF;
--actionPrimaryTextHover: #FFFFFF;
```

### Secondary Actions
```css
--actionSecondaryBackground: linear-gradient(180deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.10) 100%);
--actionSecondaryBackgroundHover: linear-gradient(180deg, rgba(255, 255, 255, 0.18) 0%, rgba(255, 255, 255, 0.16) 100%);
--actionSecondaryText: #E0E0E0;
--actionSecondaryTextHover: #E0E0E0;
```

### Semantic Colors

**Blue (Info)**
```css
--blueText: #8AC2FF;
--blueIcon: #8AC2FF;
--blueBorder: #007DF0;
```

**Green (Success)**
```css
--greenBackground: #007A41;
--greenBackgroundHover: #0D8A4F;
--greenText: #63D489;
--greenIcon: #63D489;
--greenBorder: #259D4D;
```

**Yellow (Warning)**
```css
--yellowBackground: #946B00;
--yellowBackgroundHover: #AF7F00;
--yellowText: #F3C831;
--yellowIcon: #F3C831;
--yellowBorder: #D7A220;
```

**Red (Error)**
```css
--redBackground: #CF313B;
--redBackgroundHover: #CB3535;
--redText: #FF8A8A;
--redIcon: #FF8A8A;
--redBorder: #E42F3A;
```

**Orange**
```css
--orangeBackground: #BF4704;
--orangeBackgroundHover: #DC95616;
--orangeText: #EBA267;
--orangeIcon: #EBA267;
--orangeBorder: #DF640C;
```

**Purple**
```css
--purpleBackground: #734CE0;
--purpleBackgroundHover: #815BEB;
--purpleText: #B89EFF;
--purpleIcon: #B89EFF;
--purpleBorder: #875FFD;
```

## Box Shadows

```css
/* Buttons (colored) */
--boxShadows-action-colored: 0px 0.5px 1px 0px rgba(0, 0, 0, 0.8),
  0px 0.5px 0.5px 0px rgba(255, 255, 255, 0.20) inset;

/* Buttons (secondary) */
--boxShadows-action-secondary: 0px 0.5px 1px rgba(0, 0, 0, 0.8),
  inset 0px 0.5px 0.5px rgba(255, 255, 255, 0.12);

/* Inputs */
--boxShadows-input-inner: 0px 1px 1px -1px rgba(0, 0, 0, 0.13) inset,
  0px 3px 3px -3px rgba(0, 0, 0, 0.17) inset,
  0px 4px 4px -4px rgba(0, 0, 0, 0.17) inset,
  0px 8px 8px -8px rgba(0, 0, 0, 0.17) inset,
  0px 12px 12px -12px rgba(0, 0, 0, 0.13) inset,
  0px 16px 16px -16px rgba(0, 0, 0, 0.13) inset;

/* Menus/Dropdowns */
--boxShadows-menu: 0px 0.5px 0.5px 0px rgba(255, 255, 255, 0.12) inset,
  0px 12px 24px 8px rgba(0, 0, 0, 0.04),
  0px 8px 16px 4px rgba(0, 0, 0, 0.04),
  0px 4px 8px 2px rgba(0, 0, 0, 0.04),
  0px 2px 6px 0px rgba(0, 0, 0, 0.04),
  0px 0px 1px 0px rgba(0, 0, 0, 0.25);
```

## Usage in CSS

```css
.my-button {
  background: var(--actionPrimaryBackground);
  color: var(--actionPrimaryText);
  font-family: var(--font-stack);
  font-size: var(--font-size-large);
  border-radius: var(--border-radius);
  box-shadow: var(--boxShadows-action-colored);
  border: none;
  padding: 8px 16px;
  cursor: pointer;
}

.my-button:hover {
  background: var(--actionPrimaryBackgroundHover);
}

.my-input {
  background: var(--backgroundInput);
  color: var(--text1);
  border: 1px solid var(--border2);
  border-radius: var(--border-radius);
  box-shadow: var(--boxShadows-input-inner);
  padding: 8px 12px;
}

.my-panel {
  background: var(--background2);
  border: 1px solid var(--border1);
}
```

## Resources

- [Webflow Apps Figma UI Kit](https://www.figma.com/community/file/1291823507081366246/webflow-app-ui-kit-2-0)
- [Inter Font on Google Fonts](https://fonts.google.com/specimen/Inter)
