# Section Groups - Layout Area Configuration

Section groups define configurable layout areas like headers, footers, and sidebars that merchants can customize through the theme editor. This guide covers section group implementation, configuration patterns, and best practices for flexible layout management.

## 🎯 Section Groups Overview

### Purpose and Function
Section groups enable:
- **Flexible layout areas** - Header, footer, aside sections
- **Merchant customization** - Add, remove, reorder sections
- **Contextual configuration** - Different layouts per template
- **Theme editor integration** - Visual section management

### Available Group Types
- **`header`** - Top navigation and announcement areas
- **`footer`** - Bottom content and links
- **`aside`** - Sidebar content and filters

## 🏗️ Section Group Structure

### Basic Group Configuration
```json
{
  "name": "Header",
  "type": "header",
  "sections": {
    "announcement": {
      "type": "announcement-bar",
      "settings": {
        "text": "Free shipping on orders over $50",
        "background_color": "#000000",
        "text_color": "#ffffff"
      }
    },
    "header": {
      "type": "header",
      "settings": {
        "logo_width": 150,
        "menu": "main-menu",
        "enable_sticky": true
      }
    }
  },
  "order": ["announcement", "header"]
}
```

### Footer Group Configuration
```json
{
  "name": "Footer",
  "type": "footer",
  "sections": {
    "footer-links": {
      "type": "footer-links",
      "blocks": {
        "link-list-1": {
          "type": "link_list",
          "settings": {
            "heading": "Shop",
            "menu": "footer-shop"
          }
        },
        "link-list-2": {
          "type": "link_list",
          "settings": {
            "heading": "Support",
            "menu": "footer-support"
          }
        }
      },
      "block_order": ["link-list-1", "link-list-2"]
    },
    "footer-bottom": {
      "type": "footer-bottom",
      "settings": {
        "show_payment_icons": true,
        "show_social_icons": true,
        "copyright_text": "© 2024 Your Store Name"
      }
    }
  },
  "order": ["footer-links", "footer-bottom"]
}
```

## 🚀 Header Group Patterns

### Multi-Section Header
```json
{
  "name": "Header",
  "type": "header",
  "sections": {
    "announcement-bar": {
      "type": "announcement-bar",
      "settings": {
        "text": "Free shipping on orders over $50",
        "link": "/collections/all",
        "background_color": "#000000",
        "text_color": "#ffffff",
        "show_close": true
      }
    },
    "header-main": {
      "type": "header",
      "settings": {
        "logo_width": 150,
        "logo_position": "left",
        "menu": "main-menu",
        "enable_search": true,
        "search_placeholder": "Search products...",
        "enable_sticky": true,
        "sticky_background": "#ffffff"
      }
    },
    "header-promotion": {
      "type": "promotional-banner",
      "settings": {
        "text": "New collection now available",
        "link": "/collections/new",
        "background_color": "#f8f8f8",
        "show_on_homepage_only": false
      }
    }
  },
  "order": ["announcement-bar", "header-main", "header-promotion"]
}
```

### Responsive Header Configuration
```json
{
  "sections": {
    "header": {
      "type": "header",
      "settings": {
        "logo_width_desktop": 200,
        "logo_width_mobile": 120,
        "menu_style_desktop": "horizontal",
        "menu_style_mobile": "drawer",
        "show_search_desktop": true,
        "show_search_mobile": false,
        "enable_sticky_desktop": true,
        "enable_sticky_mobile": false
      }
    }
  }
}
```

## 🎨 Footer Group Patterns

### Comprehensive Footer
```json
{
  "name": "Footer",
  "type": "footer",
  "sections": {
    "footer-newsletter": {
      "type": "newsletter-signup",
      "settings": {
        "heading": "Stay in the loop",
        "subheading": "Get exclusive offers and news",
        "background_color": "#f8f8f8",
        "show_social_icons": true
      }
    },
    "footer-content": {
      "type": "footer-content",
      "blocks": {
        "footer-menu-1": {
          "type": "link_list",
          "settings": {
            "heading": "Shop",
            "menu": "footer-shop",
            "show_heading": true
          }
        },
        "footer-menu-2": {
          "type": "link_list",
          "settings": {
            "heading": "Customer Care",
            "menu": "footer-support",
            "show_heading": true
          }
        },
        "footer-contact": {
          "type": "contact_info",
          "settings": {
            "heading": "Contact Us",
            "address": "123 Store Street, City, State 12345",
            "phone": "+1 (555) 123-4567",
            "email": "hello@yourstore.com",
            "show_map_link": true
          }
        },
        "footer-social": {
          "type": "social_media",
          "settings": {
            "heading": "Follow Us",
            "show_facebook": true,
            "show_instagram": true,
            "show_twitter": true
          }
        }
      },
      "block_order": ["footer-menu-1", "footer-menu-2", "footer-contact", "footer-social"]
    },
    "footer-bottom": {
      "type": "footer-bottom",
      "settings": {
        "show_payment_icons": true,
        "payment_icon_style": "outline",
        "show_country_selector": true,
        "show_language_selector": false,
        "copyright_text": "© {{ 'now' | date: '%Y' }} {{ shop.name }}. All rights reserved."
      }
    }
  },
  "order": ["footer-newsletter", "footer-content", "footer-bottom"]
}
```

