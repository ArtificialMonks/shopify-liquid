# Section Groups Documentation

Section groups enable dynamic organization of theme layout areas, allowing merchants to customize headers, footers, and sidebars through the theme editor. This documentation covers section group implementation, contextual overrides, and advanced configuration patterns.

## 📁 What's in This Section

### Core Documentation
| File | Purpose | What You'll Learn |
|------|---------|-------------------|
| **[group-fundamentals.md](./group-fundamentals.md)** | Section group basics | Core concepts, group types, implementation |
| **[contextual-overrides.md](./contextual-overrides.md)** | Template-specific groups | Different configurations per template |
| **[dynamic-sources.md](./dynamic-sources.md)** | Data-driven sections | API-driven content, metaobject integration |
| **[performance-patterns.md](./performance-patterns.md)** | Optimization strategies | Lazy loading, critical rendering, caching |

### Practical Resources
| Directory | Purpose | Contents |
|-----------|---------|----------|
| **[examples/](./examples/)** | Working group configurations | Complete section group files, integration patterns |

## 🎯 Quick Start

### For Beginners
1. Start with **[group-fundamentals.md](./group-fundamentals.md)** to understand section groups
2. Review **[examples/](./examples/)** for practical implementations
3. Study **[contextual-overrides.md](./contextual-overrides.md)** for template customization

### For Experienced Developers
- Jump to **[dynamic-sources.md](./dynamic-sources.md)** for advanced data integration
- Browse **[performance-patterns.md](./performance-patterns.md)** for optimization techniques
- Reference **[examples/](./examples/)** for production-ready configurations

## 📋 Section Groups Overview

### What Are Section Groups?
Section groups are **configurable layout areas** that enable:
- **Flexible headers** - Navigation, announcements, search, utilities
- **Dynamic footers** - Links, newsletters, social media, legal
- **Contextual sidebars** - Filters, recommendations, promotional content
- **Template-specific layouts** - Different configurations per page type

### Online Store 2.0 Integration
Section groups are part of Shopify's **Online Store 2.0** architecture:
- **Merchant customization** - Add, remove, reorder sections via theme editor
- **Template flexibility** - Override group configurations per template
- **App block support** - Third-party integrations within groups
- **Performance optimization** - Selective loading and rendering

## 🏗️ Group Types and Structure

### Available Group Types
```json
{
  "header": {
    "name": "Header",
    "type": "header",
    "sections": { ... }
  },
  "footer": {
    "name": "Footer",
    "type": "footer",
    "sections": { ... }
  },
  "aside": {
    "name": "Sidebar",
    "type": "aside",
    "sections": { ... }
  }
}
```

### Basic Group Structure
```json
{
  "name": "Header Configuration",
  "type": "header",
  "sections": {
    "announcement-bar": {
      "type": "announcement-bar",
      "settings": {
        "text": "Free shipping on orders over $50",
        "background_color": "#000000"
      }
    },
    "header-main": {
      "type": "header",
      "settings": {
        "logo_width": 150,
        "menu": "main-menu"
      }
    }
  },
  "order": ["announcement-bar", "header-main"]
}
```

## 🚀 Implementation Patterns

### Header Group Configuration
```json
{
  "name": "Header",
  "type": "header",
  "sections": {
    "announcement": {
      "type": "announcement-bar",
      "settings": {
        "text": "Welcome to our store",
        "link": "/collections/all",
        "show_close": true,
        "background_color": "#000000",
        "text_color": "#ffffff"
      }
    },
    "header": {
      "type": "header",
      "settings": {
        "logo_width": 200,
        "logo_position": "left",
        "menu": "main-menu",
        "enable_search": true,
        "enable_sticky": true,
        "cart_type": "drawer"
      }
    },
    "promotion": {
      "type": "promotional-banner",
      "settings": {
        "text": "New collection available now",
        "button_text": "Shop now",
        "button_link": "/collections/new"
      }
    }
  },
  "order": ["announcement", "header", "promotion"]
}
```

### Footer Group Configuration
```json
{
  "name": "Footer",
  "type": "footer",
  "sections": {
    "newsletter": {
      "type": "newsletter-signup",
      "settings": {
        "heading": "Stay in the loop",
        "subheading": "Get exclusive offers and updates",
        "show_social_icons": true
      }
    },
    "footer-content": {
      "type": "footer-multicolumn",
      "blocks": {
        "menu-1": {
          "type": "link_list",
          "settings": {
            "heading": "Shop",
            "menu": "footer-shop"
          }
        },
        "menu-2": {
          "type": "link_list",
          "settings": {
            "heading": "Support",
            "menu": "footer-support"
          }
        },
        "contact": {
          "type": "contact_info",
          "settings": {
            "heading": "Contact",
            "address": "123 Store St, City, State",
            "phone": "+1 555-123-4567"
          }
        }
      },
      "block_order": ["menu-1", "menu-2", "contact"]
    },
    "footer-bottom": {
      "type": "footer-copyright",
      "settings": {
        "show_payment_icons": true,
        "show_social_icons": true,
        "copyright_text": "© 2024 Your Store"
      }
    }
  },
  "order": ["newsletter", "footer-content", "footer-bottom"]
}
```

