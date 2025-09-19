# Repository Structure

Complete file tree and organization of the Shopify Liquid Development Guide.

## 📁 Root Level

```
shopify-liquid/
├── README.md                          # Main repository overview and quick start
├── STRUCTURE.md                       # This file - complete documentation structure
├── CLAUDE.md                          # AI assistant instructions and guidelines
├── .theme-check.yml                   # Theme Check linting configuration
├── .mcp.json                          # MCP server configuration
├── .vscode/                           # VS Code workspace configuration
├── .claude/                           # Claude-specific configurations
├── _archive/                          # Legacy documentation (preserved for reference)
└── shopify-liquid-guides/             # Main documentation and code library
```

## 🎯 Core Documentation (`shopify-liquid-guides/`)

### Learning Path (Sequential)
```
shopify-liquid-guides/
├── README.md                          # Entry point with navigation and philosophy
├── 01-fundamentals.md                 # Liquid syntax, objects, filters, control flow
├── 02-quick-start.md                  # Step-by-step implementation walkthrough
├── 03-sections-and-schema.md          # Section development and schema configuration
├── 04-blocks-and-css-scoping.md       # CSS methodology and block patterns
├── 05-performance-and-accessibility.md # Optimization and WCAG compliance
└── 06-troubleshooting.md              # Common issues and debugging
```

### Production Code Library
```
code-library/
├── README.md                          # Code library overview and usage
├── sections/                          # Complete section templates
├── blocks/                            # Reusable block components
├── snippets/                          # Utility functions and helpers
└── css-patterns/                      # CSS methodologies and patterns
```

### Complete Examples
```
examples/
├── README.md                          # Template usage and customization guide
├── complete-homepage.json             # Full homepage with hero, products, testimonials
├── product-page-sections.json         # Enhanced product page layout
└── collection-layout.json             # Collection page with filtering and features
```

### Tool Documentation
```
docs/
├── README.md                          # Documentation overview
└── shopify-extension/                 # VS Code extension integration
    ├── README.md                      # Extension features and setup
    └── configuration.md               # Detailed configuration guide
```

## 🔧 Development Configuration

### VS Code Workspace (`.vscode/`)
```
.vscode/
├── settings.json                      # Shopify Liquid extension configuration
├── extensions.json                    # Recommended extensions for team
└── sessions.json                      # Terminal session configuration
```

**Key Settings:**
- Shopify Liquid extension as default formatter
- Theme Check integration with auto-fix on save
- Liquid file associations and Emmet support
- Search exclusions for performance

### Theme Check Configuration (`.theme-check.yml`)
```yaml
# Optimized for documentation repository
enabled: true
root: "."
exclude: ["node_modules/**", "_archive/**", ".git/**"]
```

**Rule Highlights:**
- Security checks for header modifications
- Performance limits (100KB assets)
- Disabled template requirements for code library
- File-specific configurations for examples

## 📚 Code Library Details

### Sections (`code-library/sections/`)
```
sections/
├── README.md                          # Section implementation guide
├── hero-banner.liquid                 # Simple hero with heading/subtext
├── hero-richtext-cta.liquid           # Advanced hero with blocks and CTA
├── testimonial-carousel.liquid        # Customer testimonials with ratings
├── faq-accordion.liquid               # Accessible collapsible FAQ
└── product-grid-paginate.liquid       # Product grid with collection support
```

**Features:**
- Complete JSON schema configurations
- CSS scoping using unique section IDs
- WCAG 2.1 AA accessibility compliance
- Responsive design patterns

### Blocks (`code-library/blocks/`)
```
blocks/
├── README.md                          # Block architecture and implementation
├── block-media-text.liquid           # Media and text combination block
└── block-feature-item.liquid         # Feature highlight with icon/text
```

**Architecture:**
- Dynamic content through section settings
- Nested CSS scoping (section + block IDs)
- Reusable across multiple sections

### Snippets (`code-library/snippets/`)
```
snippets/
├── README.md                          # Snippet usage and parameters
├── responsive-image.liquid            # Optimized image rendering with lazy loading
└── metafield-render.liquid            # Safe metafield rendering with fallbacks
```

