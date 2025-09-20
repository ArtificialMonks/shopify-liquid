# Sections

Production-ready Shopify Liquid section templates with complete schema configurations. Organized into three categories for optimal project structure.

## 📁 Folder Structure

```
sections/
├── essential/     ✅ Phase 1 Complete - Core theme foundations
├── enhanced/      🚧 Phase 2 Coming - Advanced user experience
├── legacy/        📚 Reference - Previously created sections
└── README.md      📖 This documentation
```

## 🎯 Essential Sections (`/essential/`)

**Phase 1 Complete** - Core sections every professional Shopify theme requires for Theme Store compliance.

| Section | Description | Key Features |
|---------|-------------|--------------|
| `header.liquid` | Complete navigation system | Logo, menu, search, cart, mobile overlay, sticky header, dropdown menus |
| `footer.liquid` | Comprehensive footer with newsletter | Contact info, social links, newsletter signup, payment icons, back-to-top |
| `image-with-text.liquid` | Versatile content section | Flexible layouts, video overlay, block system, responsive design |
| `newsletter.liquid` | Marketing email signup | GDPR compliance, validation, social icons, success handling |
| `rich-text.liquid` | Flexible content foundation | Multiple block types, typography controls, custom HTML support |

**Quality Metrics:**
- ✅ 44 accessibility attributes (aria-*) across all sections
- ✅ Complete schema validation and Theme Store compliance
- ✅ Production-ready CSS scoping and performance optimization
- ✅ WCAG 2.1 AA accessibility standards

## 🚀 Enhanced Sections (`/enhanced/`)

**Phase 2 Planned** - Advanced sections for enhanced user experience and conversion optimization.

| Section | Description | Priority |
|---------|-------------|----------|
| `video.liquid` | Video content with controls | High - Media engagement |
| `feature-grid.liquid` | Feature/benefit showcase | High - Product highlights |
| `logo-list.liquid` | Brand/partner logos | Medium - Trust building |
| `contact-form.liquid` | Contact form with validation | Medium - Customer service |
| `announcement-bar.liquid` | Promotional banner | Low - Marketing campaigns |

## 📚 Legacy Sections (`/legacy/`)

Previously created sections preserved for reference and backward compatibility.

| Section | Description | Status |
|---------|-------------|--------|
| `hero-banner.liquid` | Simple hero banner | Reference |
| `hero-richtext-cta.liquid` | Feature-rich hero | Reference |
| `testimonial-carousel.liquid` | Customer testimonials | Reference |
| `faq-accordion.liquid` | Collapsible FAQ | Reference |
| `featured-products.liquid` | Product grid | Reference |

## Usage

Each section includes:
- Complete Liquid template with proper HTML structure
- JSON schema for theme customization
- CSS scoping using unique block IDs
- WCAG 2.1 AA accessibility compliance
- Responsive design patterns

## CSS Scoping Methodology

All sections use unique ID generation to prevent style collisions:

```liquid
{% assign unique = section.id | replace: '_', '' | downcase %}
```

Apply scoped styles:
```css
.section-name-{{ unique }} {
  /* Your styles here */
}
```

## Schema Patterns

Sections follow Shopify's schema conventions:
- Setting validation and proper types
- Block configurations for dynamic content
- Preset templates for quick setup
- Professional naming and descriptions

For implementation guidance, see [03-sections-and-schema.md](../../03-sections-and-schema.md).