## 🎨 Advanced Configuration Patterns

### Contextual Group Overrides
```json
// layout/header.json - Global header
{
  "name": "Header",
  "type": "header",
  "sections": {
    "header": {
      "type": "header",
      "settings": {
        "show_breadcrumbs": false,
        "enable_collection_nav": false
      }
    }
  }
}

// templates/collection.json - Collection-specific override
{
  "sections": {
    "header": {
      "type": "header",
      "settings": {
        "show_breadcrumbs": true,
        "enable_collection_nav": true,
        "collection_nav_style": "tabs"
      }
    }
  }
}
```

### Dynamic Content Integration
```json
{
  "name": "Dynamic Sidebar",
  "type": "aside",
  "sections": {
    "filters": {
      "type": "collection-filters",
      "settings": {
        "show_when": "collection_has_products",
        "min_products": 5
      }
    },
    "recommendations": {
      "type": "product-recommendations",
      "settings": {
        "source": "related_products",
        "products_to_show": 4,
        "show_when": "product_page"
      }
    },
    "recent-products": {
      "type": "recently-viewed",
      "settings": {
        "products_to_show": 3,
        "show_when": "has_viewed_products"
      }
    }
  },
  "order": ["filters", "recommendations", "recent-products"]
}
```

### Responsive Group Behavior
```json
{
  "sections": {
    "header": {
      "type": "header",
      "settings": {
        "desktop_layout": "horizontal",
        "mobile_layout": "stacked",
        "desktop_logo_position": "left",
        "mobile_logo_position": "center",
        "desktop_menu_style": "horizontal",
        "mobile_menu_style": "drawer"
      }
    }
  }
}
```

## 🔧 Group Management and Events

### Section Group Events
```liquid
<!-- Section group container with event handling -->
<div data-section-group="header" data-group-id="{{ section_group.id }}">
  {% for section in section_group.sections %}
    <div data-section-type="{{ section.type }}" data-section-id="{{ section.id }}">
      {% render section.type, section: section %}
    </div>
  {% endfor %}
</div>

<script>
// Handle section group changes
document.addEventListener('shopify:section:load', function(event) {
  const sectionGroup = event.target.closest('[data-section-group]');
  if (sectionGroup) {
    reinitializeGroup(sectionGroup.dataset.sectionGroup);
  }
});

document.addEventListener('shopify:section:unload', function(event) {
  const sectionGroup = event.target.closest('[data-section-group]');
  if (sectionGroup) {
    cleanupGroup(sectionGroup.dataset.sectionGroup);
  }
});
</script>
```

### Dynamic Group Loading
```javascript
class SectionGroupManager {
  constructor() {
    this.groups = new Map();
    this.init();
  }

  init() {
    this.bindEvents();
    this.loadVisibleGroups();
  }

  bindEvents() {
    document.addEventListener('shopify:section:load', this.onSectionLoad.bind(this));
    document.addEventListener('shopify:section:unload', this.onSectionUnload.bind(this));
    document.addEventListener('shopify:section:reorder', this.onSectionReorder.bind(this));
  }

  onSectionLoad(event) {
    const groupElement = event.target.closest('[data-section-group]');
    if (groupElement) {
      const groupType = groupElement.dataset.sectionGroup;
      this.reinitializeGroup(groupType, groupElement);
    }
  }

  reinitializeGroup(groupType, element) {
    // Cleanup existing group instance
    if (this.groups.has(groupType)) {
      this.groups.get(groupType).destroy();
    }

    // Create new group instance
    const GroupClass = this.getGroupClass(groupType);
    if (GroupClass) {
      const groupInstance = new GroupClass(element);
      this.groups.set(groupType, groupInstance);
    }
  }

  getGroupClass(groupType) {
    const groupClasses = {
      header: HeaderGroup,
      footer: FooterGroup,
      aside: AsideGroup
    };
    return groupClasses[groupType];
  }
}
```

## 📱 Responsive and Performance Optimization

### Conditional Loading
```json
{
  "sections": {
    "mobile-header": {
      "type": "mobile-header",
      "settings": {
        "show_on_desktop": false,
        "show_on_mobile": true
      }
    },
    "desktop-header": {
      "type": "desktop-header",
      "settings": {
        "show_on_desktop": true,
        "show_on_mobile": false
      }
    }
  }
}
```

### Lazy Loading Configuration
```json
{
  "sections": {
    "footer-newsletter": {
      "type": "newsletter-signup",
      "settings": {
        "lazy_load": true,
        "load_trigger": "scroll_near",
        "load_offset": "200px"
      }
    },
    "footer-social": {
      "type": "social-media-feed",
      "settings": {
        "lazy_load": true,
        "load_trigger": "user_interaction"
      }
    }
  }
}
```

