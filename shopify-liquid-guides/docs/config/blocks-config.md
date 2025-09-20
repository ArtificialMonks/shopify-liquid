# Block Configuration - Component-Level Settings

Block configuration defines the settings and behavior of individual blocks within sections. This guide covers block schema design, dynamic block patterns, app block integration, and best practices for creating flexible, reusable components.

## 🎯 Block Configuration Overview

### Purpose and Function
Block configuration enables:
- **Component modularity** - Reusable content blocks
- **Merchant control** - Add, remove, reorder blocks
- **Dynamic content** - Flexible content composition
- **App integration** - Third-party block support

### Block Types
- **Theme blocks** - Built into theme sections
- **App blocks** - Created by Shopify apps
- **Dynamic blocks** - Configurable content components
- **Static blocks** - Fixed functionality blocks

## 🏗️ Block Schema Structure

### Basic Block Configuration
```json
{
  "type": "text",
  "name": "Text Block",
  "settings": [
    {
      "type": "richtext",
      "id": "content",
      "label": "Text content",
      "default": "<p>Add your text content here</p>",
      "info": "Supports HTML formatting"
    },
    {
      "type": "select",
      "id": "text_size",
      "label": "Text size",
      "options": [
        { "value": "small", "label": "Small" },
        { "value": "medium", "label": "Medium" },
        { "value": "large", "label": "Large" }
      ],
      "default": "medium"
    },
    {
      "type": "select",
      "id": "text_alignment",
      "label": "Text alignment",
      "options": [
        { "value": "left", "label": "Left" },
        { "value": "center", "label": "Center" },
        { "value": "right", "label": "Right" }
      ],
      "default": "left"
    }
  ]
}
```

### Advanced Block Schema
```json
{
  "type": "feature",
  "name": "Feature Block",
  "settings": [
    {
      "type": "header",
      "content": "Content"
    },
    {
      "type": "image_picker",
      "id": "icon",
      "label": "Feature icon",
      "info": "Recommended size: 64x64px"
    },
    {
      "type": "text",
      "id": "heading",
      "label": "Feature heading",
      "default": "Feature Title"
    },
    {
      "type": "textarea",
      "id": "description",
      "label": "Feature description",
      "default": "Describe your feature here"
    },
    {
      "type": "url",
      "id": "link",
      "label": "Feature link",
      "info": "Optional link for the feature"
    },
    {
      "type": "header",
      "content": "Styling"
    },
    {
      "type": "color",
      "id": "icon_color",
      "label": "Icon color",
      "default": "#000000"
    },
    {
      "type": "select",
      "id": "layout",
      "label": "Layout style",
      "options": [
        { "value": "vertical", "label": "Icon above text" },
        { "value": "horizontal", "label": "Icon beside text" },
        { "value": "overlay", "label": "Icon overlaid on text" }
      ],
      "default": "vertical"
    },
    {
      "type": "range",
      "id": "icon_size",
      "label": "Icon size",
      "min": 32,
      "max": 128,
      "step": 8,
      "unit": "px",
      "default": 64
    }
  ]
}
```

## 🚀 Common Block Patterns

### Product Block
```json
{
  "type": "product",
  "name": "Featured Product",
  "settings": [
    {
      "type": "product",
      "id": "product",
      "label": "Product",
      "info": "Select a product to feature"
    },
    {
      "type": "checkbox",
      "id": "show_vendor",
      "label": "Show vendor",
      "default": false
    },
    {
      "type": "checkbox",
      "id": "show_price",
      "label": "Show price",
      "default": true
    },
    {
      "type": "checkbox",
      "id": "show_description",
      "label": "Show description",
      "default": true
    },
    {
      "type": "select",
      "id": "image_ratio",
      "label": "Image aspect ratio",
      "options": [
        { "value": "natural", "label": "Natural" },
        { "value": "square", "label": "Square" },
        { "value": "portrait", "label": "Portrait" },
        { "value": "landscape", "label": "Landscape" }
      ],
      "default": "natural"
    }
  ]
}
```