### Minimal Footer
```json
{
  "name": "Footer",
  "type": "footer",
  "sections": {
    "footer-simple": {
      "type": "footer-simple",
      "settings": {
        "show_social_icons": true,
        "social_icon_size": "medium",
        "show_payment_icons": true,
        "payment_icon_color": "dark",
        "copyright_text": "© {{ 'now' | date: '%Y' }} {{ shop.name }}",
        "background_color": "#ffffff",
        "text_color": "#000000"
      }
    }
  },
  "order": ["footer-simple"]
}
```

## 🔧 Aside Group Patterns

### Sidebar Configuration
```json
{
  "name": "Sidebar",
  "type": "aside",
  "sections": {
    "collection-filters": {
      "type": "collection-filters",
      "settings": {
        "filter_style": "sidebar",
        "show_filter_count": true,
        "enable_color_swatches": true,
        "enable_price_range": true,
        "show_clear_filters": true
      }
    },
    "featured-products": {
      "type": "featured-products-sidebar",
      "settings": {
        "heading": "You might also like",
        "collection": "featured-products",
        "products_to_show": 3,
        "show_price": true,
        "show_vendor": false
      }
    },
    "promotional-content": {
      "type": "promotional-banner",
      "settings": {
        "image": "sidebar-promo.jpg",
        "heading": "New Collection",
        "text": "Discover our latest arrivals",
        "button_text": "Shop Now",
        "button_link": "/collections/new"
      }
    }
  },
  "order": ["collection-filters", "featured-products", "promotional-content"]
}
```

## 🎯 Contextual Group Configuration

### Template-Specific Headers
```json
// templates/collection.json
{
  "sections": {
    "header": {
      "type": "header",
      "settings": {
        "show_collection_breadcrumbs": true,
        "collection_nav_style": "tabs",
        "enable_collection_search": true
      }
    }
  }
}

// templates/product.json
{
  "sections": {
    "header": {
      "type": "header",
      "settings": {
        "show_product_breadcrumbs": true,
        "enable_back_to_collection": true,
        "show_collection_nav": false
      }
    }
  }
}
```

### Conditional Section Display
```json
{
  "sections": {
    "announcement": {
      "type": "announcement-bar",
      "settings": {
        "show_on_homepage": true,
        "show_on_collection": true,
        "show_on_product": false,
        "show_on_cart": false,
        "hide_on_checkout": true
      }
    }
  }
}
```

## 📱 Responsive Group Behavior

### Mobile-Optimized Groups
```json
{
  "sections": {
    "header": {
      "type": "header",
      "settings": {
        "mobile_menu_style": "drawer",
        "mobile_logo_position": "center",
        "mobile_search_style": "icon",
        "mobile_cart_style": "icon",
        "enable_mobile_sticky": false,
        "mobile_announcement_priority": "high"
      }
    },
    "footer": {
      "type": "footer",
      "settings": {
        "mobile_layout": "accordion",
        "mobile_social_position": "top",
        "mobile_payment_icons": "bottom",
        "mobile_newsletter_inline": false
      }
    }
  }
}
```

### Breakpoint-Specific Configuration
```json
{
  "sections": {
    "header": {
      "type": "header",
      "settings": {
        "desktop_layout": "horizontal",
        "tablet_layout": "condensed",
        "mobile_layout": "stacked",
        "breakpoint_tablet": "768px",
        "breakpoint_mobile": "480px"
      }
    }
  }
}
```

## 🔄 Dynamic Group Management

