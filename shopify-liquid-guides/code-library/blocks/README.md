# Theme Blocks Library

**Production-ready, reusable Shopify Liquid block templates organized by category for maximum flexibility and maintainability.**

## 📚 Block Library Structure

Our comprehensive block library is organized into three categories based on functionality and use case:

### 🎯 Essential Blocks (`/essential`)
The 5 most critical blocks every Shopify theme needs:

| Block | Description | Key Features |
|-------|-------------|--------------|
| **text.liquid** | Rich text content with typography control | Headings, paragraphs, gradient text, responsive sizing |
| **image.liquid** | Responsive image with optimization | Lazy loading, srcset, mobile image, overlays |
| **button.liquid** | Versatile call-to-action button | Multiple styles, icons, animations, accessibility |
| **spacer.liquid** | Flexible spacing control | Desktop/mobile values, optional divider |
| **divider.liquid** | Visual separator with styles | Lines, icons, text, patterns, animations |

### 🕰️ Legacy Blocks (`/legacy`)
Traditional blocks for backward compatibility:

| Block | Description | Key Features |
|-------|-------------|--------------|
| **heading.liquid** | Simple heading block | H1-H6 tags, alignment, color |
| **paragraph.liquid** | Basic text paragraph | Font size, alignment, color |
| **video-embed.liquid** | YouTube/Vimeo embeds | Aspect ratios, autoplay, loop |
| **html.liquid** | Custom HTML injection | Direct HTML code input |
| **liquid.liquid** | Custom Liquid code | Access Shopify objects |

### 🚀 Advanced Blocks (`/advanced`)
Modern blocks for enhanced functionality:

| Block | Description | Key Features |
|-------|-------------|--------------|
| **accordion.liquid** | Collapsible content sections | Smooth animations, multiple items, accessibility |
| **countdown.liquid** | Timer for sales/events | Days/hours/minutes/seconds, expired handling |
| **testimonial.liquid** | Customer review display | Avatar, rating system, multiple layouts, shadow effects |
| **tabs.liquid** | Tabbed content interface | Horizontal/vertical tabs, smooth transitions, keyboard navigation |
| **progress-bar.liquid** | Visual progress indicator | Animated progress, custom colors, percentage labels |
| **icon-list.liquid** | List with custom icons | SVG icons, flexible layouts, hover effects |
| **comparison-table.liquid** | Feature comparison grid | Responsive tables, highlight columns, checkmarks |
| **sticky-banner.liquid** | Persistent notification | Top/bottom positioning, dismissible, call-to-action |
| **video-system.liquid** | 🎥 **Complete video system** | **YouTube/Vimeo/MP4/Shopify files, full background system, typography controls, grid layouts, animations, mobile optimization, accessibility features** |

## 🎥 **Complete Video System Block**

The `video-system.liquid` block is our most comprehensive block, providing a complete video solution with every feature you need for modern video experiences:

### Core Video Features
- **Multiple Video Sources**: YouTube, Vimeo, MP4 URLs, Shopify file uploads
- **Aspect Ratio Control**: 16:9, 4:3, 1:1, 21:9, 3:2, 9:16 with responsive handling
- **Video Positioning**: Center, top, bottom, left, right positioning within container
- **Scalability Options**: 50% to 150% scaling with smooth transitions
- **Quality Settings**: From 240p to 1080p with adaptive streaming
- **Playback Controls**: Autoplay, muted, loop, controls visibility, lazy loading

### Advanced Styling System
- **Video Effects**: Border radius, opacity, shadow with blur/spread/color controls
- **Shadow System**: None, small, medium, large, extra-large with custom colors
- **Fit Options**: Cover, contain, fill with object positioning

### Complete Background System
- **Solid Colors**: Full RGBA support with opacity controls
- **Linear/Radial Gradients**: Multi-stop gradients with angle controls
- **Background Images**: Position, size, repeat, attachment options
- **Blend Modes**: 12 blend modes including multiply, overlay, difference
- **Global Color Override**: Option to override theme colors with block-specific colors

### Full Typography Controls
- **Header Text**: Complete font control with family, size, weight, line height, letter spacing
- **Body Text**: Independent typography controls for descriptive content
- **Text Positioning**: Above, below, left, or right of video with flexible grid system
- **Text Effects**: Shadow controls (X, Y, blur, color), text transform, alignment options
- **Responsive Text**: Automatic scaling for mobile devices

### Flexible Layout System
- **Layout Types**: Stacked, side-by-side, custom 3x3 grid positioning
- **Grid Positioning**: 9-point positioning system for video and text content
- **Responsive Layouts**: Different layouts for mobile with orientation changes
- **Spacing Controls**: Padding, margin, gap controls with mobile variants

### Advanced Animations
- **Scroll Animations**: Fade, slide, zoom, rotate with duration/delay controls
- **Hover Effects**: Scale, lift, glow, rotate with smooth transitions
- **Parallax Scrolling**: Background and video parallax with performance optimization
- **Loading States**: Shimmer animation for loading content

### Mobile Optimization
- **Separate Mobile Layouts**: Stacked or reverse stacking for mobile
- **Mobile Typography**: Independent font sizes for mobile devices
- **Bandwidth Detection**: Automatic quality adjustment for slow connections
- **Touch Optimization**: Larger touch targets (88px) for accessibility
- **Mobile Background Images**: Different background images for mobile

### Accessibility & Performance
- **WCAG 2.1 AA Compliance**: Proper ARIA labels, keyboard navigation, focus management
- **Reduced Motion Support**: Respects user preferences for motion
- **Screen Reader Optimization**: Comprehensive screen reader support
- **Performance Features**: Lazy loading, intersection observer, hardware acceleration
- **High Contrast Mode**: Automatic adjustments for high contrast preferences

