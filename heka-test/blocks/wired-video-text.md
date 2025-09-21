# Advanced Video + Text Block - Component Wiring Documentation

## Overview

The `advanced_video_text.liquid` block is a sophisticated Shopify theme block that creates dynamic video and text layouts with extensive customization options. This document maps all the connected files and dependencies for this component.

## Core Architecture

### Primary Component Files

#### 1. **Block Definition**
- **File**: `/blocks/advanced_video_text.liquid`
- **Type**: Shopify Theme Block
- **Purpose**: Schema definition and snippet delegation
- **Key Function**: Acts as a wrapper that defines the block's settings schema and renders the implementation snippet

```liquid
{%- render 'block-video-text', block: block -%}
```

#### 2. **Implementation Snippet**
- **File**: `/snippets/block-video-text.liquid`
- **Type**: Liquid Snippet
- **Purpose**: Complete rendering logic and CSS implementation
- **Key Function**: Contains all the visual rendering, styling, and business logic

## Component Dependencies

### Direct Dependencies

#### Schema Integration
- **Block Type**: `"advanced_video_text"` or `"@theme"`
- **Integration Method**: Can be used in any section that accepts theme blocks
- **Schema Location**: Embedded in `/blocks/advanced_video_text.liquid` (lines 20-527)

#### Asset Dependencies
- **Font Loading**: Dynamic font loading via `{{ block.settings.heading_font | font_face }}`
- **Video Sources**: Multiple source support for cross-browser compatibility
- **Image Assets**: Poster images and background images loaded via Shopify's `image_url` filter

### Connected Sections

#### 1. **Custom Section**
- **File**: `/sections/custom-section.liquid`
- **Connection Type**: Accepts `@theme` blocks (line 46)
- **Usage**: Can contain the advanced_video_text block as a child block

#### 2. **Group Block**
- **File**: `/blocks/group.liquid`
- **Connection Type**: Layout wrapper for theme blocks
- **Usage**: Can contain and arrange multiple advanced_video_text blocks

## Styling Architecture

### Instance-Scoped CSS
- **Methodology**: CSS classes are suffixed with unique block.id
- **Example**: `.video-text-{{ uid }}` where `uid = block.id | replace: '_', '' | downcase`
- **Purpose**: Prevents style collisions between multiple block instances

### CSS Structure
```liquid
{% style %}
  .video-text-{{ uid }} { /* Main container */ }
  .video-text__inner-{{ uid }} { /* Layout container */ }
  .video-text__text-{{ uid }} { /* Text content area */ }
  .video-text__video-{{ uid }} { /* Video container */ }
  .video-text__heading-{{ uid }} { /* Heading styles */ }
  .video-text__body-{{ uid }} { /* Body text styles */ }
{% endstyle %}
```

### Background Priority System
1. **Background Video** (Highest Priority)
2. **Background Image** (Medium Priority)
3. **Background Color** (Fallback)

## Data Flow

### Settings Configuration
The block accepts 70+ settings organized into categories:

#### Content Settings
- `heading` - Main heading text
- `heading_tag` - Semantic heading level (h2, h3, h4)
- `body` - Rich text content
- `video_alt` - Accessibility description

#### Typography Settings
- `heading_font` - Font picker for heading
- `body_font` - Font picker for body text
- `heading_size` - Font size (16-72px)
- `text_color` - Color picker

#### Layout & Positioning
- `layout_style` - Overall arrangement (side_by_side, stacked, overlay, floating, custom_grid)
- `video_position` - Video placement (left, center, right, top, bottom)
- `text_position` - Text placement including overlay options
- `mobile_layout` - Mobile-specific layout overrides

#### Video Settings
- `video_file` - Main video upload
- `video_poster` - Poster image
- `autoplay`, `show_controls`, `loop` - Playback options
- `aspect_ratio` - Video dimensions (16:9, 4:3, 1:1, 21:9, custom)

#### Background Settings
- `bg_video` - Background video file
- `bg_image` - Background image
- `bg_color` - Fallback background color
- `bg_size` - Background sizing (full_screen, half_screen, section_only, custom)

#### Effects & Animations
- `enable_hover_effects` - Toggle interactive effects
- `video_hover_effect` - Video interaction styles
- `text_hover_effect` - Text interaction styles
- `enable_scroll_animations` - Scroll-triggered animations
- `scroll_animation_style` - Animation type (fade_in, slide_up, zoom_in, stagger)

### Rendering Process

1. **Unique ID Generation**: `block.id` processed to create CSS-safe identifier
2. **Aspect Ratio Calculation**: Video dimensions calculated based on settings
3. **Background Priority Logic**: Determines which background type to render
4. **CSS Generation**: Instance-scoped styles generated inline
5. **HTML Structure**: Semantic markup with accessibility features
6. **Progressive Enhancement**: CSS-only effects with reduced motion support

## Integration Patterns

### Section Integration
Any section that accepts theme blocks can include this component:

```json
{
  "blocks": [{ "type": "@theme" }]
}
```

### Block Usage in Sections
```liquid
{% content_for 'blocks' %}
```

### Direct Snippet Usage (Alternative)
```liquid
{% render 'block-video-text', block: block, section: section %}
```

## Technical Constraints

### Schema Validation
- **Range Step Rule**: All range settings comply with `(max-min)/step ≤ 101`
- **Setting Types**: Only Shopify-standard setting types used
- **Background Priority**: Implemented via Liquid logic, not CSS

### Performance Optimizations
- **Font Loading**: Optimized with `font_face` filter
- **Image Sizing**: Responsive images with appropriate widths
- **CSS Scope**: Instance-specific classes prevent global conflicts
- **Reduced Motion**: Full `prefers-reduced-motion` support

### Accessibility Features
- **Semantic HTML**: Proper heading hierarchy with configurable heading tags
- **ARIA Labels**: Video elements include descriptive labels
- **Focus States**: Keyboard navigation support
- **Reduced Motion**: Animation respects user preferences

## File Dependencies Summary

```
advanced_video_text.liquid (Block Definition)
├── snippets/block-video-text.liquid (Implementation)
├── sections/custom-section.liquid (Host Section)
├── blocks/group.liquid (Layout Wrapper)
└── Shopify Asset Pipeline
    ├── Font Assets (Dynamic Loading)
    ├── Video Files (Settings-driven)
    └── Image Assets (Poster/Background)
```

## Usage Examples

### Theme Editor Integration
1. Add to any section with `{"type": "@theme"}` block support
2. Configure through Shopify theme editor
3. Customize layout, typography, and effects through settings

### Developer Integration
1. Include in section blocks array
2. Access via `{% content_for 'blocks' %}`
3. Custom styling through CSS variables or class targeting

## Version Information
- **Component Version**: 1.0.0
- **Shopify Compatibility**: All Shopify themes
- **Last Updated**: January 2025
- **Theme Check**: Compliant
- **WCAG**: 2.1 AA compliant

## Component Scope
This component is fully self-contained with no external JavaScript dependencies. All functionality is achieved through:
- Liquid templating for data processing
- CSS for styling and animations
- HTML5 video for media playback
- CSS custom properties for dynamic styling

The component follows the repository's CSS scoping methodology to ensure it can be safely used alongside other components without style conflicts.