### Critical Rendering Path
```liquid
<!-- Critical header content -->
<div data-section-group="header" data-priority="critical">
  {% section 'header-core' %}
</div>

<!-- Deferred header content -->
<div data-section-group="header" data-priority="deferred" data-lazy-load>
  {% section 'header-announcement' %}
  {% section 'header-promotion' %}
</div>
```

## 🌟 Advanced Features

### Template-Specific Groups
```json
// templates/product.json
{
  "layout": "product",
  "sections": {
    // Override global header for product pages
    "header": {
      "type": "header",
      "settings": {
        "show_product_breadcrumbs": true,
        "show_back_to_collection": true,
        "enable_product_search": true
      }
    }
  },
  "section_groups": {
    "aside": {
      "sections": {
        "product-recommendations": {
          "type": "product-recommendations",
          "settings": {
            "heading": "You might also like",
            "products_to_show": 6
          }
        },
        "recently-viewed": {
          "type": "recently-viewed-products",
          "settings": {
            "heading": "Recently viewed",
            "products_to_show": 4
          }
        }
      },
      "order": ["product-recommendations", "recently-viewed"]
    }
  }
}
```

### App Block Integration
```json
{
  "sections": {
    "header": {
      "type": "header",
      "blocks": {
        "app-reviews": {
          "type": "@app",
          "settings": {}
        },
        "app-wishlist": {
          "type": "@app",
          "settings": {}
        }
      },
      "block_order": ["app-reviews", "app-wishlist"]
    }
  }
}
```

### Metaobject Integration
```json
{
  "sections": {
    "dynamic-content": {
      "type": "metaobject-content",
      "settings": {
        "metaobject_type": "promotional_banner",
        "handle": "current_promotion",
        "show_when_active": true
      }
    }
  }
}
```

## 🚨 Common Section Group Pitfalls

### 1. Invalid Group Types
**Problem**: Using incorrect group type
```json
{
  "type": "sidebar" // ❌ Invalid - use 'aside'
}
```

**Solution**: Use only valid group types
```json
{
  "type": "aside" // ✅ Valid group type
}
```

### 2. Missing Section References
**Problem**: Group references non-existent sections
```json
{
  "sections": {
    "non-existent": {
      "type": "missing-section" // ❌ Section doesn't exist
    }
  }
}
```

**Solution**: Verify all referenced sections exist

### 3. Performance Issues
**Problem**: Too many sections in group
```json
{
  "sections": {
    // ❌ 15+ sections cause performance issues
  }
}
```

**Solution**: Limit sections and use lazy loading
```json
{
  "sections": {
    "critical-section": { "priority": "high" },
    "deferred-section": { "lazy_load": true }
  }
}
```

### 4. Circular Dependencies
**Problem**: Sections referencing each other
```json
{
  "header-a": { "includes": "header-b" },
  "header-b": { "includes": "header-a" } // ❌ Circular reference
}
```

**Solution**: Design clear section hierarchies

## 📊 Testing and Validation

### Group Configuration Testing
```bash
# Validate JSON structure
npx jsonlint layout/header.json

# Test with Theme Check
shopify theme check

# Preview different templates
shopify theme dev --template=product
shopify theme dev --template=collection
```

### Performance Testing
```javascript
// Monitor section group loading performance
class GroupPerformanceMonitor {
  constructor() {
    this.metrics = new Map();
    this.init();
  }

  init() {
    this.observeGroupLoading();
    this.measureRenderTime();
  }

  observeGroupLoading() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const groupType = entry.target.dataset.sectionGroup;
          this.startTiming(groupType);
        }
      });
    });

    document.querySelectorAll('[data-section-group]').forEach(group => {
      observer.observe(group);
    });
  }

  startTiming(groupType) {
    const startTime = performance.now();
    this.metrics.set(groupType, { startTime });
  }

  endTiming(groupType) {
    const metric = this.metrics.get(groupType);
    if (metric) {
      metric.endTime = performance.now();
      metric.duration = metric.endTime - metric.startTime;

      console.log(`Section group ${groupType} loaded in ${metric.duration.toFixed(2)}ms`);
    }
  }
}
```

## 🛠️ Development Workflow

### Group Development Process
1. **Plan layout structure** - Design header, footer, sidebar needs
2. **Create base configurations** - Build default group files
3. **Implement template overrides** - Add contextual variations
4. **Optimize performance** - Add lazy loading and critical rendering
5. **Test across templates** - Verify behavior on all page types

### Maintenance Best Practices
- **Version control** - Track group configuration changes
- **Performance monitoring** - Monitor loading times and user impact
- **Merchant feedback** - Iterate based on customization needs
- **Template testing** - Verify groups work across all templates

---

Section groups provide powerful layout flexibility while maintaining performance and usability. Well-designed groups balance merchant customization with optimal loading speed and user experience across all devices and page types.