# Block Types & Configuration - Advanced Patterns

Blocks are **reusable content modules** that merchants can add, remove, and reorder within sections. This guide covers both basic and advanced block patterns, including AI-generated block structures and professional development techniques.

> 💡 **Think of blocks like smart LEGO pieces** - each one is self-contained but works perfectly with others in a section.

---

## Basic Block Concepts

### What Are Blocks?

Blocks allow merchants to:
- **Add multiple content items** (testimonials, slides, features)
- **Reorder content** by dragging in the theme editor
- **Customize each item** independently
- **Remove unwanted items** without affecting others

### Block vs Section

- **Section** = The container (e.g., "Testimonials")
- **Block** = Individual items (e.g., each testimonial)

```liquid
<!-- Section: Testimonials -->
<div class="testimonials-section">
  {% for block in section.blocks %}
    <!-- Block: Individual testimonial -->
    <div class="testimonial-card" {{ block.shopify_attributes }}>
      {{ block.settings.quote }}
    </div>
  {% endfor %}
</div>
```

---

## Basic Block Structure

### Simple Block Example

```liquid
<!-- In your section .liquid file -->
<div class="features-section">
  {% if section.blocks.size > 0 %}
    <div class="features-grid">
      {% for block in section.blocks %}
        {% case block.type %}
          {% when 'feature' %}
            <div class="feature-card" {{ block.shopify_attributes }}>
              {% if block.settings.icon %}
                <img src="{{ block.settings.icon | image_url: width: 80 }}" alt="">
              {% endif %}
              <h3>{{ block.settings.title | escape }}</h3>
              <p>{{ block.settings.description | escape }}</p>
            </div>
        {% endcase %}
      {% endfor %}
    </div>
  {% endif %}
</div>

{% schema %}
{
  "name": "Feature Section",
  "max_blocks": 6,
  "blocks": [
    {
      "type": "feature",
      "name": "Feature",
      "settings": [
        {
          "type": "image_picker",
          "id": "icon",
          "label": "Icon"
        },
        {
          "type": "text",
          "id": "title",
          "label": "Title",
          "default": "Feature Title"
        },
        {
          "type": "textarea",
          "id": "description",
          "label": "Description",
          "default": "Feature description goes here"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Features",
      "blocks": [
        {"type": "feature"},
        {"type": "feature"},
        {"type": "feature"}
      ]
    }
  ]
}
{% endschema %}
```

---

## Advanced Block Pattern: AI-Generated Structure

Based on modern Shopify development, here's the **professional block format** used by AI tools and advanced developers:

### 1. Documentation Pattern

```liquid
{% doc %}
  @prompt
    Create a two-column section where one column displays an uploaded MP4 video and the other column contains a customizable text block. The section should be responsive and allow merchants to upload their own video file and edit the text content.
{% enddoc %}
```

**Purpose**: Documents the block's functionality for team collaboration and AI regeneration.

### 2. Unique ID Generation

```liquid
{% assign ai_gen_id = block.id | replace: '_', '' | downcase %}
```

**Purpose**: Creates unique, collision-free CSS class names for multiple block instances.

### 3. Scoped Styling System

```liquid
{% style %}
  .video-text-block-{{ ai_gen_id }} {
    display: flex;
    align-items: center;
    gap: {{ block.settings.column_gap }}px;
    padding: {{ block.settings.section_padding }}px;
    background-color: {{ block.settings.background_color }};
  }

  .video-text-block__column-{{ ai_gen_id }} {
    flex: 1;
  }

  .video-text-block__video-{{ ai_gen_id }} {
    width: 100%;
    height: auto;
    border-radius: {{ block.settings.video_border_radius }}px;
  }

  /* Conditional styling based on settings */
  {% if block.settings.layout == 'text_left' %}
    .video-text-block-{{ ai_gen_id }} {
      flex-direction: row;
    }
  {% else %}
    .video-text-block-{{ ai_gen_id }} {
      flex-direction: row-reverse;
    }
  {% endif %}

  /* Responsive design */
  @media screen and (max-width: 749px) {
    .video-text-block-{{ ai_gen_id }} {
      flex-direction: column;
      gap: {{ block.settings.mobile_gap }}px;
    }
  }
{% endstyle %}
```

**Key Features**:
- **Scoped classes** prevent conflicts between block instances
- **Dynamic values** from block settings
- **Conditional CSS** based on user choices
- **Mobile-first responsive design**

### 4. Smart HTML Structure