### Button Block
```json
{
  "type": "button",
  "name": "Button",
  "settings": [
    {
      "type": "text",
      "id": "button_text",
      "label": "Button text",
      "default": "Click here"
    },
    {
      "type": "url",
      "id": "button_link",
      "label": "Button link"
    },
    {
      "type": "select",
      "id": "button_style",
      "label": "Button style",
      "options": [
        { "value": "primary", "label": "Primary" },
        { "value": "secondary", "label": "Secondary" },
        { "value": "outline", "label": "Outline" },
        { "value": "text", "label": "Text only" }
      ],
      "default": "primary"
    },
    {
      "type": "select",
      "id": "button_size",
      "label": "Button size",
      "options": [
        { "value": "small", "label": "Small" },
        { "value": "medium", "label": "Medium" },
        { "value": "large", "label": "Large" }
      ],
      "default": "medium"
    },
    {
      "type": "checkbox",
      "id": "full_width",
      "label": "Full width button",
      "default": false
    }
  ]
}
```

### Image Block with Advanced Options
```json
{
  "type": "image",
  "name": "Image Block",
  "settings": [
    {
      "type": "header",
      "content": "Image"
    },
    {
      "type": "image_picker",
      "id": "image",
      "label": "Image",
      "info": "High resolution images recommended"
    },
    {
      "type": "text",
      "id": "alt_text",
      "label": "Alt text",
      "info": "Describe the image for accessibility"
    },
    {
      "type": "header",
      "content": "Layout"
    },
    {
      "type": "select",
      "id": "image_fit",
      "label": "Image fit",
      "options": [
        { "value": "cover", "label": "Cover (crop to fit)" },
        { "value": "contain", "label": "Contain (fit within bounds)" },
        { "value": "fill", "label": "Fill (stretch to fit)" }
      ],
      "default": "cover"
    },
    {
      "type": "select",
      "id": "image_position",
      "label": "Image position",
      "options": [
        { "value": "top", "label": "Top" },
        { "value": "center", "label": "Center" },
        { "value": "bottom", "label": "Bottom" }
      ],
      "default": "center"
    },
    {
      "type": "header",
      "content": "Effects"
    },
    {
      "type": "range",
      "id": "border_radius",
      "label": "Border radius",
      "min": 0,
      "max": 50,
      "step": 5,
      "unit": "px",
      "default": 0
    },
    {
      "type": "checkbox",
      "id": "enable_hover_effect",
      "label": "Enable hover effect",
      "default": false
    },
    {
      "type": "checkbox",
      "id": "enable_lazy_loading",
      "label": "Enable lazy loading",
      "default": true,
      "info": "Improves page load speed"
    }
  ]
}
```

## 🎨 Advanced Block Patterns

### Video Block
```json
{
  "type": "video",
  "name": "Video Block",
  "settings": [
    {
      "type": "header",
      "content": "Video Source"
    },
    {
      "type": "radio",
      "id": "video_type",
      "label": "Video type",
      "options": [
        { "value": "upload", "label": "Upload video file" },
        { "value": "youtube", "label": "YouTube video" },
        { "value": "vimeo", "label": "Vimeo video" }
      ],
      "default": "upload"
    },
    {
      "type": "video",
      "id": "video_file",
      "label": "Video file",
      "info": "MP4 format recommended. Shown when 'Upload video file' is selected."
    },
    {
      "type": "text",
      "id": "video_url",
      "label": "Video URL",
      "info": "YouTube or Vimeo URL. Shown when external video is selected.",
      "placeholder": "https://www.youtube.com/watch?v=..."
    },
    {
      "type": "image_picker",
      "id": "poster_image",
      "label": "Poster image",
      "info": "Thumbnail shown before video plays"
    },
    {
      "type": "header",
      "content": "Playback Settings"
    },
    {
      "type": "checkbox",
      "id": "autoplay",
      "label": "Autoplay video",
      "default": false,
      "info": "Videos must be muted to autoplay"
    },
    {
      "type": "checkbox",
      "id": "loop",
      "label": "Loop video",
      "default": false
    },
    {
      "type": "checkbox",
      "id": "muted",
      "label": "Mute video",
      "default": true,
      "info": "Required for autoplay"
    },
    {
      "type": "checkbox",
      "id": "show_controls",
      "label": "Show video controls",
      "default": true
    }
  ]
}
```

