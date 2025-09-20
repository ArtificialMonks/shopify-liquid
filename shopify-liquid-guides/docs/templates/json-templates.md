# JSON Templates - Section-Based Architecture

JSON templates represent the modern approach to Shopify theme development, enabling merchant customization through section-based composition. They provide maximum flexibility while maintaining clean separation between content and presentation.

## 🎯 What are JSON Templates?

### Core Concept
JSON templates are **configuration files** that:
- **Reference sections** instead of containing markup
- **Enable merchant editing** through the theme editor
- **Support drag-and-drop** section management
- **Separate content from code** for maintainability

### Benefits Over Liquid Templates
✅ **Merchant flexibility** - Add/remove/reorder sections
✅ **Future-proof** - Easier updates and maintenance
✅ **Performance** - Optimized section rendering
✅ **Consistency** - Standardized section patterns

## 🏗️ JSON Template Structure

### Basic Structure
```json
{
  "sections": {
    "section_id": {
      "type": "section-filename",
      "settings": {
        "setting_key": "value"
      }
    }
  },
  "order": ["section_id"]
}
```

### Complete Example
```json
{
  "sections": {
    "main": {
      "type": "main-product",
      "settings": {
        "show_vendor": true,
        "show_sku": true,
        "enable_video_looping": false
      },
      "blocks": {
        "block_1": {
          "type": "text",
          "settings": {
            "text": "Free shipping on orders over $50"
          }
        },
        "block_2": {
          "type": "buy_buttons",
          "settings": {
            "show_dynamic_checkout": true
          }
        }
      },
      "block_order": ["block_1", "block_2"]
    },
    "recommendations": {
      "type": "product-recommendations",
      "settings": {
        "heading": "You may also like",
        "products_to_show": 4,
        "image_ratio": "square"
      }
    },
    "recently_viewed": {
      "type": "recently-viewed-products",
      "settings": {
        "heading": "Recently viewed"
      }
    }
  },
  "order": ["main", "recommendations", "recently_viewed"]
}
```

## 🔧 Template Components

### Sections Object
Defines all sections used in the template:

```json
{
  "sections": {
    "unique-section-id": {
      "type": "section-filename",
      "settings": {},
      "blocks": {},
      "block_order": []
    }
  }
}
```

#### Section Properties
- **`type`**: References the section filename (without .liquid)
- **`settings`**: Override section default settings
- **`blocks`**: Define blocks within the section
- **`block_order`**: Specify block rendering order

### Order Array
Controls section rendering sequence:

```json
{
  "order": [
    "header-content",
    "main-content",
    "related-content",
    "footer-content"
  ]
}
```

### Settings Override
Customize section behavior:

```json
{
  "sections": {
    "hero": {
      "type": "hero-banner",
      "settings": {
        "heading": "Welcome to our store",
        "button_text": "Shop now",
        "background_color": "#f8f8f8",
        "text_alignment": "center",
        "show_overlay": true
      }
    }
  }
}
```

## 🎨 Advanced Patterns

### Dynamic Section Loading
```json
{
  "sections": {
    "main": {
      "type": "main-collection",
      "settings": {
        "products_per_page": 24,
        "enable_filtering": true,
        "enable_sorting": true
      }
    },
    "filters": {
      "type": "collection-filters",
      "settings": {
        "filter_type": "horizontal",
        "show_product_count": true
      }
    },
    "promotion": {
      "type": "promotional-banner",
      "settings": {
        "show_on_collection": "featured",
        "banner_text": "Free shipping this week!"
      }
    }
  },
  "order": ["filters", "promotion", "main"]
}
```

### Conditional Section Display
Use section settings to control visibility:

```json
{
  "sections": {
    "seasonal_banner": {
      "type": "announcement-bar",
      "settings": {
        "text": "Holiday Sale - 20% off everything!",
        "show_banner": true,
        "start_date": "2024-12-01",
        "end_date": "2024-12-31"
      }
    }
  }
}
```

### Block Configuration
Define complex block structures:

```json
{
  "sections": {
    "featured_products": {
      "type": "featured-collection",
      "blocks": {
        "product_1": {
          "type": "featured_product",
          "settings": {
            "product": "{{products.featured-item-1}}",
            "show_quick_add": true,
            "image_ratio": "square"
          }
        },
        "product_2": {
          "type": "featured_product",
          "settings": {
            "product": "{{products.featured-item-2}}",
            "show_quick_add": true,
            "image_ratio": "square"
          }
        },
        "text_block": {
          "type": "text",
          "settings": {
            "heading": "Why choose us?",
            "text": "<p>Quality products, fast shipping, great support.</p>"
          }
        }
      },
      "block_order": ["product_1", "text_block", "product_2"]
    }
  }
}
```

## 📱 Template-Specific Patterns

### Product Templates
```json
{
  "sections": {
    "main": {
      "type": "main-product",
      "blocks": {
        "vendor": { "type": "text", "settings": { "text": "{{ product.vendor }}" }},
        "title": { "type": "title" },
        "price": { "type": "price" },
        "variant_picker": { "type": "variant_picker" },
        "quantity_selector": { "type": "quantity_selector" },
        "buy_buttons": { "type": "buy_buttons" },
        "description": { "type": "description" },
        "share": { "type": "share" }
      },
      "block_order": ["vendor", "title", "price", "variant_picker", "quantity_selector", "buy_buttons", "description", "share"]
    },
    "product_recommendations": {
      "type": "product-recommendations",
      "settings": {
        "heading": "You may also like",
        "products_to_show": 4
      }
    }
  },
  "order": ["main", "product_recommendations"]
}
```