```liquid
<div
  class="video-text-block-{{ ai_gen_id }}"
  {{ block.shopify_attributes }}
>
  <!-- Video Column -->
  <div class="video-text-block__column-{{ ai_gen_id }}">
    <div class="video-text-block__video-wrapper-{{ ai_gen_id }}">
      {% if block.settings.video_file %}
        <video
          class="video-text-block__video-{{ ai_gen_id }}"
          {% if block.settings.autoplay %}autoplay{% endif %}
          {% if block.settings.loop %}loop{% endif %}
          {% if block.settings.muted %}muted{% endif %}
          {% if block.settings.controls %}controls{% endif %}
          preload="metadata"
          playsinline
        >
          <source src="{{ block.settings.video_file }}" type="video/mp4">
          Your browser does not support the video tag.
        </video>
      {% else %}
        <!-- Graceful fallback with helpful placeholder -->
        <div class="video-text-block__placeholder-{{ ai_gen_id }}">
          <svg><!-- Video icon --></svg>
          <div class="empty-state-text">Upload an MP4 video file</div>
        </div>
      {% endif %}
    </div>
  </div>

  <!-- Text Column -->
  <div class="video-text-block__column-{{ ai_gen_id }}">
    <div class="video-text-block__text-content-{{ ai_gen_id }}">
      {% if block.settings.text_content != blank %}
        {{ block.settings.text_content }}
      {% else %}
        <!-- Default content when empty -->
        <h2>Add your heading here</h2>
        <p>Add your text content here. You can include multiple paragraphs.</p>
      {% endif %}
    </div>
  </div>
</div>
```

**Features**:
- **Conditional rendering** with fallbacks
- **Semantic HTML structure**
- **Accessibility-friendly** attributes
- **BEM-style naming** with unique IDs

### 5. Comprehensive Schema

```json
{
  "name": "Video and Text",
  "settings": [
    {
      "type": "header",
      "content": "Layout"
    },
    {
      "type": "select",
      "id": "layout",
      "label": "Layout",
      "options": [
        {"value": "text_left", "label": "Text left, video right"},
        {"value": "text_right", "label": "Video left, text right"}
      ],
      "default": "text_left"
    },
    {
      "type": "range",
      "id": "column_gap",
      "min": 20,
      "max": 100,
      "step": 10,
      "unit": "px",
      "label": "Column gap",
      "default": 40
    },
    {
      "type": "header",
      "content": "Video"
    },
    {
      "type": "url",
      "id": "video_file",
      "label": "Video file URL"
    },
    {
      "type": "checkbox",
      "id": "autoplay",
      "label": "Autoplay video",
      "default": false
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
      "default": true
    },
    {
      "type": "checkbox",
      "id": "controls",
      "label": "Show video controls",
      "default": true
    },
    {
      "type": "header",
      "content": "Text Content"
    },
    {
      "type": "richtext",
      "id": "text_content",
      "label": "Text content",
      "default": "<h2>Your heading here</h2><p>Add your text content here.</p>"
    },
    {
      "type": "range",
      "id": "text_size",
      "min": 12,
      "max": 24,
      "step": 1,
      "unit": "px",
      "label": "Text size",
      "default": 16
    },
    {
      "type": "color",
      "id": "text_color",
      "label": "Text color",
      "default": "#333333"
    },
    {
      "type": "header",
      "content": "Mobile"
    },
    {
      "type": "range",
      "id": "mobile_gap",
      "min": 10,
      "max": 50,
      "step": 5,
      "unit": "px",
      "label": "Mobile gap",
      "default": 20
    },
    {
      "type": "range",
      "id": "mobile_text_size",
      "min": 12,
      "max": 20,
      "step": 1,
      "unit": "px",
      "label": "Mobile text size",
      "default": 14
    }
  ],
  "presets": [
    {
      "name": "Video and Text"
    }
  ]
}
```

---

## Block Development Template

Here's a complete template for creating professional blocks:

```liquid
{% doc %}
  @prompt
    [Describe what this block does and its purpose]
{% enddoc %}

{% comment %} Generate unique ID for scoped CSS {% endcomment %}
{% assign block_id = block.id | replace: '_', '' | downcase %}

{% style %}
  .my-block-{{ block_id }} {
    /* Base styles with dynamic values */
    display: {{ block.settings.display_type | default: 'block' }};
    padding: {{ block.settings.padding | default: 20 }}px;
    background: {{ block.settings.bg_color | default: 'transparent' }};
    color: {{ block.settings.text_color | default: '#333' }};
  }

  /* Child elements */
  .my-block__element-{{ block_id }} {
    /* Element-specific styles */
  }

  /* Conditional styles */
  {% if block.settings.style == 'modern' %}
    .my-block-{{ block_id }} {
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
  {% endif %}

  /* Responsive behavior */
  @media screen and (max-width: 749px) {
    .my-block-{{ block_id }} {
      padding: {{ block.settings.mobile_padding | default: 15 }}px;
      font-size: {{ block.settings.mobile_font_size | default: 14 }}px;
    }
  }
{% endstyle %}

<div 
  class="my-block-{{ block_id }}"
  {{ block.shopify_attributes }}
>
  {% if block.settings.main_content != blank %}
    <div class="my-block__content-{{ block_id }}">
      {{ block.settings.main_content }}
    </div>
  {% else %}
    <!-- Helpful placeholder -->
    <div class="my-block__placeholder-{{ block_id }}">
      <p>Add your content here</p>
    </div>
  {% endif %}

  {% if block.settings.show_secondary %}
    <div class="my-block__secondary-{{ block_id }}">
      {{ block.settings.secondary_content }}
    </div>
  {% endif %}
</div>

{% schema %}
{
  "name": "My Custom Block",
  "settings": [
    {
      "type": "header",
      "content": "Content"
    },
    {
      "type": "richtext",
      "id": "main_content",
      "label": "Main Content",
      "default": "<h3>Block Title</h3><p>Block description goes here.</p>"
    },
    {
      "type": "checkbox",
      "id": "show_secondary",
      "label": "Show secondary content",
      "default": false
    },
    {
      "type": "textarea",
      "id": "secondary_content", 
      "label": "Secondary Content"
    },
    {
      "type": "header",
      "content": "Styling"
    },
    {
      "type": "select",
      "id": "style",
      "label": "Style",
      "options": [
        {"value": "simple", "label": "Simple"},
        {"value": "modern", "label": "Modern"},
        {"value": "minimal", "label": "Minimal"}
      ],
      "default": "simple"
    },
    {
      "type": "range",
      "id": "padding",
      "min": 10,
      "max": 60,
      "step": 5,
      "unit": "px",
      "label": "Padding",
      "default": 20
    },
    {
      "type": "color",
      "id": "bg_color",
      "label": "Background Color",
      "default": "#ffffff"
    },
    {
      "type": "color",
      "id": "text_color",
      "label": "Text Color", 
      "default": "#333333"
    },
    {
      "type": "header",
      "content": "Mobile Settings"
    },
    {
      "type": "range",
      "id": "mobile_padding",
      "min": 5,
      "max": 40,
      "step": 5,
      "unit": "px",
      "label": "Mobile Padding",
      "default": 15
    }
  ],
  "presets": [
    {
      "name": "My Custom Block"
    }
  ]
}
{% endschema %}
```

---

## Advanced Block Techniques

### 1. Multi-Type Blocks

Handle multiple block types in one section:

```liquid
{% for block in section.blocks %}
  {% case block.type %}
    {% when 'heading' %}
      <h2 {{ block.shopify_attributes }}>{{ block.settings.text }}</h2>
    
    {% when 'paragraph' %}
      <p {{ block.shopify_attributes }}>{{ block.settings.content }}</p>
    
    {% when 'image' %}
      <img src="{{ block.settings.image | image_url }}" {{ block.shopify_attributes }}>
    
    {% when 'button' %}
      <a href="{{ block.settings.url }}" class="btn" {{ block.shopify_attributes }}>
        {{ block.settings.label }}
      </a>
  {% endcase %}
{% endfor %}
```

### 2. Block Validation

Check for required content:

```liquid
{% for block in section.blocks %}
  {% case block.type %}
    {% when 'testimonial' %}
      {% if block.settings.quote != blank and block.settings.author != blank %}
        <!-- Render testimonial -->
      {% else %}
        <div class="block-error" {{ block.shopify_attributes }}>
          <p>⚠️ Please add both quote and author name</p>
        </div>
      {% endif %}
  {% endcase %}
{% endfor %}
```

### 3. Block Counter & Styling

Apply different styles based on position:

```liquid
{% for block in section.blocks %}
  {% assign block_index = forloop.index %}
  {% assign is_even = block_index | modulo: 2 %}
  
  <div class="block {% if is_even == 0 %}block--even{% else %}block--odd{% endif %}"
       {{ block.shopify_attributes }}>
    <span class="block-number">{{ block_index }}</span>
    <!-- Block content -->
  </div>
{% endfor %}
```

