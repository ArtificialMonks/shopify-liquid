# Design System Implementation Guide

**Unified design token system for consistent, scalable Shopify Liquid components**

## Overview

This implementation guide establishes a **comprehensive design token system** that ensures consistency across all Shopify theme components while maintaining flexibility for merchant customization.

## Design Token Hierarchy

```
Primitive Tokens    →    Semantic Tokens    →    Component Tokens
    (Base Values)           (Contextual)           (Specific Use)
```

### 1. Primitive Tokens (Foundation)
Base design values that rarely change:
```css
--neutral-100: #f1f5f9;
--space-4: 1rem;
--font-size-lg: 1.125rem;
```

### 2. Semantic Tokens (Context)
Contextual meanings that reference primitives:
```css
--surface-primary: var(--neutral-0);
--text-primary: var(--neutral-900);
--spacing-component-md: var(--space-6);
```

### 3. Component Tokens (Specific)
Component-specific values that reference semantic tokens:
```css
--button-primary-bg: var(--brand-primary-500);
--card-padding: var(--spacing-component-md);
--input-border-focus: var(--border-brand);
```

## Implementation in Liquid Components

### Standard Pattern for All Components

```liquid
{% comment %} Generate unique CSS class suffix {% endcomment %}
{% assign unique = block.id | replace: '_', '' | downcase %}

{% style %}
  .component-{{ unique }} {
    /* ✅ Component tokens with semantic fallbacks */
    --component-bg: var(--surface-primary);
    --component-text: var(--text-primary);
    --component-spacing: var(--spacing-component-md);
    --component-radius: var(--border-radius-lg);

    /* ✅ Shopify setting integration with token fallbacks */
    --dynamic-bg: {{ block.settings.bg_color | default: 'var(--component-bg)' }};
    --dynamic-text: {{ block.settings.text_color | default: 'var(--component-text)' }};
    --dynamic-accent: {{ block.settings.accent_color | default: 'var(--brand-primary-500)' }};

    /* ✅ Apply tokens to properties */
    background: var(--dynamic-bg);
    color: var(--dynamic-text);
    padding: var(--component-spacing);
    border-radius: var(--component-radius);

    /* ✅ Responsive behavior using token system */
    gap: var(--spacing-component-sm);
  }

  .component-{{ unique }}__element {
    color: var(--dynamic-text);
    font-size: var(--font-size-base);
    line-height: var(--line-height-normal);
  }

  .component-{{ unique }}__accent {
    color: var(--dynamic-accent);
    border-color: var(--dynamic-accent);
  }

  /* ✅ Focus states using design tokens */
  .component-{{ unique }}:focus-within {
    outline: var(--focus-ring-width) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  /* ✅ Responsive adjustments */
  @media (max-width: 749px) {
    .component-{{ unique }} {
      padding: var(--spacing-component-sm);
      gap: var(--spacing-component-xs);
    }
  }
{% endstyle %}
```

## Component-Specific Implementations

### Video Text Component with Design Tokens

```liquid
{% assign unique = block.id | replace: '_', '' | downcase %}

{% style %}
  .video-text-{{ unique }} {
    /* Component configuration using tokens */
    --component-bg: var(--surface-primary);
    --component-padding: var(--spacing-component-lg);
    --component-gap: var(--spacing-component-md);
    --component-radius: var(--border-radius-lg);

    /* Dynamic values from Shopify settings */
    --video-bg: {{ block.settings.bg_color | default: 'var(--component-bg)' }};
    --video-text: {{ block.settings.text_color | default: 'var(--text-primary)' }};
    --video-accent: {{ block.settings.accent_color | default: 'var(--brand-primary-500)' }};

    /* Apply design tokens */
    background: var(--video-bg);
    padding: var(--component-padding);
    border-radius: var(--component-radius);
    box-shadow: var(--shadow-sm);
  }

  .video-text-{{ unique }}__content {
    display: flex;
    flex-direction: column;
    gap: var(--component-gap);
    color: var(--video-text);
  }

  .video-text-{{ unique }}__heading {
    font-size: var(--font-size-2xl);
    font-weight: var(--font-weight-bold);
    line-height: var(--line-height-tight);
    color: var(--video-text);
  }

  .video-text-{{ unique }}__body {
    font-size: var(--font-size-base);
    line-height: var(--line-height-normal);
    color: var(--text-secondary);
  }

  .video-text-{{ unique }}__video {
    border-radius: var(--border-radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-md);
  }

  /* Button using button tokens */
  .video-text-{{ unique }}__button {
    background: var(--video-accent, var(--button-primary-bg));
    color: var(--button-primary-text);
    padding: var(--button-padding-y) var(--button-padding-x);
    border-radius: var(--button-border-radius);
    font-weight: var(--button-font-weight);
    border: none;
    transition: var(--button-transition);
    cursor: pointer;
  }

  .video-text-{{ unique }}__button:hover {
    filter: brightness(0.95);
    transform: translateY(-1px);
  }

  .video-text-{{ unique }}__button:focus {
    outline: var(--focus-ring);
    outline-offset: var(--focus-ring-offset);
  }
{% endstyle %}
```

### Card Component with Design Tokens