### Testimonial Block
```json
{
  "type": "testimonial",
  "name": "Customer Testimonial",
  "settings": [
    {
      "type": "header",
      "content": "Testimonial Content"
    },
    {
      "type": "richtext",
      "id": "quote",
      "label": "Customer quote",
      "default": "<p>This product exceeded my expectations!</p>"
    },
    {
      "type": "text",
      "id": "customer_name",
      "label": "Customer name",
      "default": "Happy Customer"
    },
    {
      "type": "text",
      "id": "customer_title",
      "label": "Customer title",
      "placeholder": "CEO, Company Name"
    },
    {
      "type": "image_picker",
      "id": "customer_photo",
      "label": "Customer photo",
      "info": "Square images work best"
    },
    {
      "type": "header",
      "content": "Rating"
    },
    {
      "type": "range",
      "id": "star_rating",
      "label": "Star rating",
      "min": 1,
      "max": 5,
      "step": 1,
      "default": 5
    },
    {
      "type": "checkbox",
      "id": "show_stars",
      "label": "Show star rating",
      "default": true
    },
    {
      "type": "header",
      "content": "Styling"
    },
    {
      "type": "select",
      "id": "layout_style",
      "label": "Layout style",
      "options": [
        { "value": "card", "label": "Card style" },
        { "value": "minimal", "label": "Minimal style" },
        { "value": "quote", "label": "Quote style" }
      ],
      "default": "card"
    }
  ]
}
```

### Social Media Block
```json
{
  "type": "social_media",
  "name": "Social Media",
  "settings": [
    {
      "type": "header",
      "content": "Social Links"
    },
    {
      "type": "url",
      "id": "facebook_url",
      "label": "Facebook URL",
      "info": "https://facebook.com/yourpage"
    },
    {
      "type": "url",
      "id": "instagram_url",
      "label": "Instagram URL",
      "info": "https://instagram.com/youraccount"
    },
    {
      "type": "url",
      "id": "twitter_url",
      "label": "Twitter URL",
      "info": "https://twitter.com/youraccount"
    },
    {
      "type": "url",
      "id": "youtube_url",
      "label": "YouTube URL",
      "info": "https://youtube.com/c/yourchannel"
    },
    {
      "type": "url",
      "id": "tiktok_url",
      "label": "TikTok URL",
      "info": "https://tiktok.com/@youraccount"
    },
    {
      "type": "header",
      "content": "Display Options"
    },
    {
      "type": "select",
      "id": "icon_style",
      "label": "Icon style",
      "options": [
        { "value": "solid", "label": "Solid" },
        { "value": "outline", "label": "Outline" },
        { "value": "branded", "label": "Branded colors" }
      ],
      "default": "solid"
    },
    {
      "type": "range",
      "id": "icon_size",
      "label": "Icon size",
      "min": 16,
      "max": 48,
      "step": 4,
      "unit": "px",
      "default": 24
    },
    {
      "type": "select",
      "id": "alignment",
      "label": "Alignment",
      "options": [
        { "value": "left", "label": "Left" },
        { "value": "center", "label": "Center" },
        { "value": "right", "label": "Right" }
      ],
      "default": "left"
    }
  ]
}
```

## 🔧 App Block Integration

### App Block Schema
```json
{
  "type": "@app",
  "name": "App Block",
  "settings": [
    {
      "type": "paragraph",
      "content": "This block will be replaced by app-specific settings when an app is selected."
    }
  ]
}
```

### App Block Implementation
```liquid
<!-- In section template -->
{% for block in section.blocks %}
  {% case block.type %}
    {% when '@app' %}
      {% render block %}
    {% when 'text' %}
      {% render 'block-text', block: block %}
    {% when 'button' %}
      {% render 'block-button', block: block %}
  {% endcase %}
{% endfor %}
```

### App Block Detection
```liquid
<!-- Check if block is from an app -->
{% if block.type contains '@app' %}
  <div class="app-block" data-app-id="{{ block.settings.app_id }}">
    {% render block %}
  </div>
{% endif %}
```

## 📱 Responsive Block Configuration

### Mobile-Optimized Blocks
```json
{
  "type": "responsive_content",
  "name": "Responsive Content",
  "settings": [
    {
      "type": "header",
      "content": "Desktop Settings"
    },
    {
      "type": "range",
      "id": "columns_desktop",
      "label": "Desktop columns",
      "min": 1,
      "max": 4,
      "step": 1,
      "default": 3
    },
    {
      "type": "select",
      "id": "text_size_desktop",
      "label": "Desktop text size",
      "options": [
        { "value": "small", "label": "Small" },
        { "value": "medium", "label": "Medium" },
        { "value": "large", "label": "Large" }
      ],
      "default": "medium"
    },
    {
      "type": "header",
      "content": "Mobile Settings"
    },
    {
      "type": "range",
      "id": "columns_mobile",
      "label": "Mobile columns",
      "min": 1,
      "max": 2,
      "step": 1,
      "default": 1
    },
    {
      "type": "select",
      "id": "text_size_mobile",
      "label": "Mobile text size",
      "options": [
        { "value": "small", "label": "Small" },
        { "value": "medium", "label": "Medium" },
        { "value": "large", "label": "Large" }
      ],
      "default": "small"
    }
  ]
}
```

