# Shopify Theme File Taxonomy

A comprehensive reference for all Shopify theme file types, their purposes, relationships, and best practices for organization and implementation.

## 📁 Complete File Type Taxonomy

### 1. Layout Files (`layout/`)

#### Purpose
Define the base HTML structure and global elements for all pages.

#### Required Files
- **`theme.liquid`** *(required)*: Default layout for all pages
- **`checkout.liquid`** *(Shopify Plus only)*: Checkout process layout

#### File Characteristics
- **Extension**: `.liquid`
- **Scope**: Global (affects all pages)
- **Count**: Typically 1-3 files
- **Required Objects**: `{{ content_for_header }}`, `{{ content_for_layout }}`

#### Usage Patterns
```liquid
<!DOCTYPE html>
<html lang="{{ shop.locale }}">
<head>
  {{ content_for_header }}
</head>
<body>
  {% sections 'header-group' %}
  {{ content_for_layout }}
  {% sections 'footer-group' %}
</body>
</html>
```

---

### 2. Template Files (`templates/`)

#### Purpose
Define page-specific content structure and behavior.

#### File Types
- **JSON Templates** (`.json`): Section-based, merchant-editable
- **Liquid Templates** (`.liquid`): Static markup with Liquid logic

#### Template Categories
| Category | Templates | Purpose |
|----------|-----------|---------|
| **Core Pages** | `index`, `404`, `search` | Essential site pages |
| **Product/Collection** | `product`, `collection`, `list-collections` | E-commerce pages |
| **Content** | `page`, `blog`, `article` | Content management |
| **Customer** | `customers/*` | Account management |
| **Utility** | `cart`, `gift_card`, `password` | Special functions |
| **Dynamic** | `metaobject/*` | Custom content types |

#### Alternative Templates
Use suffix pattern for variations:
- `product.special.liquid` - Alternative product template
- `page.landing.json` - Landing page variant
- `collection.featured.json` - Featured collection layout

---

### 3. Section Files (`sections/`)

#### Purpose
Modular, reusable content components with merchant customization.

#### File Types
- **Section Files** (`.liquid`): Component markup and logic
- **Section Groups** (`.json`): Collections of sections for layouts

#### Section Categories
| Type | Examples | Use Cases |
|------|----------|-----------|
| **Layout** | `header`, `footer` | Global components |
| **Content** | `hero-banner`, `text-block` | Content areas |
| **Product** | `product-grid`, `featured-product` | E-commerce displays |
| **Media** | `image-gallery`, `video` | Media showcases |
| **Interactive** | `newsletter`, `contact-form` | User engagement |

#### Section Structure
```liquid
<!-- Section markup -->
<div class="section-{{ section.id }}">
  {% for block in section.blocks %}
    <!-- Block rendering -->
  {% endfor %}
</div>

{% schema %}
{
  "name": "Section Name",
  "settings": [...],
  "blocks": [...],
  "presets": [...]
}
{% endschema %}
```

---

### 4. Block Files (`blocks/`)

#### Purpose
Standalone, reusable components that can be used across multiple sections.

#### Block Types
- **Theme Blocks**: Standalone files with their own schemas
- **Section Blocks**: Defined within section schemas
- **App Blocks**: Third-party application components

#### Block Characteristics
- **Extension**: `.liquid`
- **Scope**: Reusable across sections
- **Schema**: Self-contained with `{% schema %}` tag
- **Nesting**: Can contain other blocks

#### Example Structure
```liquid
{% assign unique = block.id | replace: '_', '' | downcase %}

{% style %}
  .block-{{ unique }} { /* scoped styles */ }
{% endstyle %}

<div class="block-{{ unique }}" {{ block.shopify_attributes }}>
  <!-- Block content -->
</div>

{% schema %}
{
  "name": "Block Name",
  "settings": [...],
  "presets": [...]
}
{% endschema %}
```

---

### 5. Asset Files (`assets/`)

#### Purpose
Static resources including styles, scripts, images, and media.

#### Asset Categories
| Category | Extensions | Purpose |
|----------|------------|---------|
| **Stylesheets** | `.css`, `.css.liquid` | Styling and layout |
| **Scripts** | `.js`, `.js.liquid` | Interactivity and behavior |
| **Images** | `.jpg`, `.png`, `.webp`, `.svg` | Visual content |
| **Fonts** | `.woff`, `.woff2`, `.ttf` | Typography |
| **Media** | `.mp4`, `.mov`, `.gif` | Video and animations |
| **Icons** | `.svg`, `.ico` | Interface elements |