### Section Loading and Unloading
```liquid
<!-- Section group container -->
<div data-section-group="header" data-section-id="{{ section.id }}">
  {% for section in layout.header.sections %}
    {% render section.type, section: section %}
  {% endfor %}
</div>

<script>
// Handle section group changes in theme editor
document.addEventListener('shopify:section:load', function(event) {
  const sectionGroup = event.target.dataset.sectionGroup;

  if (sectionGroup === 'header') {
    // Re-initialize header functionality
    initializeHeader();
  }
});

document.addEventListener('shopify:section:unload', function(event) {
  const sectionGroup = event.target.dataset.sectionGroup;

  if (sectionGroup === 'header') {
    // Cleanup header functionality
    cleanupHeader();
  }
});
</script>
```

### Group State Management
```javascript
class SectionGroupManager {
  constructor() {
    this.groups = {
      header: new HeaderGroup(),
      footer: new FooterGroup(),
      aside: new AsideGroup()
    };
    this.init();
  }

  init() {
    this.bindSectionEvents();
    this.initializeGroups();
  }

  bindSectionEvents() {
    document.addEventListener('shopify:section:load', this.onSectionLoad.bind(this));
    document.addEventListener('shopify:section:unload', this.onSectionUnload.bind(this));
    document.addEventListener('shopify:section:reorder', this.onSectionReorder.bind(this));
  }

  onSectionLoad(event) {
    const groupType = event.target.closest('[data-section-group]')?.dataset.sectionGroup;
    if (groupType && this.groups[groupType]) {
      this.groups[groupType].refresh();
    }
  }

  onSectionUnload(event) {
    const groupType = event.target.closest('[data-section-group]')?.dataset.sectionGroup;
    if (groupType && this.groups[groupType]) {
      this.groups[groupType].cleanup();
    }
  }

  onSectionReorder(event) {
    const groupType = event.target.closest('[data-section-group]')?.dataset.sectionGroup;
    if (groupType && this.groups[groupType]) {
      this.groups[groupType].reorder();
    }
  }
}
```

## 📊 Group Performance Optimization

### Lazy Loading Group Sections
```json
{
  "sections": {
    "footer": {
      "type": "footer",
      "settings": {
        "lazy_load_newsletter": true,
        "lazy_load_social_feed": true,
        "defer_non_critical": true
      }
    }
  }
}
```

### Critical Group Prioritization
```liquid
<!-- Prioritize critical header content -->
<div data-section-group="header" data-priority="critical">
  {% section 'header-main' %}
</div>

<!-- Defer non-critical header sections -->
<div data-section-group="header" data-priority="deferred">
  {% section 'header-announcement' %}
  {% section 'header-promotion' %}
</div>
```

## 🚨 Common Group Configuration Pitfalls

### 1. Missing Section References
**Problem**: Group references non-existent sections
```json
{
  "sections": {
    "non-existent-section": {
      "type": "missing-section"
    }
  }
}
```

**Solution**: Verify all referenced sections exist

### 2. Incorrect Group Types
**Problem**: Using invalid group types
```json
{
  "type": "sidebar" // ❌ Invalid type
}
```

**Solution**: Use only `header`, `footer`, or `aside`

### 3. Circular Dependencies
**Problem**: Sections referencing each other
```json
{
  "header-a": { "includes": "header-b" },
  "header-b": { "includes": "header-a" }
}
```

**Solution**: Design clear section hierarchies

### 4. Performance Issues
**Problem**: Too many sections in groups
```json
{
  "sections": {
    // ❌ 20+ sections cause performance issues
  }
}
```

**Solution**: Limit sections per group and use lazy loading

## 🛠️ Development Workflow

### Group Development Process
1. **Design layout areas** - Plan header, footer, aside needs
2. **Create section groups** - Define group structure
3. **Build supporting sections** - Create sections for groups
4. **Test responsiveness** - Verify mobile/desktop behavior
5. **Optimize performance** - Implement lazy loading patterns

### Testing Group Configurations
```bash
# Validate group JSON structure
npx jsonlint layout/header.json

# Test with Theme Check
shopify theme check

# Preview in development
shopify theme dev
```

### Group Maintenance
- **Version control** - Track group configuration changes
- **Performance monitoring** - Monitor group loading times
- **Merchant feedback** - Iterate based on customization needs
- **Cross-template testing** - Verify group behavior across templates

---

Section groups provide flexible layout management while maintaining performance and usability. Well-designed groups balance merchant customization with theme functionality and loading speed.