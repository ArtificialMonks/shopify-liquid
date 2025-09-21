# Custom CSS Patterns Directory

**Custom-made CSS methodologies and patterns for this repository**

## Purpose

This directory contains custom-developed CSS patterns and methodologies that are:
- **Repository-specific**: Built for this project's unique requirements
- **Scoping-focused**: Prevent style collisions between component instances
- **Performance-optimized**: Efficient CSS with minimal overhead

## Structure

```
css-patterns/custom/
├── README.md                    # This documentation
├── instance-scoping.css         # Advanced CSS scoping patterns
├── responsive-utilities.css     # Custom responsive design utilities
└── [future patterns]           # Additional custom CSS methodologies
```

## Core Scoping Methodology

Our custom CSS scoping pattern prevents style collisions:

```liquid
{%- assign uid = block.id | replace: '_', '' | downcase -%}

{% style %}
  .component-{{ uid }} {
    /* Component-specific styles with unique ID */
  }
  
  .component__element-{{ uid }} {
    /* BEM-style element naming with scoping */
  }
  
  .component__element--modifier-{{ uid }} {
    /* BEM modifier with scoping */
  }
{% endstyle %}
```

## Pattern Categories

### 1. Instance Scoping
- **Purpose**: Prevent CSS conflicts between multiple instances
- **Usage**: All blocks and sections with repeatable content
- **Implementation**: `block.id` or `section.id` suffix generation

### 2. Responsive Utilities
- **Purpose**: Consistent breakpoint and sizing systems
- **Breakpoints**: Mobile-first with 750px desktop threshold
- **Usage**: Typography scaling, layout adjustments, spacing

### 3. Animation Patterns
- **Purpose**: CSS-only effects with accessibility compliance
- **Features**: `prefers-reduced-motion` support, progressive enhancement
- **Usage**: Hover effects, scroll-triggered animations

## Development Guidelines

When creating custom CSS patterns:
1. **Always scope with unique IDs** - Never use global classes for component-specific styles
2. **Mobile-first approach** - Base styles for mobile, desktop overrides at 750px+
3. **Accessibility compliance** - Respect `prefers-reduced-motion: reduce`
4. **Performance considerations** - Minimize CSS size, use efficient selectors
5. **Documentation** - Include usage examples and integration notes

## Usage Example

```liquid
{%- assign uid = section.id | replace: '_', '' | downcase -%}

{% style %}
  .custom-hero-{{ uid }} {
    /* Apply custom patterns */
    @media (min-width: 750px) {
      /* Desktop overrides */
    }
  }
{% endstyle %}

<section class="custom-hero-{{ uid }}" {{ section.shopify_attributes }}>
  <!-- Content with scoped styling -->
</section>
```

## Integration with Theme Architecture

Custom CSS patterns integrate with:
- **Shopify's Online Store 2.0** - Section and block architecture
- **Theme Check validation** - Pass all style-related checks  
- **Performance budgets** - Minimal CSS overhead per component
- **Accessibility standards** - WCAG 2.1 AA compliance

## Reference Documentation

- **CSS Scoping Guide**: `../../04-blocks-and-css-scoping.md`
- **Performance Guidelines**: `../../docs/architecture/best-practices-2025.md`
- **Accessibility Patterns**: `../../05-performance-and-accessibility.md`