**Design Principles:**
- Parameter validation and graceful degradation
- Performance optimized with minimal overhead
- Accessibility-ready with proper ARIA labels

### CSS Patterns (`code-library/css-patterns/`)
```
css-patterns/
├── README.md                          # CSS methodology documentation
├── scoped-blocks.css                  # CSS scoping implementation examples
├── responsive-grid.css                # Mobile-first grid system patterns
└── accessibility.css                  # WCAG 2.1 AA compliance patterns
```

**Methodologies:**
- Unique ID generation for conflict prevention
- Mobile-first responsive design
- Color contrast and focus management
- Performance optimization patterns

## 📋 JSON Template Examples

### Complete Page Templates (`examples/`)
```
examples/
├── README.md                          # Template implementation guide
├── complete-homepage.json             # Homepage: hero + products + testimonials + FAQ
├── product-page-sections.json         # Product: details + reviews + recommendations
└── collection-layout.json             # Collection: banner + grid + features + FAQ
```

**Template Features:**
- Real content examples with actual copy
- Section order optimized for conversion
- Progressive disclosure and social proof
- Mobile and desktop responsive configurations

## 🏗 Archive Structure (`_archive/`)

Preserved legacy documentation for reference:

```
_archive/
├── shopify-liquid/                    # Original tutorial-style documentation
│   ├── README.md                      # Learning-focused guides
│   ├── 01-quick-start.md              # Basic implementation tutorials
│   ├── 02-section-schema.md           # Schema fundamentals
│   └── examples/                      # Basic code examples
└── shopify-liquid-gpt5/               # Original reference documentation
    ├── README.md                      # Copy-paste code snippets
    ├── fundamentals.md                # Syntax reference
    ├── blocks.md                      # Block patterns
    └── code-snippets/                 # Production code examples
```

## 🤖 Claude Configuration (`.claude/`)

AI assistant configuration for project continuity:

```
.claude/
├── settings.local.json                # Local Claude settings
├── agents/                            # Specialized agent configurations
│   ├── design-review-agent.md         # UI/UX review patterns
│   └── feature-documenter.md          # Documentation standards
└── commands/                          # Custom command definitions
    └── doc-features.md                # Feature documentation workflow
```

## 🔄 File Relationships

### Documentation Flow
```
README.md → shopify-liquid-guides/README.md → Individual guides (01-06)
                                            ↓
                                     code-library/ examples
                                            ↓
                                    Production implementation
```

### Code Integration
```
Sections ← use ← Blocks ← use ← Snippets
    ↓                              ↑
CSS Patterns ← scope ← unique IDs ← generate
```

### Development Workflow
```
VS Code settings → Theme Check → Auto-format/fix → Production code
       ↓                ↓              ↓              ↓
Extension setup → Linting rules → Quality assurance → Deployment
```

## 📊 Repository Statistics

- **Total Files**: 87 files
- **Documentation Files**: 23 markdown files
- **Liquid Templates**: 11 production-ready files
- **JSON Examples**: 3 complete page templates
- **CSS Patterns**: 3 methodology files
- **Configuration Files**: 5 development setup files

## 🎯 Navigation Quick Reference

| Need | Start Here |
|------|------------|
| **Learn Shopify Liquid** | [01-fundamentals.md](./shopify-liquid-guides/01-fundamentals.md) |
| **Build First Section** | [02-quick-start.md](./shopify-liquid-guides/02-quick-start.md) |
| **Copy Production Code** | [code-library/](./shopify-liquid-guides/code-library/) |
| **Complete Page Templates** | [examples/](./shopify-liquid-guides/examples/) |
| **Set Up VS Code** | [docs/shopify-extension/](./shopify-liquid-guides/docs/shopify-extension/) |
| **Debug Issues** | [06-troubleshooting.md](./shopify-liquid-guides/06-troubleshooting.md) |
| **CSS Methodology** | [04-blocks-and-css-scoping.md](./shopify-liquid-guides/04-blocks-and-css-scoping.md) |
| **Performance Optimization** | [05-performance-and-accessibility.md](./shopify-liquid-guides/05-performance-and-accessibility.md) |

---

**Last Updated**: Current structure as of VS Code extension integration and complete README implementation.