### 4. Conditional Block Display

Show/hide blocks based on settings:

```liquid
{% if section.settings.show_blocks %}
  {% for block in section.blocks %}
    {% unless block.settings.hide_block %}
      <!-- Render block -->
    {% endunless %}
  {% endfor %}
{% endif %}
```

---

## Block Best Practices

### ✅ Do This

1. **Always include `{{ block.shopify_attributes }}`** - Required for theme editor
2. **Use unique CSS classes** with block IDs to prevent conflicts
3. **Provide meaningful fallbacks** when content is empty
4. **Group related settings** with headers in schema
5. **Include helpful presets** with sample content
6. **Test with multiple blocks** to ensure proper styling

### ❌ Avoid This

1. **Generic CSS classes** that might conflict with theme styles
2. **Missing `shopify_attributes`** - breaks theme editor functionality
3. **No fallback content** - creates confusing empty blocks
4. **Too many settings** - overwhelming for merchants
5. **Hard-coded values** - always use settings for customization
6. **No mobile considerations** - blocks must work on all screen sizes

---

## Block Schema Reference

### Essential Settings Types

```json
{
  "type": "text",         // Short text input
  "type": "textarea",     // Multi-line text
  "type": "richtext",     // Formatted text with HTML
  "type": "image_picker", // Image selection
  "type": "video",        // Video file upload
  "type": "url",          // Link input
  "type": "select",       // Dropdown options
  "type": "checkbox",     // True/false toggle
  "type": "range",        // Slider for numbers
  "type": "color",        // Color picker
  "type": "font_picker"   // Font selection
}
```

### Block-Specific Properties

```json
{
  "blocks": [
    {
      "type": "my_block",           // Unique identifier
      "name": "My Block",           // Display name
      "limit": 3,                  // Max instances (optional)
      "settings": [...]            // Block settings
    }
  ],
  "max_blocks": 10                // Total blocks allowed
}
```

---

## Common Block Patterns

### Content Block
```liquid
{% for block in section.blocks %}
  {% case block.type %}
    {% when 'content' %}
      <div class="content-block" {{ block.shopify_attributes }}>
        {% if block.settings.heading %}
          <h3>{{ block.settings.heading }}</h3>
        {% endif %}
        {{ block.settings.content }}
      </div>
  {% endcase %}
{% endfor %}
```

### Image Block
```liquid
{% when 'image' %}
  <div class="image-block" {{ block.shopify_attributes }}>
    {% if block.settings.image %}
      <img src="{{ block.settings.image | image_url: width: 600 }}" 
           alt="{{ block.settings.image.alt | escape }}">
    {% endif %}
    {% if block.settings.caption %}
      <p class="caption">{{ block.settings.caption }}</p>
    {% endif %}
  </div>
```

### Feature Block
```liquid
{% when 'feature' %}
  <div class="feature-block" {{ block.shopify_attributes }}>
    {% if block.settings.icon %}
      <div class="feature-icon">
        <img src="{{ block.settings.icon | image_url: width: 80 }}" alt="">
      </div>
    {% endif %}
    <div class="feature-content">
      <h4>{{ block.settings.title }}</h4>
      <p>{{ block.settings.description }}</p>
    </div>
  </div>
```

---

## Advanced: AI-Generated Block Documentation

For teams using AI tools, document blocks like this:

```liquid
{% doc %}
  @prompt
    Create a testimonial block that displays:
    - Customer quote with quotation marks
    - Star rating (1-5 stars)  
    - Customer name and company
    - Optional customer photo
    - Configurable text colors and sizes
    
  @responsive
    - Stack vertically on mobile
    - Reduce font sizes for small screens
    
  @accessibility  
    - Proper alt text for images
    - Semantic HTML structure
    - Good color contrast
{% enddoc %}
```

This documentation helps with:
- **Team collaboration** - Clear requirements
- **AI regeneration** - Consistent output  
- **Maintenance** - Understanding original intent
- **Testing** - Complete feature coverage

---

## Next Steps

Ready to build more complex sections? Check out:

- **[Liquid Syntax for Sections](./04-liquid-syntax.md)** - Template code patterns
- **[Code Examples & Patterns](./05-code-examples.md)** - Working block examples
- **[Best Practices & Performance](./06-best-practices.md)** - Optimization techniques

Blocks are the building blocks of flexible, merchant-friendly Shopify sections! 🚀
