# Shopify Liquid Templates Documentation

Templates define page-specific content structure and behavior in Shopify themes. This documentation covers all template types, JSON vs Liquid approaches, and modern development patterns for creating flexible, maintainable templates.

## 📁 What's in This Section

### Core Documentation
| File | Purpose | What You'll Learn |
|------|---------|-------------------|
| **[json-templates.md](./json-templates.md)** | JSON template architecture | Section-based composition, merchant flexibility |
| **[liquid-templates.md](./liquid-templates.md)** | Liquid template patterns | Static markup, custom logic, performance |
| **[metaobject-templates.md](./metaobject-templates.md)** | Custom content types | 2024 metaobject feature, dynamic content |

### Practical Resources
| Directory | Purpose | Contents |
|-----------|---------|----------|
| **[examples/](./examples/)** | Working templates | Complete template files, patterns, and variations |

## 🎯 Quick Start

### For Beginners
1. Start with **[json-templates.md](./json-templates.md)** to understand modern template architecture
2. Review **[examples/](./examples/)** for practical implementations
3. Learn **[liquid-templates.md](./liquid-templates.md)** for custom scenarios

### For Experienced Developers
- Jump to **[metaobject-templates.md](./metaobject-templates.md)** for cutting-edge features
- Browse **[examples/](./examples/)** for advanced patterns
- Reference specific files for implementation details

## 📋 Template Types Overview

### Required Templates
Every theme needs these core templates:
- **`index`** - Homepage (JSON recommended)
- **`404`** - Error page (Liquid often sufficient)
- **`search`** - Search results (JSON for flexibility)

### E-commerce Templates
Essential for online stores:
- **`product`** - Product details (JSON recommended)
- **`collection`** - Product listings (JSON recommended)
- **`cart`** - Shopping cart (JSON for customization)
- **`list-collections`** - Collection directory

### Content Templates
For blogs and pages:
- **`page`** - Static pages (JSON for flexibility)
- **`blog`** - Blog listing (JSON recommended)
- **`article`** - Blog posts (JSON for rich content)

### Customer Templates
Account management:
- **`customers/account`** - Customer dashboard
- **`customers/login`** - Login form
- **`customers/register`** - Registration
- **`customers/addresses`** - Address management
- **`customers/order`** - Order details

### Utility Templates
Special functions:
- **`gift_card`** - Gift card display
- **`password`** - Password-protected store
- **`robots.txt`** - SEO crawling rules

## 🚀 Template Architecture Patterns

### JSON Template Structure
```json
{
  "sections": {
    "main": {
      "type": "main-product",
      "settings": {
        "show_vendor": true,
        "show_sku": true
      }
    },
    "recommendations": {
      "type": "product-recommendations",
      "settings": {
        "heading": "You may also like"
      }
    }
  },
  "order": ["main", "recommendations"]
}
```

### Liquid Template Structure
```liquid
{% layout 'custom-layout' %}

<div class="product-page">
  <div class="product-media">
    {% for media in product.media %}
      <!-- Media rendering logic -->
    {% endfor %}
  </div>

  <div class="product-details">
    <h1>{{ product.title | escape }}</h1>
    <div class="price">{{ product.price | money }}</div>
    <!-- Custom product form -->
  </div>
</div>
```

### Alternative Templates
Create variations with suffix patterns:
- `product.quick-view.json` - Quick view modal
- `collection.grid.json` - Grid layout
- `page.landing.json` - Landing page variant

## 🎨 Template Selection Logic

### Template Resolution Order
1. **Alternative template** (if specified)
2. **Default template** for the resource type
3. **Fallback** to basic template

### Dynamic Template Assignment
```liquid
<!-- In admin or via URL parameter -->
?view=quick-view  <!-- Loads product.quick-view.json -->
```

### Conditional Template Logic
```liquid
<!-- Within templates -->
{% if template.suffix == 'quick-view' %}
  <!-- Quick view specific content -->
{% endif %}
```

## 📊 Template Best Practices

### 1. Choose the Right Type
- **JSON Templates**: When merchants need customization flexibility
- **Liquid Templates**: For static layouts or complex custom logic
- **Metaobject Templates**: For custom content types and data structures

### 2. Performance Optimization
- **Lazy load** below-the-fold content
- **Paginate** large collections (`{% paginate %}`)
- **Optimize images** with appropriate sizing
- **Minimize loops** over large datasets

### 3. SEO Implementation
- **Structured data** for rich snippets
- **Meta tags** for social sharing
- **Canonical URLs** for duplicate content
- **Hreflang** for multi-language sites

### 4. Accessibility Standards
- **Semantic HTML** structure
- **ARIA labels** for dynamic content
- **Focus management** for interactive elements
- **Screen reader** compatible navigation

## 🔧 Advanced Patterns

### Template Inheritance Simulation
```liquid
<!-- base-product.liquid -->
{% include 'product-breadcrumbs' %}
{% include 'product-media' %}
{% include 'product-form' %}
{% include 'product-details' %}

<!-- product.featured.liquid -->
{% layout 'full-width' %}
{% include 'featured-badge' %}
{% include 'base-product' %}
{% include 'social-sharing' %}
```

### Dynamic Section Loading
```liquid
<!-- Load sections based on product type -->
{% case product.type %}
  {% when 'clothing' %}
    {% section 'size-guide' %}
  {% when 'electronics' %}
    {% section 'tech-specs' %}
{% endcase %}
```

### Template Context Handling
```liquid
<!-- Access template information -->
<body class="template-{{ template.name }}
           {% if template.suffix %}template-{{ template.name }}-{{ template.suffix }}{% endif %}
           {% if collection %}collection-{{ collection.handle }}{% endif %}
           {% if product %}product-{{ product.type | handle }}{% endif %}">
```

## 🛟 Common Challenges

### Template vs Section Balance
**Challenge**: When to use template logic vs section settings
**Solution**: Use sections for merchant-customizable content, templates for fixed structure

### Performance with Large Collections
**Challenge**: Slow loading with many products
**Solution**: Implement pagination and lazy loading patterns

### SEO for Dynamic Content
**Challenge**: Proper meta tags for filtered/sorted content
**Solution**: Dynamic meta tag generation based on current state

### Mobile Optimization
**Challenge**: Complex layouts on small screens
**Solution**: Mobile-first responsive design with progressive enhancement

## 📚 Related Documentation

- **[Sections Guide](../../README.md)** - How templates work with sections
- **[Layouts Guide](../layouts/)** - Template foundation structure
- **[Architecture Overview](../architecture/theme-overview.md)** - Complete theme structure
- **[Best Practices](../architecture/best-practices-2025.md)** - 2025 development standards

---

This documentation provides comprehensive guidance for creating all types of Shopify templates, from basic pages to complex e-commerce experiences with modern Online Store 2.0 features.