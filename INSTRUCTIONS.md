# Complete Instructions for Shopify Theme Development

This guide provides comprehensive instructions for all types of Shopify theme development tasks using this complete resource.

## 📖 How to Use This Guide

### Development Tasks
- [Building Complete Themes](#building-complete-themes) - New theme from scratch
- [Adding Features](#adding-features) - Specific functionality implementation
- [Creating Individual Files](#creating-individual-files) - Sections, blocks, snippets
- [Performance Optimization](#performance-optimization) - Speed and Core Web Vitals
- [Multi-language Implementation](#multi-language-implementation) - Internationalization
- [Advanced Features](#advanced-features) - AI, PWA, metaobjects

### Quick References
- [Task-Specific Quick Paths](#task-specific-quick-paths) - Fast navigation for common tasks
- [Development Standards](#development-standards) - Code quality requirements
- [Schema Validation](#schema-validation) - Prevent errors
- [AI Assistant Guide](./.claude/project-guide.md) - Complete project workflows for Claude agents

---

# Theme Validation Automation

## 🎯 **Ultimate Theme Validation Setup**

**Your theme validation setup is 100% ready for production with comprehensive validation coverage!**

### ⚡ **Quick Validation Commands**

```bash
# Complete validation workflow - one command does everything:
./scripts/validate-theme.sh all

# Fast development validation (essential checks only):
./scripts/validate-theme.sh development

# Production validation (Theme Store ready):
./scripts/validate-theme.sh production

# Auto-fix issues:
./scripts/validate-theme.sh auto-fix
```

**Result**: 100% Theme Store compliance guaranteed with automated error detection, correction, and comprehensive reporting!

### 🔧 **Available Validation Levels**

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `./scripts/validate-theme.sh development` | Fast validation with ultimate checks | During daily development |
| `./scripts/validate-theme.sh ultimate` | Zero tolerance liquid validation only | Quick quality check |
| `./scripts/validate-theme.sh deep` | Ultimate + integrity + comprehensive | Pre-deployment validation |
| `./scripts/validate-theme.sh comprehensive` | Complete validation suite | Before committing changes |
| `./scripts/validate-theme.sh production` | Theme Store submission ready | Before going live |
| `./scripts/validate-theme.sh auto-fix` | Auto-correct fixable issues | When validation shows errors |
| `./scripts/validate-theme.sh all` | Complete workflow | Full validation process |

### 📊 **What Gets Validated**

- **50+ Validation Rules**: All critical checks for schema, content, performance, and security
- **All 7 File Types**: Sections, snippets, templates, layouts, locales, JSON configs, CSS
- **Theme Store Compliance**: 100% alignment with Theme Store requirements
- **Performance Checks**: Core Web Vitals and optimization best practices
- **Accessibility Standards**: WCAG 2.1 AA compliance validation
- **Security Patterns**: Content validation and security best practices

📖 **[Complete Validation Guide](./THEME-CHECK-SETUP.md)** - Comprehensive validation documentation

## 🚀 **Daily Development Workflow**

### **Step 1: Before You Start Coding**
```bash
# Ensure your environment is ready
./scripts/validate-theme.sh development
```

### **Step 2: During Development**
```bash
# Quick check after making changes
./scripts/validate-theme.sh development

# Auto-fix any simple issues
./scripts/validate-theme.sh auto-fix
```

### **Step 3: Before Committing**
```bash
# Comprehensive validation
./scripts/validate-theme.sh comprehensive
```

### **Step 4: Production Ready**
```bash
# Final validation before deployment
./scripts/validate-theme.sh production
```

## 🏆 **Production-Ready Validation**

### **Theme Store Submission Workflow**
```bash
# Run complete validation suite
./scripts/validate-theme.sh all

# Generate detailed report
./scripts/validate-theme.sh report

# Final production check
./scripts/validate-theme.sh production
```

**Guaranteed Result**: Zero Theme Store rejections with our comprehensive validation setup!

### **CI/CD Integration**
```bash
# JSON output for automated workflows
shopify theme check --output json --config .theme-check-production.yml

# Fail on errors for automated builds
shopify theme check --fail-level error --config .theme-check-production.yml
```

---

# Building Complete Themes

## 🎯 New Theme Development

### Prerequisites
- Shopify CLI installed
- VS Code with Shopify Liquid extension
- Understanding of target audience and requirements

### Architecture Planning
**Start Here**: [Theme Architecture Overview](./shopify-liquid-guides/docs/architecture/theme-overview.md)

1. **Understand Complete Structure**
   - Review [File Taxonomy](./shopify-liquid-guides/docs/architecture/file-taxonomy.md) - All 7 file types
   - Study [Best Practices 2025](./shopify-liquid-guides/docs/architecture/best-practices-2025.md)
   - Plan theme features and customization needs

### Foundation Implementation
**Reference**: [Layouts Documentation](./shopify-liquid-guides/docs/layouts/)

1. **Set Up Core Files**
   - Create [theme.liquid](./shopify-liquid-guides/docs/layouts/theme-liquid.md) foundation
   - Configure [checkout.liquid](./shopify-liquid-guides/docs/layouts/checkout-liquid.md) if needed
   - Set up asset pipeline using [Assets Guide](./shopify-liquid-guides/docs/assets/)

2. **Validate Foundation**
   ```bash
   # Test your theme foundation
   ./scripts/validate-theme.sh development
   ```

### Template Architecture
**Reference**: [Templates Documentation](./shopify-liquid-guides/docs/templates/)

1. **Choose Template Strategy**
   - Use [JSON Templates](./shopify-liquid-guides/docs/templates/json-templates.md) for merchant flexibility
   - Use [Liquid Templates](./shopify-liquid-guides/docs/templates/liquid-templates.md) for custom logic
   - Implement [Metaobject Templates](./shopify-liquid-guides/docs/templates/metaobject-templates.md) for custom content

2. **Validate Template Configuration**
   ```bash
   # Ensure templates are properly configured
   ./scripts/validate-theme.sh development
   ```

### Section Development
**Reference**: [Code Library](./shopify-liquid-guides/code-library/)

1. **Use Production-Ready Components**
   - Copy from [sections directory](./shopify-liquid-guides/code-library/sections/)
   - Customize [blocks](./shopify-liquid-guides/code-library/blocks/) for reusability
   - Implement [CSS patterns](./shopify-liquid-guides/code-library/css-patterns/) for scoping

2. **Validate Each Section**
   ```bash
   # After adding each section, validate immediately
   ./scripts/validate-theme.sh development

   # Auto-fix any schema or syntax issues
   ./scripts/validate-theme.sh auto-fix
   ```

### Configuration Setup
**Reference**: [Config Documentation](./shopify-liquid-guides/docs/config/)

1. **Merchant Customization**
   - Create [settings schema](./shopify-liquid-guides/docs/config/settings-schema.md)
   - Configure [section groups](./shopify-liquid-guides/docs/section-groups/) for layout flexibility
   - Set up [block configurations](./shopify-liquid-guides/docs/config/blocks-config.md)

2. **Final Theme Validation**
   ```bash
   # Complete validation before launch
   ./scripts/validate-theme.sh production

   # Generate compliance report
   ./scripts/validate-theme.sh report
   ```

### 🎉 **Theme Store Submission Ready**

When your theme passes all validation levels:
```bash
# Final validation confirms Theme Store readiness
./scripts/validate-theme.sh all
```

**Guaranteed**: Your theme will meet all Theme Store requirements!

---

# Adding Features

## 🔥 Feature Implementation Paths

### E-commerce Features
- **Product Display**: Use [product sections](./shopify-liquid-guides/code-library/sections/) and [JSON templates](./shopify-liquid-guides/docs/templates/json-templates.md)
- **Cart Functionality**: Reference [JavaScript assets](./shopify-liquid-guides/docs/assets/javascript-assets.md)
- **Search & Filtering**: Implement section groups and dynamic content

**Validation**: After implementing each feature:
```bash
./scripts/validate-theme.sh development  # Quick validation
./scripts/validate-theme.sh auto-fix     # Fix any issues
```

### Content Management
- **Blog Integration**: Use [template documentation](./shopify-liquid-guides/docs/templates/)
- **Custom Content Types**: Implement [metaobjects](./shopify-liquid-guides/docs/advanced-features/metaobject-integration.md)
- **Dynamic Layouts**: Use [section groups](./shopify-liquid-guides/docs/section-groups/)

**Validation**: Ensure content templates work correctly:
```bash
./scripts/validate-theme.sh comprehensive  # Full validation
```

### Performance Features
- **Speed Optimization**: Follow [advanced performance](./shopify-liquid-guides/docs/advanced-features/advanced-performance.md)
- **Core Web Vitals**: Implement [asset optimization](./shopify-liquid-guides/docs/assets/)
- **PWA Features**: Add [progressive web app](./shopify-liquid-guides/docs/advanced-features/progressive-web-app.md) capabilities

**Validation**: Performance checks included in validation:
```bash
./scripts/validate-theme.sh production  # Performance + Theme Store validation
```

### Multi-language Support
- **Translation Setup**: Use [locales documentation](./shopify-liquid-guides/docs/locales/)
- **Regional Formatting**: Configure locale-specific formats
- **Language Switching**: Implement navigation patterns

**Validation**: Translation validation included:
```bash
./scripts/validate-theme.sh production  # Includes translation checks
```

---

---

# Task-Specific Quick Paths

## 🚀 Common Development Scenarios

### Building a Store Homepage
1. **Architecture**: [Theme Overview](./shopify-liquid-guides/docs/architecture/theme-overview.md)
2. **Layout**: [theme.liquid](./shopify-liquid-guides/docs/layouts/theme-liquid.md)
3. **Template**: [JSON templates](./shopify-liquid-guides/docs/templates/json-templates.md)
4. **Sections**: [Hero](./shopify-liquid-guides/code-library/sections/hero-banner.liquid), [Products](./shopify-liquid-guides/code-library/sections/product-grid.liquid)
5. **Examples**: [Complete homepage](./shopify-liquid-guides/examples/complete-homepage.json)
6. **Validate**: `./scripts/validate-theme.sh development` after each step

### Adding Product Features
1. **Templates**: [Product templates](./shopify-liquid-guides/docs/templates/json-templates.md)
2. **Sections**: [Product sections](./shopify-liquid-guides/code-library/sections/)
3. **JavaScript**: [Product interactions](./shopify-liquid-guides/docs/assets/javascript-assets.md)
4. **Performance**: [Image optimization](./shopify-liquid-guides/docs/assets/image-assets.md)
5. **Validate**: `./scripts/validate-theme.sh comprehensive` before deployment

### Implementing Multi-language
1. **Strategy**: [Translation system](./shopify-liquid-guides/docs/locales/translation-system.md)
2. **Files**: [Locale structure](./shopify-liquid-guides/docs/locales/locale-file-structure.md)
3. **Implementation**: Replace hard-coded text with `{{ 'key' | t }}`
4. **Regional**: [Formatting patterns](./shopify-liquid-guides/docs/locales/regional-formatting.md)
5. **Validate**: `./scripts/validate-theme.sh production` includes translation checks

### Performance Optimization
1. **Assets**: [CSS](./shopify-liquid-guides/docs/assets/css-assets.md), [JS](./shopify-liquid-guides/docs/assets/javascript-assets.md), [Images](./shopify-liquid-guides/docs/assets/image-assets.md)
2. **Advanced**: [Performance patterns](./shopify-liquid-guides/docs/advanced-features/advanced-performance.md)
3. **Core Web Vitals**: [Best practices](./shopify-liquid-guides/docs/architecture/best-practices-2025.md)
4. **Validate**: `./scripts/validate-theme.sh production` includes performance checks

### Adding Custom Content
1. **Metaobjects**: [Integration guide](./shopify-liquid-guides/docs/advanced-features/metaobject-integration.md)
2. **Templates**: [Metaobject templates](./shopify-liquid-guides/docs/templates/metaobject-templates.md)
3. **Dynamic**: [Section groups](./shopify-liquid-guides/docs/section-groups/)
4. **Validate**: `./scripts/validate-theme.sh comprehensive` after implementation

### Modern Features
1. **AI Blocks**: [AI-generated blocks](./shopify-liquid-guides/docs/advanced-features/ai-generated-blocks.md)
2. **PWA**: [Progressive web app](./shopify-liquid-guides/docs/advanced-features/progressive-web-app.md)
3. **Section Groups**: [Dynamic layouts](./shopify-liquid-guides/docs/section-groups/)
4. **Validate**: `./scripts/validate-theme.sh all` for complete feature validation

---

# Creating Individual Files

**When creating any new Shopify Liquid section, block, snippet, or CSS pattern, follow these instructions exactly.**

## 🎯 **Before You Start**

**CRITICAL: Start with validation setup**
```bash
# Ensure your validation environment is ready
./scripts/validate-theme.sh development
```

When given a prompt like *"Create a product comparison section"* or *"Build a newsletter signup block"*, follow these instructions **exactly** to ensure consistency with our established methodology.

### 🎨 **Design System First Approach**

This repository uses a **unified design token system** that ensures consistency across all components. Before coding, understand our design hierarchy:

```
Primitive Tokens → Semantic Tokens → Component Tokens
   (Base Values)     (Contextual)      (Specific Use)
```

**Key Design System Files:**
- **Design Tokens**: `code-library/css-patterns/design-tokens.css` (450+ tokens)
- **Implementation Guide**: `docs/architecture/design-system-implementation.md`
- **Token Integration**: All components use token-based CSS for consistency

**Design Token Usage Pattern:**
```liquid
{% style %}
  .component-{{ unique }} {
    /* ✅ Component tokens with semantic fallbacks */
    --component-bg: var(--surface-primary);
    --component-text: var(--text-primary);
    --component-spacing: var(--spacing-component-md);

    /* ✅ Shopify setting integration with token fallbacks */
    --dynamic-bg: {{ block.settings.bg_color | default: 'var(--component-bg)' }};
    --dynamic-text: {{ block.settings.text_color | default: 'var(--component-text)' }};

    /* Apply tokens to properties */
    background: var(--dynamic-bg);
    color: var(--dynamic-text);
    padding: var(--component-spacing);
  }
{% endstyle %}
```

### **🚀 Validation-First Development with Shopify MCP**

Every file creation must include validation steps with Shopify MCP integration:

1. **Before coding**: Run quick validation check + MCP documentation lookup
2. **During development**: Validate schema as you build it + live GraphQL validation
3. **After completion**: Comprehensive validation + MCP theme validation
4. **Before deployment**: Production-ready validation + Theme Store compliance

### **🔗 Shopify MCP Server Integration**

This repository includes comprehensive Shopify MCP server integration for enhanced development capabilities:

**MCP Tools Available:**
- `learn_shopify_api` - Initialize Shopify API context for development
- `validate_theme` - Comprehensive theme validation against Shopify standards
- `validate_graphql_codeblocks` - Real-time GraphQL query validation
- `introspect_graphql_schema` - Live schema introspection for API development
- `search_docs_chunks` - Search official Shopify documentation
- `fetch_full_docs` - Retrieve complete documentation pages

**MCP Usage in Development Workflow:**
```bash
# 1. Traditional validation
./scripts/validate-theme.sh development

# 2. Enhanced MCP validation (when working with AI assistants)
# - Use validate_theme for comprehensive Liquid validation
# - Use validate_graphql_codeblocks for API queries
# - Use search_docs_chunks for documentation lookup
# - Use introspect_graphql_schema for schema exploration
```

📖 **[Complete MCP Setup Guide](./SHOPIFY-MCP-SETUP.md)** - Full integration and usage documentation

---

## 📋 **STEP 1: Understand Our Codebase Structure**

### **Available File Types & Locations**

```
shopify-liquid-guides/
├── code-library/
│   ├── sections/           # Complete page sections (.liquid files)
│   ├── blocks/            # Reusable theme block components (.liquid files)
│   ├── snippets/          # Utility functions (.liquid files)
│   └── css-patterns/      # CSS methodology examples (.css files)
└── schema-validation/
    └── schema-guidelines.md  # **CRITICAL**: Schema validation rules
```

### **🎯 CRITICAL: Understanding Sections vs Blocks**

**There are TWO types of blocks in Shopify themes:**

#### **1. Theme Blocks (Standalone Files)**
- **Location**: `/blocks` folder in theme root
- **File Extension**: `.liquid`
- **Schema**: Has its own `{% schema %}` tag
- **Reusability**: Can be used across multiple sections
- **Nesting**: Can contain other blocks (hierarchical)
- **Example**: `blocks/text.liquid`, `blocks/image.liquid`

#### **2. Section Blocks (Defined Within Sections)**
- **Location**: Defined within section files
- **Schema**: Defined in section's `{% schema %}` blocks array
- **Reusability**: Only within the section where defined
- **Nesting**: Cannot be nested (single level only)
- **Example**: Block types in a section's schema

**Key Difference**: Theme blocks are standalone files that can be saved separately and reused across sections. Section blocks are just configuration in a section's schema.

### **🚨 MANDATORY FIRST STEP: Schema Validation**

**BEFORE creating ANY schema**, you MUST review:**
`shopify-liquid-guides/schema-validation/schema-guidelines.md`

This document prevents "FileSaveError: Invalid schema" errors by providing:
- Comprehensive validation rules and requirements
- Range step calculation formulas: `(max - min) / step ≤ 101`
- Valid setting types (use `video` not `file` for video uploads)
- Critical restrictions (no `enabled_on` in section schemas)
- Step value minimums (≥ 0.1 for all ranges)

**Automated Schema Validation**: Our validation system will catch schema errors:
```bash
# This will validate your schema automatically
./scripts/validate-theme.sh development
```

### **Reference Existing Patterns**

**ALWAYS** examine these files first to understand our patterns:

1. **🔴 CRITICAL**: `shopify-liquid-guides/schema-validation/schema-guidelines.md` - Schema validation rules
2. **Section Example**: `shopify-liquid-guides/code-library/sections/hero-richtext-cta.liquid`
3. **Block Example**: `shopify-liquid-guides/code-library/blocks/block-feature-item.liquid`
4. **CSS Scoping**: `shopify-liquid-guides/code-library/css-patterns/scoped-blocks.css`
5. **JSON Examples**: `shopify-liquid-guides/examples/complete-homepage.json`

---

## 📐 **STEP 2: Design System + CSS Scoping Methodology (CRITICAL)**

### **Unique ID Generation Pattern**

**Every section and block MUST use this exact pattern:**

```liquid
{%- assign unique = section.id | replace: '_', '' | downcase -%}
<!-- For blocks: -->
{%- assign u = block.id | replace: '_', '' | downcase -%}
```

### **Design Token Integration Pattern**

**All components MUST use design tokens for consistency:**

```liquid
{% style %}
  .component-name-{{ unique }} {
    /* ✅ Component tokens with semantic fallbacks */
    --component-bg: var(--surface-primary);
    --component-text: var(--text-primary);
    --component-spacing: var(--spacing-component-md);
    --component-radius: var(--border-radius-lg);

    /* ✅ Shopify setting integration with token fallbacks */
    --dynamic-bg: {{ section.settings.bg_color | default: 'var(--component-bg)' }};
    --dynamic-text: {{ section.settings.text_color | default: 'var(--component-text)' }};
    --dynamic-accent: {{ section.settings.accent_color | default: 'var(--brand-primary-500)' }};

    /* ✅ Apply tokens to properties */
    background: var(--dynamic-bg);
    color: var(--dynamic-text);
    padding: var(--component-spacing);
    border-radius: var(--component-radius);
  }
{% endstyle %}
```

### **CSS Class Naming Convention**

**All CSS classes MUST follow this pattern with design tokens:**

```liquid
<!-- Base component with token-based styling -->
<div class="component-name-{{ unique }}">

<!-- Elements within component -->
<h2 class="component-name__title-{{ unique }}">
<p class="component-name__text-{{ unique }}">

<!-- Modifiers -->
<div class="component-name--large-{{ unique }}">
```

### **Complete CSS Style Block Structure with Design Tokens**

```liquid
{% style %}
  .component-name-{{ unique }} {
    /* ✅ Design token integration */
    --component-bg: var(--surface-primary);
    --component-text: var(--text-primary);
    --component-spacing: var(--spacing-component-md);

    /* ✅ Dynamic values from Shopify settings */
    --dynamic-bg: {{ section.settings.bg_color | default: 'var(--component-bg)' }};
    --dynamic-text: {{ section.settings.text_color | default: 'var(--component-text)' }};

    /* ✅ Apply design tokens */
    background: var(--dynamic-bg);
    color: var(--dynamic-text);
    padding: var(--component-spacing);
    box-shadow: var(--shadow-sm);
    border-radius: var(--border-radius-lg);
  }

  .component-name__element-{{ unique }} {
    /* ✅ Element styles using design tokens */
    font-size: var(--font-size-base);
    line-height: var(--line-height-normal);
    color: var(--dynamic-text);
  }

  /* ✅ Focus states using design tokens */
  .component-name-{{ unique }}:focus-within {
    outline: var(--focus-ring-width) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  /* ✅ Responsive behavior using token system */
  @media (max-width: 749px) {
    .component-name-{{ unique }} {
      padding: var(--spacing-component-sm);
    }
  }
{% endstyle %}
```

### **Token Selection Guidelines**

**Choose appropriate token tiers:**

1. **Component Tokens** (Preferred): `--button-primary-bg`, `--card-padding`
2. **Semantic Tokens** (Fallback): `--surface-primary`, `--text-primary`
3. **Primitive Tokens** (Avoid): `--neutral-100`, `--space-4`

**Token Integration Checklist:**
- [ ] Use semantic tokens, not primitives directly
- [ ] Provide Shopify setting fallbacks with token defaults
- [ ] Include focus states using design token system
- [ ] Apply responsive adjustments through tokens

---

## 🏗 **STEP 3: File Structure Requirements with Design Tokens**

### **For Sections (`sections/component-name.liquid`)**

```liquid
{% comment %} sections/component-name.liquid {% endcomment %}
{%- assign unique = section.id | replace: '_', '' | downcase -%}

{% style %}
  .component-name-{{ unique }} {
    /* ✅ Component tokens with semantic fallbacks */
    --component-bg: var(--surface-primary);
    --component-text: var(--text-primary);
    --component-spacing: var(--spacing-component-md);
    --component-radius: var(--border-radius-lg);

    /* ✅ Shopify setting integration with token fallbacks */
    --dynamic-bg: {{ section.settings.bg_color | default: 'var(--component-bg)' }};
    --dynamic-text: {{ section.settings.text_color | default: 'var(--component-text)' }};
    --dynamic-accent: {{ section.settings.accent_color | default: 'var(--brand-primary-500)' }};

    /* Apply tokens to properties */
    background: var(--dynamic-bg);
    color: var(--dynamic-text);
    padding: var(--component-spacing);
    border-radius: var(--component-radius);
    box-shadow: var(--shadow-sm);
  }

  .component-name__element-{{ unique }} {
    font-size: var(--font-size-base);
    line-height: var(--line-height-normal);
    color: var(--dynamic-text);
  }

  /* Focus states using design tokens */
  .component-name-{{ unique }}:focus-within {
    outline: var(--focus-ring-width) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  /* Responsive using tokens */
  @media (max-width: 749px) {
    .component-name-{{ unique }} {
      padding: var(--spacing-component-sm);
    }
  }
{% endstyle %}

<section class="component-name-{{ unique }}" role="region" aria-label="{{ section.settings.aria_label | default: section.settings.heading | default: 'Section name' | escape }}">
  <!-- HTML structure with escaped content -->
  <!-- Use section.settings.* for configuration -->
  <!-- Include blocks loop if needed -->
</section>

{% schema %}{
  "name": "Section Name",
  "settings": [
    {
      "type": "header",
      "content": "Design Tokens"
    },
    {
      "type": "color",
      "id": "bg_color",
      "label": "Background Color",
      "info": "Uses --surface-primary token as fallback"
    },
    {
      "type": "color",
      "id": "text_color",
      "label": "Text Color",
      "info": "Uses --text-primary token as fallback"
    },
    {
      "type": "color",
      "id": "accent_color",
      "label": "Accent Color",
      "info": "Uses --brand-primary-500 token as fallback"
    }
  ],
  "blocks": [
    /* Block types if applicable */
  ],
  "presets": [
    {"name": "Section Name"}
  ]
}{% endschema %}
```

### **For Theme Blocks (`blocks/block-component-name.liquid`)**

**IMPORTANT**: Theme blocks are **standalone files** in the `/blocks` folder with their own `{% schema %}` tags. They can be saved separately and used across multiple sections.

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
{% endstyle %}

<div class="block-name-{{ u }}" {{ block.shopify_attributes }}>
  <h3 class="block-name__title-{{ u }}">{{ block.settings.title | escape }}</h3>
  <p class="block-name__text-{{ u }}">{{ block.settings.content | escape }}</p>
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
      "id": "title",
      "label": "Title",
      "default": "Default title"
    },
    {
      "type": "textarea",
      "id": "content",
      "label": "Content",
      "default": "Default content"
    },
    {
      "type": "header",
      "content": "Design Tokens"
    },
    {
      "type": "color",
      "id": "bg_color",
      "label": "Background Color",
      "info": "Uses --surface-secondary token as fallback"
    },
    {
      "type": "color",
      "id": "text_color",
      "label": "Text Color",
      "info": "Uses --text-primary token as fallback"
    }
  ],
  "presets": [
    {
      "name": "Block Name",
      "settings": {
        "title": "Default title",
        "content": "Default content"
      }
    }
  ]
}
{% endschema %}
```

### **For Section Blocks (Defined Within Sections)**

**Alternative**: Block types defined within a section's schema (not standalone files):

```liquid
<!-- In section template -->
{% for block in section.blocks %}
  {% case block.type %}
    {% when 'custom_block' %}
      <div class="section-block-{{ unique }}" {{ block.shopify_attributes }}>
        {{ block.settings.content | escape }}
      </div>
  {% endcase %}
{% endfor %}

<!-- In section schema -->
{
  "blocks": [
    {
      "type": "custom_block",
      "name": "Custom Block",
      "settings": [
        {
          "type": "text",
          "id": "content",
          "label": "Content"
        }
      ]
    }
  ]
}
```

### **For Snippets (`snippets/snippet-name.liquid`)**

**Snippets support design tokens for reusable styling patterns:**

```liquid
{% comment %}
  Snippet: snippet-name
  Usage: {% render 'snippet-name', param1: value1, param2: value2, unique_id: 'component-123' %}

  Parameters:
  - param1 (required): Description
  - param2 (optional): Description with default
  - unique_id (required): Unique ID for scoped styling
  - bg_color (optional): Background color override
  - text_color (optional): Text color override

  Design Token Integration:
  - Uses semantic tokens with component-specific fallbacks
  - Supports color customization through parameters
  - Maintains consistent spacing and typography
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
{% endstyle %}

<div class="snippet-name-{{ unique_id }}">
  <!-- Snippet functionality with design token styling -->
  {{ param1 | escape }}
</div>
```

---

## 🎨 **STEP 4: Schema Configuration Standards**

### **⚠️ CRITICAL: Schema Validation Requirements**

**BEFORE writing ANY schema, validate against these rules:**

1. **Range Step Calculation**: `(max - min) / step ≤ 101`
   ```json
   // ❌ BAD: (100-0)/1 = 100 steps ✓, but (200-0)/1 = 200 steps ✗
   {"type": "range", "min": 0, "max": 200, "step": 1}  // INVALID

   // ✅ GOOD: (200-0)/2 = 100 steps ✓
   {"type": "range", "min": 0, "max": 200, "step": 2}  // VALID
   ```

2. **Valid Setting Types**: Never use `"type": "file"` for videos
   ```json
   // ❌ BAD: Will cause "Invalid schema" error
   {"type": "file", "id": "video_file", "label": "Video"}

   // ✅ GOOD: Use video type for video uploads
   {"type": "video", "id": "video_file", "label": "Video"}
   ```

3. **Section Restrictions**: Never use `enabled_on` in sections (app blocks only)
   ```json
   // ❌ BAD: Will cause "enabled_on is not a valid attribute" error
   {"name": "Section", "enabled_on": {"templates": ["index"]}}

   // ✅ GOOD: Remove enabled_on from sections
   {"name": "Section"}
   ```

4. **Step Values**: Must be ≥ 0.1
   ```json
   // ❌ BAD: Step below minimum
   {"type": "range", "step": 0.01}

   // ✅ GOOD: Step meets minimum
   {"type": "range", "step": 0.1}
   ```

### **Section Schema Requirements**

```json
{
  "name": "Descriptive Section Name",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Default heading"
    },
    {
      "type": "richtext",
      "id": "content",
      "label": "Content",
      "info": "Helpful description for merchants"
    },
    {
      "type": "color",
      "id": "bg_color",
      "label": "Background color",
      "default": "#ffffff"
    }
  ],
  "blocks": [
    {
      "type": "block_type",
      "name": "Block Display Name",
      "settings": [/* block settings */]
    }
  ],
  "presets": [
    {
      "name": "Section Name",
      "blocks": [/* default blocks if any */]
    }
  ]
}
```

### **Common Setting Patterns**

Use these **validated patterns** for consistency:

```json
// Text fields
{"type": "text", "id": "heading", "label": "Heading", "default": "Default text"}

// Rich text
{"type": "richtext", "id": "content", "label": "Content"}

// Colors
{"type": "color", "id": "bg_color", "label": "Background color", "default": "#ffffff"}

// URLs
{"type": "url", "id": "link_url", "label": "Link URL"}

// Images
{"type": "image_picker", "id": "image", "label": "Image"}

// Videos (NEVER use "file" type)
{"type": "video", "id": "video_file", "label": "Video Upload"}
{"type": "video_url", "id": "video_url", "label": "Video URL"}

// Ranges (ALWAYS validate step calculation)
{"type": "range", "id": "padding", "label": "Padding", "min": 0, "max": 100, "step": 4, "unit": "px", "default": 20}
// ✅ Calculation: (100-0)/4 = 25 steps (≤ 101) ✓

{"type": "range", "id": "opacity", "label": "Opacity", "min": 0, "max": 100, "step": 1, "unit": "%", "default": 50}
// ✅ Calculation: (100-0)/1 = 100 steps (≤ 101) ✓

// Select options
{"type": "select", "id": "alignment", "label": "Alignment", "options": [
  {"value": "left", "label": "Left"},
  {"value": "center", "label": "Center"},
  {"value": "right", "label": "Right"}
], "default": "center"}
```

---

## ♿ **STEP 5: Accessibility Requirements (MANDATORY)**

### **HTML Structure Standards**

```liquid
<!-- Semantic HTML with proper ARIA -->
<section role="region" aria-label="{{ section.settings.aria_label | default: section.settings.heading | escape }}">
  <h2>{{ section.settings.heading | escape }}</h2>

  <!-- Proper heading hierarchy -->
  <h3>{{ block.settings.title | escape }}</h3>

  <!-- Escaped user content -->
  <p>{{ section.settings.text | escape }}</p>

  <!-- Links with aria-labels -->
  <a href="{{ section.settings.url }}" aria-label="{{ section.settings.aria_label | default: section.settings.link_text | escape }}">
    {{ section.settings.link_text | escape }}
  </a>
</section>
```

### **Required Accessibility Features**

1. **Escape ALL user content**: `{{ content | escape }}`
2. **Semantic HTML**: Use `<section>`, `<article>`, `<header>`, etc.
3. **ARIA labels**: Provide context for screen readers
4. **Proper headings**: Logical h1→h2→h3 hierarchy
5. **Alt text**: Images must have meaningful alt attributes
6. **Focus management**: Visible focus states in CSS

---

## 🚀 **STEP 6: Performance & Theme Store Compliance**

### **Liquid Best Practices**

```liquid
<!-- Check for blank values -->
{% if section.settings.heading != blank %}
  <h2>{{ section.settings.heading | escape }}</h2>
{% endif %}

<!-- Responsive images -->
{% if section.settings.image %}
  <img
    src="{{ section.settings.image | image_url: width: 800 }}"
    srcset="{{ section.settings.image | image_url: width: 400 }} 400w,
            {{ section.settings.image | image_url: width: 800 }} 800w"
    sizes="(min-width: 750px) 50vw, 100vw"
    alt="{{ section.settings.image.alt | escape }}"
    loading="lazy"
  >
{% endif %}

<!-- Safe property access -->
{{ product.title | default: 'Product' | escape }}
```

### **CSS Performance Rules**

```css
/* Use CSS custom properties for dynamic values */
.component-{{ unique }} {
  --bg-color: {{ section.settings.bg_color | default: '#ffffff' }};
  --text-color: {{ section.settings.text_color | default: '#333333' }};

  background: var(--bg-color);
  color: var(--text-color);
}

/* Mobile-first responsive design */
.component-{{ unique }} {
  /* Mobile styles first */
}

@media (min-width: 750px) {
  .component-{{ unique }} {
    /* Desktop styles */
  }
}
```

---

## 📝 **STEP 7: Content Standards**

### **Default Content Guidelines**

- **Headings**: Use realistic, merchant-friendly defaults
- **Text**: Provide meaningful placeholder content
- **Links**: Default to common Shopify URLs (`/collections/all`, `/pages/about`)
- **Images**: Reference common image scenarios in alt text
- **Colors**: Use neutral, professional color palettes

### **Schema Labels & Info Text**

```json
{
  "type": "text",
  "id": "heading",
  "label": "Section heading",
  "info": "This appears at the top of your section",
  "default": "Welcome to our store"
}
```

---

## 🔄 **STEP 8: Integration Patterns**

### **Block Integration in Sections**

```liquid
{% if section.blocks.size > 0 %}
  <div class="section-name__blocks-{{ unique }}">
    {% for block in section.blocks %}
      {% case block.type %}
        {% when 'feature_item' %}
          {% render 'block-feature-item', block: block %}
        {% when 'text_block' %}
          {% render 'block-text', block: block %}
      {% endcase %}
    {% endfor %}
  </div>
{% endif %}
```

### **Snippet Integration**

```liquid
<!-- In sections or blocks -->
{% render 'responsive-image',
   image: section.settings.image,
   alt: section.settings.heading,
   sizes: '(min-width: 750px) 50vw, 100vw' %}
```

---

## 📁 **STEP 9: File Naming & Comments**

### **File Naming Convention**

- **Sections**: `section-name.liquid` (kebab-case)
- **Blocks**: `block-component-name.liquid`
- **Snippets**: `utility-name.liquid`
- **CSS**: `pattern-name.css`

### **Required Comments**

```liquid
{% comment %} sections/section-name.liquid {% endcomment %}
<!-- At the top of every file -->

{%- comment -%} Block schema (add under section schema) {%- endcomment -%}
<!-- For block schema reference -->
```

---

## ✅ **STEP 10: Validation & Quality Checklist**

### **🚀 Automated Validation First + Shopify MCP**

**Run these commands for every new file:**

```bash
# 1. Development validation (fast)
./scripts/validate-theme.sh development

# 2. Auto-fix any simple issues
./scripts/validate-theme.sh auto-fix

# 3. Comprehensive validation
./scripts/validate-theme.sh comprehensive

# 4. Production readiness check
./scripts/validate-theme.sh production
```

**Enhanced validation with Shopify MCP (when working with AI assistants):**
- **Theme Validation**: Use `validate_theme` MCP tool for comprehensive Liquid template validation
- **GraphQL Validation**: Use `validate_graphql_codeblocks` for API query validation
- **Documentation Lookup**: Use `search_docs_chunks` for real-time Shopify documentation
- **Schema Exploration**: Use `introspect_graphql_schema` for API development and exploration
- **Complete Documentation**: Use `fetch_full_docs` for comprehensive reference material

**MCP Integration Benefits:**
- Real-time validation against live Shopify APIs
- Direct access to official Shopify documentation
- Schema introspection for accurate API development
- Theme Store compliance validation
- Automated error detection and prevention

### **Manual Quality Checks**

After automated validation passes, verify:

### **Code Quality**
- [ ] Uses unique ID scoping pattern (`{{ unique }}` or `{{ u }}`)
- [ ] All user content is escaped with `| escape`
- [ ] Blank value checks for optional settings
- [ ] Responsive CSS with mobile-first approach
- [ ] CSS custom properties for dynamic values

### **Design System Compliance**
- [ ] **Design token integration**: Uses semantic tokens, not primitives directly
- [ ] **Token fallbacks**: Shopify settings provide token defaults (`{{ block.settings.bg_color | default: 'var(--component-bg)' }}`)
- [ ] **Component tokens**: Uses appropriate tier (component → semantic → primitive)
- [ ] **Focus states**: Implements design token-based focus management
- [ ] **Responsive tokens**: Uses token system for responsive adjustments
- [ ] **Schema integration**: Color settings reference design token fallbacks in `info` text
- [ ] **Token consistency**: Component CSS follows unified design token patterns

### **Accessibility**
- [ ] Semantic HTML structure
- [ ] Proper ARIA labels and roles
- [ ] Logical heading hierarchy
- [ ] Meaningful alt text for images
- [ ] Sufficient color contrast

### **Schema Validation (AUTOMATED + MANUAL)**
- [ ] **Automated validation passed**: `./scripts/validate-theme.sh development` shows no errors
- [ ] **Applied schema validation rules** from `schema-validation/schema-guidelines.md`
- [ ] **Range step calculations verified**: All ranges follow `(max - min) / step ≤ 101`
- [ ] **Valid setting types confirmed**: Use `video` not `file` for video uploads
- [ ] **No invalid section attributes**: Remove `enabled_on` from sections
- [ ] **Step values meet minimum**: All steps ≥ 0.1
- [ ] **JSON syntax validated**: No trailing commas, proper quotes
- [ ] **Setting IDs are unique**: No duplicate IDs within schema
- [ ] **Auto-fix applied**: `./scripts/validate-theme.sh auto-fix` completed
- [ ] **Production validation passed**: `./scripts/validate-theme.sh production` shows success
- [ ] Descriptive labels and helpful info text
- [ ] Sensible default values

### **Performance**
- [ ] Responsive images with srcset
- [ ] Lazy loading where appropriate
- [ ] Minimal CSS specificity
- [ ] No hardcoded values (use settings)
- [ ] **Design token efficiency**: Groups related token assignments for performance
- [ ] **CSS custom property optimization**: Uses token-based CSS variables for dynamic styling

---

## 🎯 **Summary: What You Need to Do**

When I give you a prompt to create a new Shopify Liquid file:

1. **🚀 START WITH VALIDATION**: Run `./scripts/validate-theme.sh development` to ensure clean environment
2. **🎨 DESIGN SYSTEM FIRST**: Reference design token system (`code-library/css-patterns/design-tokens.css`) and implementation guide
3. **🔴 VALIDATE SCHEMA FIRST**: Review `schema-validation/schema-guidelines.md` before any schema work
4. **Apply validation rules**: Check range calculations, setting types, and restrictions
5. **Identify the type** (section, block, snippet, CSS pattern)
6. **Choose the correct location** in `shopify-liquid-guides/code-library/`
7. **Follow the exact file structure** from Step 3 with design token integration
8. **Use our CSS scoping methodology** with unique IDs and semantic tokens
9. **Include validated schema configuration** with design token fallbacks and realistic defaults
10. **Ensure accessibility compliance** with ARIA and semantic HTML
11. **Follow performance best practices** for Theme Store approval
12. **Match our naming conventions** and comment patterns
13. **🎯 VALIDATE COMPLETION**: Run complete validation workflow:
    ```bash
    ./scripts/validate-theme.sh development  # Quick check
    ./scripts/validate-theme.sh auto-fix     # Fix issues
    ./scripts/validate-theme.sh production   # Final validation
    ```

### **🛡️ Error Prevention Priority**

**The #1 cause of development friction is schema validation errors.** Our automated validation prevents these:

```bash
# Automated error detection and prevention
./scripts/validate-theme.sh development
./scripts/validate-theme.sh auto-fix
```

**Manual validation checks** (automated validation covers most of these):
- Validate range step calculations: `(max - min) / step ≤ 101`
- Use correct setting types: `video` not `file` for uploads
- Remove invalid attributes: No `enabled_on` in sections
- Ensure minimum step values: ≥ 0.1 for all ranges
- Check JSON syntax: No trailing commas or quotes issues

**Key principle**: Every new file should feel like a natural extension of our existing codebase, following identical patterns and maintaining the same level of quality and consistency.

**Design system principle**: Every component must use the unified design token system to ensure visual consistency and maintainability across all theme components.

**Schema validation principle**: Every schema must pass the comprehensive validation rules to prevent "FileSaveError: Invalid schema" errors that break the development workflow.

### **🎉 Validation-First Development Workflow**

```bash
# Perfect development cycle:
./scripts/validate-theme.sh development  # Start clean
# [Create your file]
./scripts/validate-theme.sh development  # Quick validation
./scripts/validate-theme.sh auto-fix     # Fix any issues
./scripts/validate-theme.sh production   # Production ready
```

📖 **Essential References**:
- [Complete Validation Guide](./THEME-CHECK-SETUP.md) - Ultimate validation setup
- [Shopify MCP Server Setup](./SHOPIFY-MCP-SETUP.md) - Direct Shopify API integration
- `shopify-liquid-guides/schema-validation/schema-guidelines.md` - Schema validation rules
- `shopify-liquid-guides/docs/architecture/design-system-implementation.md` - Design system implementation guide
- `shopify-liquid-guides/code-library/css-patterns/design-tokens.css` - Unified design token system (450+ tokens)

**🚀 Result**: 100% Theme Store compliance with unified design system excellence guaranteed with zero development friction!

Now you're ready to create any Shopify Liquid file that perfectly fits our established methodology with full validation automation! 🎉