#### Asset Organization Patterns
```
assets/
├── styles/
│   ├── theme.css.liquid          # Main stylesheet
│   ├── components/               # Component styles
│   └── utilities/                # Utility classes
├── scripts/
│   ├── theme.js                  # Main JavaScript
│   ├── modules/                  # Feature modules
│   └── vendor/                   # Third-party libraries
├── images/
│   ├── icons/                    # SVG icons
│   ├── backgrounds/              # Background images
│   └── placeholders/             # Default images
└── fonts/                        # Web fonts
```

---

### 6. Configuration Files (`config/`)

#### Purpose
Theme settings, data, and configuration management.

#### Configuration Files
| File | Purpose | Format |
|------|---------|--------|
| **`settings_schema.json`** | Theme settings definition | JSON |
| **`settings_data.json`** | Current settings values | JSON |
| **`markets.json`** | Market-specific customizations | JSON |

#### Settings Architecture
- **Theme Settings**: Global theme configuration
- **Section Settings**: Component-specific options
- **Block Settings**: Individual element customization

#### Example Schema Structure
```json
[
  {
    "name": "Colors",
    "settings": [
      {
        "type": "color",
        "id": "color_primary",
        "label": "Primary color",
        "default": "#000000"
      }
    ]
  }
]
```

---

### 7. Locale Files (`locales/`)

#### Purpose
Internationalization and translation management.

#### Locale File Types
| Type | Extension | Purpose |
|------|-----------|---------|
| **Storefront** | `.json` | Customer-facing translations |
| **Schema** | `.schema.json` | Theme editor translations |
| **Default** | `.default.json` | Fallback language |

#### Translation Structure
```json
{
  "general": {
    "search": {
      "title": "Search",
      "placeholder": "Search products..."
    }
  },
  "products": {
    "product": {
      "add_to_cart": "Add to cart",
      "sold_out": "Sold out"
    }
  }
}
```

---

### 8. Snippet Files (`snippets/`)

#### Purpose
Reusable code fragments and utility functions.

#### Snippet Categories
| Category | Examples | Purpose |
|----------|----------|---------|
| **Components** | `product-card`, `breadcrumbs` | Reusable UI elements |
| **Utilities** | `responsive-image`, `price-formatter` | Helper functions |
| **Forms** | `contact-form`, `newsletter-form` | Form components |
| **Media** | `video-player`, `image-gallery` | Media handlers |

#### Usage Pattern
```liquid
<!-- Include snippet -->
{% include 'product-card', product: product %}

<!-- Or render snippet (isolated scope) -->
{% render 'product-card', product: product %}
```

---

## 🔗 File Relationships

### Dependency Hierarchy
```
Layout (foundation)
├── Templates (page structure)
│   ├── Sections (components)
│   │   ├── Blocks (elements)
│   │   └── Snippets (utilities)
│   ├── Assets (resources)
│   └── Config (settings)
└── Locales (translations)
```

### Data Flow
1. **Request** → Layout loads
2. **Template** → Determines page structure
3. **Sections** → Render based on template
4. **Blocks** → Fill section content areas
5. **Assets** → Provide styling and behavior
6. **Config** → Supply setting values
7. **Locales** → Provide translated content

### Setting Inheritance
```
Theme Settings (global)
└── Section Settings (component)
    └── Block Settings (element)
```

---

## 📋 File Naming Conventions

### General Rules
- Use lowercase letters
- Separate words with hyphens
- Be descriptive and consistent
- Follow Shopify conventions

### Specific Patterns
| File Type | Pattern | Example |
|-----------|---------|---------|
| **Sections** | `noun` or `noun-descriptor` | `hero-banner`, `product-grid` |
| **Blocks** | `block-descriptor` | `block-testimonial`, `block-feature` |
| **Snippets** | `function-descriptor` | `responsive-image`, `price-display` |
| **Assets** | `category-descriptor` | `theme.css`, `product-zoom.js` |
| **Templates** | `type.variant` | `product.featured`, `page.landing` |

---

## 🎯 Best Practices Summary

### File Organization
1. **Logical grouping**: Organize by function and purpose
2. **Consistent naming**: Follow established conventions
3. **Modular structure**: Keep files focused and reusable
4. **Clear hierarchy**: Maintain obvious relationships

### Development Workflow
1. **Start with layout**: Establish base structure
2. **Build templates**: Define page types
3. **Create sections**: Develop modular components
4. **Add blocks**: Build reusable elements
5. **Style with assets**: Implement visual design
6. **Configure settings**: Enable customization
7. **Add translations**: Support internationalization

### Maintenance Strategy
1. **Version control**: Track all file changes
2. **Documentation**: Document custom implementations
3. **Testing**: Validate across file types
4. **Performance**: Monitor file impact
5. **Updates**: Keep files current with Shopify changes

This taxonomy provides the complete reference for understanding and organizing all Shopify theme file types effectively.