### Collection Templates
```json
{
  "sections": {
    "banner": {
      "type": "collection-banner",
      "settings": {
        "show_collection_description": true,
        "show_collection_image": true
      }
    },
    "product_grid": {
      "type": "main-collection-product-grid",
      "settings": {
        "products_per_page": 24,
        "columns_desktop": 4,
        "image_ratio": "adapt",
        "enable_quick_add": true,
        "enable_filtering": true,
        "filter_type": "horizontal",
        "enable_sorting": true
      }
    }
  },
  "order": ["banner", "product_grid"]
}
```

### Homepage Templates
```json
{
  "sections": {
    "hero": {
      "type": "image-banner",
      "blocks": {
        "heading": {
          "type": "heading",
          "settings": {
            "heading": "Welcome to our store",
            "heading_size": "h1"
          }
        },
        "text": {
          "type": "text",
          "settings": {
            "text": "Discover amazing products"
          }
        },
        "button": {
          "type": "buttons",
          "settings": {
            "button_label_1": "Shop now",
            "button_link_1": "shopify://collections/all"
          }
        }
      },
      "block_order": ["heading", "text", "button"]
    },
    "featured_collection": {
      "type": "featured-collection",
      "settings": {
        "title": "Featured products",
        "collection": "{{collections.featured}}",
        "products_to_show": 8,
        "columns_desktop": 4
      }
    },
    "testimonials": {
      "type": "multicolumn",
      "blocks": {
        "testimonial_1": {
          "type": "column",
          "settings": {
            "title": "Amazing quality",
            "text": "I love the products from this store!",
            "link_label": "View all reviews"
          }
        }
      },
      "block_order": ["testimonial_1"]
    }
  },
  "order": ["hero", "featured_collection", "testimonials"]
}
```

## 🚀 Performance Optimization

### Lazy Loading Sections
```json
{
  "sections": {
    "above_fold": {
      "type": "hero-banner",
      "settings": {
        "loading_priority": "high"
      }
    },
    "below_fold": {
      "type": "testimonials",
      "settings": {
        "loading_priority": "low",
        "lazy_load": true
      }
    }
  }
}
```

### Conditional Section Loading
```json
{
  "sections": {
    "mobile_banner": {
      "type": "image-banner",
      "settings": {
        "mobile_only": true,
        "image_mobile": "banner-mobile.jpg"
      }
    },
    "desktop_banner": {
      "type": "image-banner",
      "settings": {
        "desktop_only": true,
        "image_desktop": "banner-desktop.jpg"
      }
    }
  }
}
```

## 🔄 Template Inheritance Patterns

### Base Template Structure
Create reusable section combinations:

```json
// templates/product.json (base)
{
  "sections": {
    "main": {
      "type": "main-product"
    },
    "recommendations": {
      "type": "product-recommendations"
    }
  },
  "order": ["main", "recommendations"]
}

// templates/product.bundle.json (extended)
{
  "sections": {
    "main": {
      "type": "main-product"
    },
    "bundle_offer": {
      "type": "product-bundle",
      "settings": {
        "discount_percentage": 15
      }
    },
    "recommendations": {
      "type": "product-recommendations"
    }
  },
  "order": ["main", "bundle_offer", "recommendations"]
}
```

## 🛠️ Development Workflow

### 1. Section-First Approach
- Design sections independently
- Build section schema carefully
- Test section combinations
- Create template compositions

### 2. Template Testing
- Verify all section references exist
- Test with different content types
- Validate JSON syntax
- Check responsive behavior

### 3. Merchant Experience
- Test theme editor functionality
- Verify drag-and-drop works
- Check setting interactions
- Validate preset behavior

## 🚨 Common Pitfalls

### 1. Missing Section Files
**Problem**: Template references non-existent section
```json
{
  "sections": {
    "main": {
      "type": "non-existent-section"  // ❌ Section doesn't exist
    }
  }
}
```

**Solution**: Verify section files exist in `/sections` directory

### 2. Invalid JSON Syntax
**Problem**: Malformed JSON breaks template
```json
{
  "sections": {
    "main": {
      "type": "main-product",
      "settings": {
        "show_vendor": true,  // ❌ Trailing comma
      }
    }
  }
}
```

**Solution**: Use JSON validator and proper syntax

### 3. Section ID Conflicts
**Problem**: Duplicate section IDs cause issues
```json
{
  "sections": {
    "main": { "type": "hero-banner" },
    "main": { "type": "featured-products" }  // ❌ Duplicate ID
  }
}
```

**Solution**: Use unique, descriptive section IDs

### 4. Block Order Mismatches
**Problem**: Block order references non-existent blocks
```json
{
  "blocks": {
    "block_1": { "type": "text" }
  },
  "block_order": ["block_1", "block_2"]  // ❌ block_2 doesn't exist
}
```

**Solution**: Ensure block_order matches defined blocks

## 📊 Best Practices

### 1. Naming Conventions
- **Section IDs**: Descriptive and unique (`hero_banner`, `featured_products`)
- **Block IDs**: Sequential or descriptive (`block_1`, `testimonial_john`)
- **Settings**: Match section schema keys exactly

### 2. Organization Patterns
- **Logical ordering**: Header → Main → Supporting → Footer
- **Related grouping**: Keep related sections together
- **Performance priority**: Critical sections first

### 3. Maintenance Strategies
- **Documentation**: Comment complex configurations
- **Version control**: Track template changes
- **Testing**: Validate changes across devices
- **Backup**: Maintain template backups

---

JSON templates provide the foundation for flexible, maintainable Shopify themes that empower merchants while maintaining developer control over functionality and performance.