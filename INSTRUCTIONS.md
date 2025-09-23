# 🚀 Complete Shopify Liquid Component Builder

**The definitive step-by-step program for building production-ready Shopify Liquid components with automated validation, MCP integration, and comprehensive quality assurance.**

---

## 🎯 **QUICK START: What Type of Component Are You Building?**

**Select your path and follow the step-by-step instructions:**

| Component Type | Click to Jump | Use Case |
|----------------|---------------|----------|
| **🏗️ [Section](#building-sections)** | Complete page sections | Hero banners, product grids, feature areas |
| **🧱 [Theme Block](#building-theme-blocks)** | Reusable components | Feature items, testimonials, product cards |
| **📦 [Snippet](#building-snippets)** | Utility functions | Image handlers, price formatters, utilities |
| **🎨 [CSS Pattern](#building-css-patterns)** | Design systems | Scoped styles, responsive patterns, tokens |
| **📄 [Layout](#building-layouts)** | Theme foundations | theme.liquid, checkout.liquid |
| **📋 [Template](#building-templates)** | Page templates | Product pages, collection pages, custom templates |

---

## 🛡️ **CRITICAL: Pre-Development Setup**

### **Step 0: Validation Environment Ready**

**MANDATORY: Run this command before starting any development:**

```bash
# Ensure your validation environment is working
./scripts/validate-theme.sh development
```

**This validates:**
- ✅ Ultimate Liquid validator is functional
- ✅ Theme Check configuration is active
- ✅ Schema validation rules are loaded
- ✅ Character encoding validation is ready
- ✅ MCP server integration is available
- ✅ Comprehensive syntax validation is ready

**If this fails, stop and fix the validation setup first.**

### **🚨 Critical: Common Issues to Avoid**

**Based on recent validation fixes, always check for these issues:**

#### **Liquid Syntax Issues**
```liquid
❌ WRONG: {% doc %} content {% enddoc %}           <!-- Invalid tags -->
✅ CORRECT: {% comment %} content {% endcomment %} <!-- Use comment tags -->

❌ WRONG: {%- liquid ... -%}                       <!-- Invalid liquid block ending -->
✅ CORRECT: {% liquid ... %}                       <!-- Proper liquid block syntax -->
```

#### **Unknown Shopify Filters**
```liquid
❌ WRONG: {{ image | image_tag }}                  <!-- image_tag doesn't exist -->
✅ CORRECT: {{ image | image_url }}                <!-- Use image_url -->

❌ WRONG: {{ form | payment_button_tag }}          <!-- payment_button_tag doesn't exist -->
✅ CORRECT: {{ form | payment_button }}            <!-- Use payment_button -->
```

#### **Performance Issues**
```liquid
❌ WRONG: {% for collection in collections %}      <!-- Can break themes -->
✅ CORRECT: {% for collection in collections limit: 50 %} <!-- Always limit -->
```

#### **Translation Keys**
Always add required translation keys to `locales/en.default.json`:
```json
{
  "general": {
    "search": {
      "placeholder": "Search",
      "submit": "Search"
    }
  }
}
```

**💡 TIP: Run `./scripts/fix-liquid-syntax.py` to automatically fix common issues.**

### **Step 1: Understand File Type Detection**

Our system automatically detects what type of file you're creating based on:

```
📁 File Structure & Auto-Detection:
├── sections/           ➜ Detects as 'section'
├── blocks/            ➜ Detects as 'theme_block'
├── snippets/          ➜ Detects as 'snippet'
├── layout/            ➜ Detects as 'layout'
├── templates/         ➜ Detects as 'template_liquid' or 'template_json'
├── assets/            ➜ Detects as 'asset'
├── config/            ➜ Detects as 'config'
└── locales/           ➜ Detects as 'locale'
```

**Our validation system automatically applies the correct validation rules based on file location.**

### **Step 2: Documentation References**

**CRITICAL: Review these before coding:**

| Documentation | Purpose | Link |
|---------------|---------|------|
| **Schema Guidelines** | Prevent validation errors | `shopify-liquid-guides/schema-validation/schema-guidelines.md` |
| **Character Encoding Research** | Upload failure prevention | `shopify-liquid-guides/docs/research/illegal-characters/` |
| **Design System** | Component tokens & patterns | `shopify-liquid-guides/docs/architecture/design-system-implementation.md` |
| **File Type Matrix** | Official validation rules | `shopify-liquid-guides/docs/validation/SHOPIFY_FILE_TYPE_VALIDATION_MATRIX.md` |
| **MCP Integration** | Enhanced validation & API access | `shopify-liquid-guides/docs/development/SHOPIFY-MCP-SETUP.md` |
| **Validation Architecture** | Understanding our validator improvements | `shopify-liquid-guides/docs/validation/VALIDATOR_ARCHITECTURE_IMPROVEMENTS.md` |

---

# 🏗️ Building Sections

**Sections are complete page components that appear in the theme editor.**

## **Section Creation Workflow**

### **Step 1: Planning & Research**

```bash
# Start with MCP-enhanced research (if using AI assistant)
# Use these MCP tools for comprehensive planning:
# - learn_shopify_api(api: "liquid") for Liquid documentation
# - search_docs_chunks for specific section examples
# - introspect_graphql_schema for any API requirements

# Traditional validation check
./scripts/validate-theme.sh development
```

**Questions to Answer:**
- What is the section's primary purpose?
- What content will merchants customize?
- Does it need blocks for dynamic content?
- What responsive behavior is required?

### **Step 2: Schema Design & Validation**

**CRITICAL: Design schema first with validation rules**

```bash
# Reference our comprehensive schema validation
cat shopify-liquid-guides/schema-validation/schema-guidelines.md
```

**Key Validation Rules:**
- Range step calculation: `(max - min) / step ≤ 101`
- Use `video` not `file` for video uploads
- No `enabled_on` in sections (app blocks only)
- Step values must be ≥ 0.1
- All setting IDs must be unique

### **Step 3: Create Section File**

**Location:** `shopify-liquid-guides/code-library/sections/section-name.liquid`

**Template Structure:**
```liquid
{% comment %} sections/section-name.liquid {% endcomment %}
{%- assign unique = section.id | replace: '_', '' | downcase -%}

{% style %}
  .section-name-{{ unique }} {
    /* ✅ Design token integration */
    --component-bg: var(--surface-primary);
    --component-text: var(--text-primary);
    --component-spacing: var(--spacing-component-md);

    /* ✅ Dynamic values from Shopify settings */
    --dynamic-bg: {{ section.settings.bg_color | default: 'var(--component-bg)' }};
    --dynamic-text: {{ section.settings.text_color | default: 'var(--component-text)' }};

    /* Apply design tokens */
    background: var(--dynamic-bg);
    color: var(--dynamic-text);
    padding: var(--component-spacing);
    border-radius: var(--border-radius-lg);
  }

  .section-name__element-{{ unique }} {
    font-size: var(--font-size-base);
    line-height: var(--line-height-normal);
    margin-bottom: var(--spacing-component-sm);
  }

  /* Focus states using design tokens */
  .section-name-{{ unique }}:focus-within {
    outline: var(--focus-ring-width) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  /* Responsive using token system */
  @media (max-width: 749px) {
    .section-name-{{ unique }} {
      padding: var(--spacing-component-sm);
    }
  }
{% endstyle %}

<section class="section-name-{{ unique }}"
         role="region"
         aria-label="{{ section.settings.aria_label | default: section.settings.heading | default: 'Section content' | escape }}">

  {% if section.settings.heading != blank %}
    <h2 class="section-name__heading-{{ unique }}">{{ section.settings.heading | escape }}</h2>
  {% endif %}

  {% if section.settings.content != blank %}
    <div class="section-name__content-{{ unique }}">{{ section.settings.content }}</div>
  {% endif %}

  {% if section.blocks.size > 0 %}
    <div class="section-name__blocks-{{ unique }}">
      {% for block in section.blocks %}
        {% case block.type %}
          {% when 'text_block' %}
            <div class="section-name__block-{{ unique }}" {{ block.shopify_attributes }}>
              <h3>{{ block.settings.heading | escape }}</h3>
              <p>{{ block.settings.text | escape }}</p>
            </div>
        {% endcase %}
      {% endfor %}
    </div>
  {% endif %}

</section>

{% schema %}
{
  "name": "Section Name",
  "settings": [
    {
      "type": "header",
      "content": "Content"
    },
    {
      "type": "text",
      "id": "heading",
      "label": "Section heading",
      "default": "Welcome to our section"
    },
    {
      "type": "richtext",
      "id": "content",
      "label": "Section content",
      "info": "Add rich text content for your section"
    },
    {
      "type": "text",
      "id": "aria_label",
      "label": "Accessibility label",
      "info": "Screen reader description for this section"
    },
    {
      "type": "header",
      "content": "Design Tokens"
    },
    {
      "type": "color",
      "id": "bg_color",
      "label": "Background Color",
      "info": "Uses --surface-primary design token as fallback"
    },
    {
      "type": "color",
      "id": "text_color",
      "label": "Text Color",
      "info": "Uses --text-primary design token as fallback"
    }
  ],
  "blocks": [
    {
      "type": "text_block",
      "name": "Text Block",
      "settings": [
        {
          "type": "text",
          "id": "heading",
          "label": "Block heading",
          "default": "Feature title"
        },
        {
          "type": "textarea",
          "id": "text",
          "label": "Block text",
          "default": "Feature description"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Section Name",
      "blocks": [
        {
          "type": "text_block"
        }
      ]
    }
  ]
}
{% endschema %}
```

### **Step 4: Comprehensive Validation**

**Run the complete validation workflow:**

```bash
# 1. Quick development validation
./scripts/validate-theme.sh development

# 2. Auto-fix any simple issues
./scripts/validate-theme.sh auto-fix

# 3. Comprehensive syntax validation
./scripts/validate-theme.sh syntax

# 4. Complete validation suite
./scripts/validate-theme.sh comprehensive

# 5. Production readiness check
./scripts/validate-theme.sh production
```

**What Gets Validated:**
- ✅ Liquid syntax validation (tag pairing, filter validation)
- ✅ Schema JSON validation (no syntax errors)
- ✅ Range step calculations (automated)
- ✅ Design token integration (CSS pattern validation)
- ✅ Accessibility compliance (ARIA, semantic HTML)
- ✅ Performance patterns (responsive images, CSS optimization)
- ✅ Theme Store compliance (all submission requirements)

### **Step 5: Quality Assurance Checklist**

**Manual verification after automated validation passes:**

- [ ] **Design System Integration**
  - [ ] Uses semantic design tokens, not primitive values
  - [ ] Shopify settings provide token fallbacks
  - [ ] Focus states implemented with design tokens
  - [ ] Responsive behavior uses token system

- [ ] **Content & Accessibility**
  - [ ] All user content is escaped (`| escape`)
  - [ ] Semantic HTML structure with proper roles
  - [ ] Logical heading hierarchy (h2 → h3 → h4)
  - [ ] Meaningful ARIA labels and descriptions

- [ ] **Performance & Compliance**
  - [ ] Responsive images with srcset and sizes
  - [ ] Lazy loading implemented where appropriate
  - [ ] CSS scoped with unique IDs
  - [ ] No hardcoded values (uses settings/tokens)

---

# 🧱 Building Theme Blocks

**Theme blocks are standalone reusable components that can be used across multiple sections.**

## **Theme Block Creation Workflow**

### **Step 1: Research & Planning**

```bash
# Enhanced research with MCP integration
# Use MCP tools for block development:
# - search_docs_chunks("theme blocks") for official documentation
# - learn_shopify_api(api: "liquid") for block-specific Liquid features
# - validate_theme for real-time validation during development

# Standard validation check
./scripts/validate-theme.sh development
```

**Key Considerations for Theme Blocks:**
- **Reusability**: Can be used in multiple sections
- **Self-contained**: Has its own schema and styling
- **Hierarchical**: Can contain other blocks
- **Saveable**: Merchants can save as custom blocks

### **Step 2: Create Theme Block File**

**Location:** `shopify-liquid-guides/code-library/blocks/block-component-name.liquid`

**Template Structure:**
```liquid
{% comment %} blocks/block-component-name.liquid {% endcomment %}
{%- assign u = block.id | replace: '_', '' | downcase -%}

{% style %}
  .block-name-{{ u }} {
    /* ✅ Component tokens with semantic fallbacks */
    --block-bg: var(--surface-secondary);
    --block-text: var(--text-primary);
    --block-spacing: var(--spacing-component-sm);
    --block-radius: var(--border-radius-md);

    /* ✅ Dynamic values from block settings */
    --dynamic-bg: {{ block.settings.bg_color | default: 'var(--block-bg)' }};
    --dynamic-text: {{ block.settings.text_color | default: 'var(--block-text)' }};

    /* Apply design tokens */
    background: var(--dynamic-bg);
    color: var(--dynamic-text);
    padding: var(--block-spacing);
    border-radius: var(--block-radius);
    box-shadow: var(--shadow-xs);
    transition: var(--transition-base);
  }

  .block-name__element-{{ u }} {
    font-size: var(--font-size-sm);
    line-height: var(--line-height-normal);
    margin-bottom: var(--spacing-component-xs);
  }

  /* Hover states using design tokens */
  .block-name-{{ u }}:hover {
    box-shadow: var(--shadow-sm);
    transform: translateY(-1px);
  }

  /* Focus states */
  .block-name-{{ u }}:focus-within {
    outline: var(--focus-ring-width) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }
{% endstyle %}

<div class="block-name-{{ u }}" {{ block.shopify_attributes }}>
  {% if block.settings.heading != blank %}
    <h3 class="block-name__heading-{{ u }}">{{ block.settings.heading | escape }}</h3>
  {% endif %}

  {% if block.settings.content != blank %}
    <div class="block-name__content-{{ u }}">{{ block.settings.content | escape }}</div>
  {% endif %}

  {% if block.settings.link_url != blank and block.settings.link_text != blank %}
    <a href="{{ block.settings.link_url }}"
       class="block-name__link-{{ u }}"
       aria-label="{{ block.settings.link_text | escape }}">
      {{ block.settings.link_text | escape }}
    </a>
  {% endif %}
</div>

{% schema %}
{
  "name": "Block Name",
  "settings": [
    {
      "type": "header",
      "content": "Content"
    },
    {
      "type": "text",
      "id": "heading",
      "label": "Block heading",
      "default": "Feature Title"
    },
    {
      "type": "textarea",
      "id": "content",
      "label": "Block content",
      "default": "Add your feature description here."
    },
    {
      "type": "url",
      "id": "link_url",
      "label": "Link URL"
    },
    {
      "type": "text",
      "id": "link_text",
      "label": "Link text",
      "default": "Learn more"
    },
    {
      "type": "header",
      "content": "Design Tokens"
    },
    {
      "type": "color",
      "id": "bg_color",
      "label": "Background Color",
      "info": "Uses --surface-secondary design token as fallback"
    },
    {
      "type": "color",
      "id": "text_color",
      "label": "Text Color",
      "info": "Uses --text-primary design token as fallback"
    }
  ],
  "presets": [
    {
      "name": "Block Name",
      "settings": {
        "heading": "Feature Title",
        "content": "Add your feature description here.",
        "link_text": "Learn more"
      }
    }
  ]
}
{% endschema %}
```

### **Step 3: Validation & Testing**

```bash
# Complete validation workflow for theme blocks
./scripts/validate-theme.sh development
./scripts/validate-theme.sh syntax
./scripts/validate-theme.sh comprehensive
```

**Theme Block Specific Validation:**
- ✅ Block schema validation (proper structure)
- ✅ Shopify attributes implementation (`{{ block.shopify_attributes }}`)
- ✅ Unique ID scoping for CSS
- ✅ Reusability across different contexts

---

# 📦 Building Snippets

**Snippets are utility functions that provide reusable functionality across the theme.**

## **Snippet Creation Workflow**

### **Step 1: Define Snippet Purpose**

```bash
# Enhanced planning with MCP
# Use MCP for snippet research:
# - search_docs_chunks("liquid snippets") for best practices
# - fetch_full_docs for comprehensive Liquid reference

./scripts/validate-theme.sh development
```

**Common Snippet Types:**
- **Utility Functions**: Image handling, price formatting, date formatting
- **Component Helpers**: Responsive images, icon rendering, social media
- **Content Processors**: Rich text handling, link generation, metadata

### **Step 2: Create Snippet File**

**Location:** `shopify-liquid-guides/code-library/snippets/snippet-name.liquid`

**Template Structure:**
```liquid
{% comment %}
  Snippet: snippet-name
  Usage: {% render 'snippet-name', param1: value1, param2: value2, unique_id: 'component-123' %}

  Parameters:
  - param1 (required): Description of parameter
  - param2 (optional): Description with default value
  - unique_id (required): Unique ID for scoped styling
  - bg_color (optional): Background color override
  - text_color (optional): Text color override

  Design Token Integration:
  - Uses semantic tokens with component-specific fallbacks
  - Supports color customization through parameters
  - Maintains consistent spacing and typography

  Example:
  {% render 'snippet-name',
     param1: 'value',
     unique_id: section.id,
     bg_color: section.settings.bg_color %}
{% endcomment %}

{%- liquid
  assign param1 = param1 | default: 'default_value'
  assign param2 = param2 | default: 'default_value'
  assign unique_id = unique_id | default: 'snippet-default'
  assign bg_color = bg_color | default: 'var(--surface-primary)'
  assign text_color = text_color | default: 'var(--text-primary)'
-%}

{% style %}
  .snippet-name-{{ unique_id }} {
    /* ✅ Design token integration for reusable snippets */
    --snippet-bg: {{ bg_color }};
    --snippet-text: {{ text_color }};
    --snippet-spacing: var(--spacing-component-sm);
    --snippet-radius: var(--border-radius-sm);

    background: var(--snippet-bg);
    color: var(--snippet-text);
    padding: var(--snippet-spacing);
    border-radius: var(--snippet-radius);
    font-size: var(--font-size-sm);
    line-height: var(--line-height-normal);
  }

  .snippet-name__element-{{ unique_id }} {
    margin-bottom: var(--spacing-component-xs);
  }
{% endstyle %}

<div class="snippet-name-{{ unique_id }}">
  <!-- Snippet functionality with design token styling -->
  {% if param1 != blank %}
    <div class="snippet-name__element-{{ unique_id }}">
      {{ param1 | escape }}
    </div>
  {% endif %}
</div>
```

### **Step 3: Snippet Validation**

```bash
# Snippet-specific validation
./scripts/validate-theme.sh development
./scripts/validate-theme.sh syntax
```

**Snippet Validation Focuses On:**
- ✅ Parameter validation and default handling
- ✅ Liquid syntax in reusable context
- ✅ Design token integration
- ✅ CSS scoping with dynamic unique IDs

---

# 🎨 Building CSS Patterns

**CSS patterns provide reusable styling methodologies and design system implementations.**

## **CSS Pattern Creation Workflow**

### **Step 1: Pattern Design**

```bash
./scripts/validate-theme.sh development
```

**Pattern Categories:**
- **Component Patterns**: Button styles, card layouts, form elements
- **Layout Patterns**: Grid systems, flexbox utilities, spacing
- **Token Patterns**: Design token implementations, theme variables
- **Responsive Patterns**: Breakpoint management, fluid typography

### **Step 2: Create CSS Pattern File**

**Location:** `shopify-liquid-guides/code-library/css-patterns/pattern-name.css`

**Template Structure:**
```css
/* CSS Pattern: pattern-name.css */
/*
   Purpose: Description of the pattern and its use cases
   Usage: How to apply this pattern in Liquid files
   Dependencies: Any required design tokens or base styles

   Design Token Integration:
   - Uses semantic design tokens for consistency
   - Provides component-level token abstractions
   - Maintains responsive behavior through token system
*/

/* ✅ Component Token Definitions */
:root {
  --pattern-bg: var(--surface-primary);
  --pattern-text: var(--text-primary);
  --pattern-border: var(--border-primary);
  --pattern-spacing: var(--spacing-component-md);
  --pattern-radius: var(--border-radius-lg);
}

/* ✅ Base Pattern Styles */
.pattern-base {
  background: var(--pattern-bg);
  color: var(--pattern-text);
  border: 1px solid var(--pattern-border);
  padding: var(--pattern-spacing);
  border-radius: var(--pattern-radius);
  box-shadow: var(--shadow-sm);
}

/* ✅ Pattern Variations */
.pattern-base--large {
  padding: var(--spacing-component-lg);
  font-size: var(--font-size-lg);
}

.pattern-base--small {
  padding: var(--spacing-component-sm);
  font-size: var(--font-size-sm);
}

/* ✅ Responsive Pattern Behavior */
@media (max-width: 749px) {
  .pattern-base {
    padding: var(--spacing-component-sm);
  }
}

/* ✅ Interactive States */
.pattern-base:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
  transition: var(--transition-base);
}

.pattern-base:focus-within {
  outline: var(--focus-ring-width) solid var(--focus-ring-color);
  outline-offset: var(--focus-ring-offset);
}

/* ✅ Pattern Component Integration */
.pattern-base__element {
  margin-bottom: var(--spacing-component-sm);
  color: var(--pattern-text);
}

.pattern-base__title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-tight);
  margin-bottom: var(--spacing-component-xs);
}

.pattern-base__content {
  font-size: var(--font-size-base);
  line-height: var(--line-height-normal);
}
```

### **Step 3: CSS Pattern Validation**

```bash
# CSS-specific validation
./scripts/validate-theme.sh development
./scripts/validate-theme.sh comprehensive
```

**CSS Pattern Validation:**
- ✅ Design token usage validation
- ✅ CSS syntax and structure
- ✅ Responsive pattern compliance
- ✅ Accessibility (focus states, color contrast)

---

# 📄 Building Layouts

**Layouts provide the foundational HTML structure for theme pages.**

## **Layout Creation Workflow**

### **Step 1: Layout Planning**

```bash
# Enhanced layout research with MCP
# Use MCP for layout documentation:
# - search_docs_chunks("theme layouts") for structure requirements
# - fetch_full_docs("/docs/api/liquid/objects/layout") for layout objects

./scripts/validate-theme.sh development
```

### **Step 2: Create Layout File**

**Location:** `shopify-liquid-guides/code-library/layouts/layout-name.liquid`

**Required Elements for Layouts:**
- `{{ content_for_header }}` (required)
- `{{ content_for_layout }}` (required)
- Proper DOCTYPE and HTML structure
- Meta tags and SEO elements

**Template Structure:**
```liquid
{% comment %} layouts/layout-name.liquid {% endcomment %}
<!DOCTYPE html>
<html lang="{{ request.locale.iso_code }}" dir="{{ settings.text_direction }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>
    {% if page_title != blank %}{{ page_title }} - {% endif %}{{ shop.name }}
  </title>

  {% if page_description %}
    <meta name="description" content="{{ page_description | escape }}">
  {% endif %}

  <link rel="canonical" href="{{ canonical_url }}">

  <link rel="preconnect" href="https://cdn.shopify.com" crossorigin>
  <link rel="preconnect" href="https://fonts.shopifycdn.com" crossorigin>

  <!-- ✅ REQUIRED: content_for_header -->
  {{ content_for_header }}

  <!-- Design System CSS -->
  {{ 'design-tokens.css' | asset_url | stylesheet_tag }}
  {{ 'base.css' | asset_url | stylesheet_tag }}
</head>

<body class="layout-{{ template.name }}">
  <!-- Skip to content link for accessibility -->
  <a href="#main-content" class="skip-link">Skip to content</a>

  <!-- Header -->
  {% section 'header' %}

  <!-- Main content area -->
  <main id="main-content" role="main">
    {{ content_for_layout }}
  </main>

  <!-- Footer -->
  {% section 'footer' %}

  <!-- Global JavaScript -->
  {{ 'global.js' | asset_url | script_tag }}
</body>
</html>
```

### **Step 3: Layout Validation**

```bash
./scripts/validate-theme.sh development
./scripts/validate-theme.sh production
```

**Layout-Specific Validation:**
- ✅ Required layout objects present
- ✅ Valid HTML structure
- ✅ Accessibility compliance (skip links, semantic HTML)
- ✅ Performance optimization (preconnect, asset loading)

---

# 📋 Building Templates

**Templates define the structure and content for specific page types.**

## **Template Creation Workflow**

### **Step 1: Template Type Selection**

```bash
# Enhanced template research
# Use MCP for template documentation:
# - search_docs_chunks("shopify templates") for template types
# - introspect_graphql_schema for data available to templates

./scripts/validate-theme.sh development
```

**Template Types:**
- **JSON Templates**: Merchant-customizable with sections
- **Liquid Templates**: Custom logic and structure
- **Metaobject Templates**: Custom content types

### **Step 2: Create Template File**

**For JSON Templates:**
**Location:** `shopify-liquid-guides/examples/template-name.json`

```json
{
  "sections": {
    "header": {
      "type": "header"
    },
    "main": {
      "type": "main-product",
      "settings": {
        "enable_sticky_info": true,
        "enable_video_looping": false
      }
    },
    "product-recommendations": {
      "type": "product-recommendations",
      "settings": {
        "heading": "You may also like",
        "products_to_show": 4
      }
    }
  },
  "order": ["header", "main", "product-recommendations"]
}
```

**For Liquid Templates:**
**Location:** `shopify-liquid-guides/code-library/templates/template-name.liquid`

```liquid
{% comment %} templates/template-name.liquid {% endcomment %}
{% layout 'theme' %}

<div class="template-page">
  {% if template.suffix == 'custom' %}
    <!-- Custom template logic -->
    {% section 'custom-hero' %}
  {% else %}
    <!-- Default template structure -->
    {% section 'page-header' %}
  {% endif %}

  <main class="main-content" role="main">
    {{ content_for_layout }}
  </main>
</div>
```

### **Step 3: Template Validation**

```bash
./scripts/validate-theme.sh development
./scripts/validate-theme.sh comprehensive
```

**Template Validation:**
- ✅ JSON syntax validation (for JSON templates)
- ✅ Section reference validation
- ✅ Template object usage validation
- ✅ Layout assignment validation

---

# 🔄 **Enhanced Validation with Shopify MCP Integration**

## **MCP-Enhanced Development Workflow**

**When working with AI assistants that support MCP, use these enhanced validation capabilities:**

### **Step 1: Initialize MCP Context**

```bash
# Traditional validation
./scripts/validate-theme.sh development

# Enhanced with MCP (AI assistants will use automatically):
# - learn_shopify_api(api: "liquid") for Liquid context
# - validate_theme for real-time theme validation
# - introspect_graphql_schema for API schema exploration
```

### **Step 2: Real-Time Development Validation**

**MCP Tools for Enhanced Development:**
- **`validate_theme`**: Comprehensive theme validation against live Shopify standards
- **`validate_graphql_codeblocks`**: Real-time GraphQL query validation
- **`search_docs_chunks`**: Direct access to official Shopify documentation
- **`introspect_graphql_schema`**: Live schema introspection for API development
- **`fetch_full_docs`**: Complete documentation page retrieval

### **Step 3: Documentation-Driven Development**

**MCP-Enhanced Research:**
```bash
# Traditional documentation reference
cat shopify-liquid-guides/schema-validation/schema-guidelines.md

# Enhanced with MCP (AI assistants use automatically):
# - search_docs_chunks("schema validation") for latest rules
# - fetch_full_docs("/docs/api/liquid/tags/schema") for complete reference
# - validate_graphql_codeblocks for API query validation
```

**📖 Complete MCP Setup: [SHOPIFY-MCP-SETUP.md](./shopify-liquid-guides/docs/development/SHOPIFY-MCP-SETUP.md)**

---

# ✅ **Quality Assurance & Final Validation**

## **Comprehensive Validation Workflow**

**Every component must pass this complete validation workflow:**

```bash
# 1. Development validation (fast, essential checks)
./scripts/validate-theme.sh development

# 2. Liquid syntax validation (comprehensive syntax checking)
./scripts/validate-theme.sh syntax

# 3. Auto-fix any correctable issues
./scripts/validate-theme.sh auto-fix

# 4. Deep validation (ultimate + integrity + syntax + comprehensive)
./scripts/validate-theme.sh deep

# 5. Production validation (Theme Store ready)
./scripts/validate-theme.sh production

# 6. Complete validation suite (all tests)
./scripts/validate-theme.sh all
```

## **Validation Capabilities**

**Our comprehensive validation system checks:**

### **Liquid Syntax Validation**
- ✅ Tag pairing validation ({% if %} ↔ {% endif %})
- ✅ Filter validation (60+ official Shopify filters)
- ✅ Object validation (official Shopify objects)
- ✅ Syntax error detection (unclosed tags, malformed expressions)

### **Character Encoding Validation**
- ✅ Cross-platform encoding compatibility (Windows/macOS/Linux)
- ✅ Upload failure prevention (BOM detection, control characters)
- ✅ Context separation validation (JavaScript/CSS/Liquid boundaries)
- ✅ Security character validation (XSS prevention, escape filters)
- ✅ Performance pattern detection (nested loops, excessive filters)
- ✅ Deprecated filter warnings (img_url → image_url)

### **Schema Validation**
- ✅ Range step calculations: `(max - min) / step ≤ 101`
- ✅ Valid setting types (video not file for uploads)
- ✅ JSON syntax validation (no trailing commas)
- ✅ Setting ID uniqueness validation
- ✅ Required property validation
- ✅ Schema placement validation

### **Design System Validation**
- ✅ Design token usage validation
- ✅ CSS scoping methodology compliance
- ✅ Component token integration
- ✅ Responsive pattern validation
- ✅ Focus state implementation

### **Accessibility Validation**
- ✅ Semantic HTML structure
- ✅ ARIA label and role validation
- ✅ Heading hierarchy validation
- ✅ Image alt text requirements
- ✅ Focus management validation

### **Performance Validation**
- ✅ Responsive image implementation
- ✅ Asset optimization validation
- ✅ CSS performance patterns
- ✅ JavaScript loading optimization
- ✅ Core Web Vitals compliance

### **Theme Store Compliance**
- ✅ All Theme Store requirements
- ✅ Security pattern validation
- ✅ Code quality standards
- ✅ Merchant experience validation
- ✅ Cross-browser compatibility

## **Manual Quality Checklist**

**After automated validation passes, verify:**

### **Code Quality Standards**
- [ ] Uses unique ID scoping pattern (`{{ unique }}` or `{{ u }}`)
- [ ] All user content is escaped with `| escape`
- [ ] Blank value checks for optional settings
- [ ] Responsive CSS with mobile-first approach
- [ ] CSS custom properties for dynamic values

### **Design System Integration**
- [ ] Uses semantic design tokens, not primitive values
- [ ] Shopify settings provide token fallbacks
- [ ] Focus states implemented with design tokens
- [ ] Responsive behavior uses token system
- [ ] Component follows unified design patterns

### **Content & Accessibility**
- [ ] Semantic HTML structure with proper roles
- [ ] Logical heading hierarchy (h2 → h3 → h4)
- [ ] Meaningful ARIA labels and descriptions
- [ ] Sufficient color contrast ratios
- [ ] Keyboard navigation support

### **Performance & Integration**
- [ ] Responsive images with srcset and sizes
- [ ] Lazy loading implemented appropriately
- [ ] CSS scoped with unique identifiers
- [ ] No hardcoded values (uses settings/tokens)
- [ ] Proper integration with existing components

---

# 📚 **Documentation & Reference Files**

## **Essential Documentation Structure**

Our documentation has been reorganized for optimal development workflow:

### **Core Development Files**
- **`INSTRUCTIONS.md`** (this file): Complete component builder program
- **`shopify-liquid-guides/schema-validation/schema-guidelines.md`**: Schema validation rules
- **`shopify-liquid-guides/docs/architecture/design-system-implementation.md`**: Design system guide

### **Enhanced Documentation Location**
- **`shopify-liquid-guides/docs/development/SHOPIFY-MCP-SETUP.md`**: Complete MCP integration guide
- **`shopify-liquid-guides/docs/validation/VALIDATOR_ARCHITECTURE_IMPROVEMENTS.md`**: Validator implementation details
- **`shopify-liquid-guides/docs/validation/SHOPIFY_FILE_TYPE_VALIDATION_MATRIX.md`**: Official validation reference

### **Code Library References**
- **`shopify-liquid-guides/code-library/`**: Production-ready component examples
- **`shopify-liquid-guides/examples/`**: Complete page templates and JSON examples
- **`shopify-liquid-guides/docs/`**: Comprehensive documentation for all file types

### **Validation Configuration**
- **`.theme-check.yml`**: Ultimate validation configuration
- **`.theme-check-development.yml`**: Fast development validation
- **`.theme-check-production.yml`**: Theme Store submission validation

---

# 🎯 **Summary: Your Development Workflow**

## **Perfect Component Creation Process**

**When building any Shopify Liquid component, follow this exact workflow:**

### **1. 🚀 Pre-Development (MANDATORY)**
```bash
./scripts/validate-theme.sh development  # Ensure clean environment
```

### **2. 🎯 Component Planning**
- Identify component type (section, block, snippet, CSS, layout, template)
- Review relevant documentation section above
- Plan schema structure with validation rules
- Consider design token integration

### **3. 🏗️ Component Creation**
- Use appropriate file location and naming
- Follow exact template structure for component type
- Integrate design token system throughout
- Implement accessibility requirements
- Apply performance best practices

### **4. 🛡️ Comprehensive Validation**
```bash
./scripts/validate-theme.sh development  # Quick check
./scripts/validate-theme.sh syntax       # Liquid syntax validation
./scripts/validate-theme.sh auto-fix     # Fix correctable issues
./scripts/validate-theme.sh production   # Final validation
```

### **5. ✅ Quality Assurance**
- Complete manual quality checklist
- Verify design system integration
- Test component in theme editor
- Validate responsive behavior

### **6. 🎉 Component Ready**
- Component passes all validation levels
- Follows unified design system
- Meets Theme Store compliance
- Ready for production deployment

---

## **🛡️ Zero-Tolerance Quality Philosophy**

**Our validation system implements a zero-tolerance approach to quality:**

- **❌ No syntax errors**: Comprehensive Liquid syntax validation catches all issues
- **❌ No schema violations**: Automated schema validation prevents "Invalid schema" errors
- **❌ No accessibility gaps**: WCAG 2.1 AA compliance validation built-in
- **❌ No performance issues**: Core Web Vitals and optimization validation
- **❌ No Theme Store rejections**: 100% compliance validation guaranteed

**Result: Every component you create will be production-ready with zero deployment issues!**

---

## **🚀 Enhanced with Shopify MCP Integration**

**When working with AI assistants that support MCP, you get:**

- **Real-time validation** against live Shopify APIs
- **Direct documentation access** to official Shopify resources
- **Schema introspection** for accurate API development
- **GraphQL validation** for complex data requirements
- **Theme compliance checking** against current Shopify standards

**📖 Complete Setup Guide: [SHOPIFY-MCP-SETUP.md](./shopify-liquid-guides/docs/development/SHOPIFY-MCP-SETUP.md)**

---

**🎯 You now have everything needed to build perfect Shopify Liquid components with automated validation, comprehensive quality assurance, and zero development friction!**