## 📊 Block Performance Optimization

### Conditional Block Loading
```json
{
  "type": "performance_block",
  "name": "Performance Optimized Block",
  "settings": [
    {
      "type": "checkbox",
      "id": "lazy_load",
      "label": "Enable lazy loading",
      "default": true,
      "info": "Improves page load speed"
    },
    {
      "type": "checkbox",
      "id": "critical_above_fold",
      "label": "Critical above-the-fold content",
      "default": false,
      "info": "Loads immediately for better Core Web Vitals"
    },
    {
      "type": "select",
      "id": "loading_priority",
      "label": "Loading priority",
      "options": [
        { "value": "high", "label": "High priority" },
        { "value": "normal", "label": "Normal priority" },
        { "value": "low", "label": "Low priority" }
      ],
      "default": "normal"
    }
  ]
}
```

### Block Caching Configuration
```json
{
  "type": "cached_content",
  "name": "Cached Content Block",
  "settings": [
    {
      "type": "checkbox",
      "id": "enable_caching",
      "label": "Enable content caching",
      "default": true,
      "info": "Caches block output for faster loading"
    },
    {
      "type": "range",
      "id": "cache_duration",
      "label": "Cache duration",
      "min": 5,
      "max": 60,
      "step": 5,
      "unit": "minutes",
      "default": 15,
      "info": "How long to cache block content"
    }
  ]
}
```

## 🚨 Common Block Configuration Pitfalls

### 1. Missing Block Types
**Problem**: Invalid or missing block type
```json
{
  "name": "Block without type" // ❌ Missing 'type' property
}
```

**Solution**: Always include valid block type
```json
{
  "type": "text",
  "name": "Text Block"
}
```

### 2. Invalid Setting References
**Problem**: Block settings with invalid structure
```json
{
  "type": "text",
  "settings": [
    {
      "id": "content",
      "label": "Content" // ❌ Missing 'type' property
    }
  ]
}
```

**Solution**: Include all required setting properties
```json
{
  "type": "text",
  "settings": [
    {
      "type": "richtext",
      "id": "content",
      "label": "Content"
    }
  ]
}
```

### 3. Block Limit Violations
**Problem**: Too many blocks in section
```json
{
  "max_blocks": 100 // ❌ Exceeds recommended limit
}
```

**Solution**: Keep reasonable block limits
```json
{
  "max_blocks": 20 // ✅ Reasonable limit
}
```

### 4. Performance Issues
**Problem**: Heavy blocks without optimization
```json
{
  "type": "video",
  "settings": [
    {
      "type": "video",
      "id": "background_video" // ❌ No lazy loading options
    }
  ]
}
```

**Solution**: Include performance settings
```json
{
  "type": "video",
  "settings": [
    {
      "type": "video",
      "id": "background_video"
    },
    {
      "type": "checkbox",
      "id": "lazy_load",
      "label": "Lazy load video",
      "default": true
    }
  ]
}
```

## 🛠️ Development Workflow

### Block Development Process
1. **Plan block functionality** - Define purpose and features
2. **Design schema structure** - Create flexible, intuitive settings
3. **Build block template** - Implement Liquid rendering logic
4. **Test block behavior** - Verify settings and responsiveness
5. **Optimize performance** - Implement loading strategies

### Block Testing
```liquid
<!-- Test block with various settings -->
{% for block in section.blocks %}
  {% case block.type %}
    {% when 'text' %}
      <div class="block-text" {{ block.shopify_attributes }}>
        {% if block.settings.content != blank %}
          <div class="text-{{ block.settings.text_size }}">
            {{ block.settings.content }}
          </div>
        {% endif %}
      </div>
  {% endcase %}
{% endfor %}
```

### Block Validation
```bash
# Validate block schema
npx jsonlint section-schema.json

# Test with Theme Check
shopify theme check

# Preview block behavior
shopify theme dev
```

---

Block configuration enables flexible, reusable content components that merchants can customize through the theme editor. Well-designed blocks balance functionality with performance and ease of use.