```liquid
{% assign unique = block.id | replace: '_', '' | downcase %}

{% style %}
  .card-{{ unique }} {
    /* Card tokens */
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--card-border-radius);
    box-shadow: var(--card-shadow);
    padding: var(--card-padding);
    transition: box-shadow var(--transition-base);

    /* Dynamic overrides */
    --card-bg-override: {{ block.settings.bg_color | default: 'var(--card-bg)' }};
    background: var(--card-bg-override);
  }

  .card-{{ unique }}:hover {
    box-shadow: var(--card-shadow-hover);
  }

  .card-{{ unique }}__header {
    margin-bottom: var(--spacing-component-md);
    padding-bottom: var(--spacing-component-sm);
    border-bottom: 1px solid var(--border-primary);
  }

  .card-{{ unique }}__title {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-semibold);
    color: var(--text-primary);
    margin: 0;
  }

  .card-{{ unique }}__content {
    color: var(--text-secondary);
    line-height: var(--line-height-normal);
  }
{% endstyle %}
```

## Schema Integration Patterns

### Design Token Settings in Schema

```json
{
  "name": "Design System Component",
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
    },
    {
      "type": "select",
      "id": "spacing_size",
      "label": "Component Spacing",
      "options": [
        {"value": "xs", "label": "Extra Small"},
        {"value": "sm", "label": "Small"},
        {"value": "md", "label": "Medium (Default)"},
        {"value": "lg", "label": "Large"},
        {"value": "xl", "label": "Extra Large"}
      ],
      "default": "md",
      "info": "Uses design token spacing scale"
    }
  ]
}
```

### Dynamic Token Assignment

```liquid
{% style %}
  .component-{{ unique }} {
    /* Spacing token based on setting */
    {% case block.settings.spacing_size %}
      {% when 'xs' %}
        --component-spacing: var(--spacing-component-xs);
      {% when 'sm' %}
        --component-spacing: var(--spacing-component-sm);
      {% when 'lg' %}
        --component-spacing: var(--spacing-component-lg);
      {% when 'xl' %}
        --component-spacing: var(--spacing-component-xl);
      {% else %}
        --component-spacing: var(--spacing-component-md);
    {% endcase %}

    padding: var(--component-spacing);
    gap: calc(var(--component-spacing) * 0.75);
  }
{% endstyle %}
```

## Accessibility Integration

### Focus Management with Tokens

```css
/* Focus ring system using tokens */
.focusable-element {
  outline: none;
  transition: box-shadow var(--transition-fast);
}

.focusable-element:focus {
  box-shadow:
    0 0 0 var(--focus-ring-offset) var(--surface-primary),
    0 0 0 calc(var(--focus-ring-offset) + var(--focus-ring-width)) var(--focus-ring-color);
}

/* High contrast mode adjustments */
@media (prefers-contrast: high) {
  .focusable-element:focus {
    outline: var(--focus-ring-width) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }
}
```

## Performance Optimization

### CSS Custom Property Efficiency

```liquid
{% style %}
  /* ✅ Efficient: Group related token assignments */
  .component-{{ unique }} {
    --component-bg: {{ block.settings.bg_color | default: 'var(--surface-primary)' }};
    --component-text: {{ block.settings.text_color | default: 'var(--text-primary)' }};
    --component-accent: {{ block.settings.accent_color | default: 'var(--brand-primary-500)' }};

    /* Apply all tokens at once */
    background: var(--component-bg);
    color: var(--component-text);
    border-color: var(--component-accent);
  }

  /* ❌ Inefficient: Repeated token lookups */
  .component-{{ unique }} {
    background: {{ block.settings.bg_color | default: 'var(--surface-primary)' }};
  }
  .component-{{ unique }}__element {
    color: {{ block.settings.bg_color | default: 'var(--surface-primary)' }};
  }
{% endstyle %}
```

## Migration Guide

### Converting Existing Components

**Before (Inconsistent):**
```liquid
{% style %}
  .hero-{{ unique }} {
    padding: 40px 20px;
    background: #ffffff;
    color: #333333;
    border-radius: 8px;
  }
{% endstyle %}
```

**After (Design Token System):**
```liquid
{% style %}
  .hero-{{ unique }} {
    --hero-bg: {{ section.settings.bg_color | default: 'var(--surface-primary)' }};
    --hero-text: {{ section.settings.text_color | default: 'var(--text-primary)' }};

    background: var(--hero-bg);
    color: var(--hero-text);
    padding: var(--spacing-component-lg) var(--spacing-component-md);
    border-radius: var(--border-radius-lg);
  }
{% endstyle %}
```

## Benefits of This System

### 1. **Consistency**
- Unified spacing scale across all components
- Consistent color tokens and naming
- Standardized typography and border radius values

### 2. **Maintainability**
- Single source of truth for design values
- Easy theme-wide updates by changing token values
- Clear inheritance hierarchy (primitive → semantic → component)

### 3. **Accessibility**
- Built-in focus management tokens
- High contrast mode support
- Reduced motion preferences respected

### 4. **Developer Experience**
- Predictable naming conventions
- IntelliSense support for token names
- Clear documentation and usage examples

### 5. **Shopify Integration**
- Seamless merchant customization
- Fallback tokens ensure components always work
- Performance optimized for Shopify's rendering

## Validation Checklist

- [ ] ✅ All components use semantic tokens, not primitives directly
- [ ] ✅ Shopify setting integration provides token fallbacks
- [ ] ✅ Focus states use design token system
- [ ] ✅ Responsive adjustments use token-based media queries
- [ ] ✅ Dark mode and high contrast support implemented
- [ ] ✅ Component tokens reference semantic tokens appropriately
- [ ] ✅ Performance optimized with grouped token assignments
- [ ] ✅ Accessibility tokens integrated throughout
- [ ] ✅ Schema settings provide merchant token customization
- [ ] ✅ Migration path documented for existing components

This unified design token system provides the foundation for scalable, consistent, and accessible Shopify theme development while maintaining the flexibility merchants expect.