### Usage Example
```liquid
<!-- In your section schema -->
{
  "blocks": [
    {"type": "video-system"}
  ]
}
```

The video system block automatically handles all complexity while providing merchant-friendly controls in the theme editor.

## 🎯 **Understanding Theme Blocks**

**Theme blocks ARE standalone files** that live in the `/blocks` folder with their own `{% schema %}` tags. They differ fundamentally from section blocks:

### ✅ **Theme Blocks (Standalone Files)**
- **Location**: `/blocks` folder in theme root
- **Schema**: Has its own `{% schema %}` tag
- **Reusability**: Can be used across multiple sections
- **Nesting**: Can contain other blocks (hierarchical)
- **Saving**: CAN be saved directly in theme editor

## 🏗️ Block Architecture & Implementation

### CSS Scoping Pattern
Every block uses a unique ID for style isolation:

```liquid
{% assign unique = block.id | replace: '_', '' | downcase %}

{% style %}
  .block-name-{{ unique }} {
    /* Scoped styles prevent conflicts */
  }
{% endstyle %}
```

### Core Features
All blocks in this library include:

✅ **Production-Ready Code**
- Copy-paste ready Liquid templates
- Comprehensive `{% schema %}` definitions
- Theme Store compliant
- Performance optimized

✅ **Accessibility**
- WCAG 2.1 AA compliance
- Proper ARIA labels
- Keyboard navigation
- Screen reader support
- Focus indicators

✅ **Responsive Design**
- Mobile-first approach
- Standard Shopify breakpoints (749px)
- Touch-friendly (44px targets)
- Flexible layouts

✅ **Developer Experience**
- Clear documentation comments
- BEM naming with scoping
- CSS custom properties
- Consistent patterns

## 📖 How to Use These Blocks

### Installation

1. **Copy block files** to your theme's `/blocks` folder
2. **Each block is self-contained** with its own schema
3. **No additional setup required** - blocks are ready to use

### Using Blocks in Sections

#### Accept All Theme Blocks
```liquid
{% schema %}
{
  "name": "My Section",
  "blocks": [
    {"type": "@theme"}  // Accepts ALL theme blocks
  ]
}
{% endschema %}
```

#### Accept Specific Blocks
```liquid
{% schema %}
{
  "name": "Content Section",
  "blocks": [
    {"type": "text"},     // Only text blocks
    {"type": "image"},    // Only image blocks
    {"type": "button"}    // Only button blocks
  ]
}
{% endschema %}
```

#### Render Blocks in Section
```liquid
<section class="my-section">
  {% content_for 'blocks' %}
</section>
```

### Theme Block Architecture

**Theme blocks are NOT snippets** - they're standalone files with schemas:

```liquid
<!-- blocks/ultimate-video.liquid -->
{% assign unique = block.id | replace: '_', '' | downcase %}

{% style %}
  .ultimate-video-{{ unique }} {
    /* Block-specific styles */
  }
{% endstyle %}

<div class="ultimate-video-{{ unique }}" {{ block.shopify_attributes }}>
  <!-- Block content -->
</div>

{% schema %}
{
  "name": "Ultimate Video",
  "settings": [
    /* Block settings */
  ],
  "presets": [
    {"name": "Ultimate Video"}
  ]
}
{% endschema %}
```

## Section Integration Examples

### Using Theme Blocks in Sections

**Sections can accept theme blocks using `@theme` reference:**

```liquid
<!-- In your section file -->
<section class="section-with-blocks">
  {% content_for 'blocks' %}
</section>

{% schema %}
{
  "name": "Section with Theme Blocks",
  "blocks": [
    {"type": "@theme"},  // Accepts ALL theme blocks
    {"type": "@app"}     // Also accepts app blocks
  ],
  "presets": [
    {"name": "Section with Theme Blocks"}
  ]
}
{% endschema %}
```

### Targeted Theme Block Support

**Sections can also specify which theme blocks to accept:**

```liquid
{% schema %}
{
  "name": "Video Section",
  "blocks": [
    {"type": "ultimate-video"},  // Only accepts ultimate-video theme blocks
    {"type": "media-text"}       // Only accepts media-text theme blocks
  ]
}
{% endschema %}
```

## Architecture Comparison

### ✅ **Theme Blocks (Standalone Files)**
- **Location**: `/blocks` folder in theme root
- **Schema**: Has its own `{% schema %}` tag
- **Reusability**: Can be used across multiple sections
- **Nesting**: Can contain other blocks (hierarchical)
- **Saving**: CAN be saved directly in theme editor

### 📝 **Section Blocks (Schema Definitions)**
- **Location**: Defined within section files
- **Schema**: Defined in section's `{% schema %}` blocks array
- **Reusability**: Only within the section where defined
- **Nesting**: Cannot be nested (single level only)
- **Saving**: Part of the section file

### 🏗️ **Correct File Structure**

```
theme/
├── blocks/              ← Theme blocks (standalone files)
│   ├── ultimate-video.liquid (HAS {% schema %})
│   ├── media-text.liquid (HAS {% schema %})
│   └── feature-item.liquid (HAS {% schema %})
├── sections/
│   └── my-section.liquid (HAS {% schema %})
│       └── can reference theme blocks with {@type: "@theme"}
└── snippets/            ← Utility functions (different purpose)
    └── helper-function.liquid (NO {% schema %})
```

For detailed implementation patterns, see [04-blocks-and-css-scoping.md](../../04-blocks-and-css-scoping.md).