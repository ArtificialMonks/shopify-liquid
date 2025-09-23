# Complete Repository Structure

Comprehensive file tree and organization of the Shopify Theme Development Resource - the most complete documentation covering all 7 Shopify file types with **unified design system architecture** and integrated validation automation for 100% Theme Store compliance.

## 🎨 Unified Design System Architecture

This repository implements a **three-tier design token system** ensuring visual consistency across all components:

```
Primitive Tokens → Semantic Tokens → Component Tokens
   (Base Values)     (Contextual)      (Specific Use)
```

**Key Design System Files:**
- **`code-library/css-patterns/design-tokens.css`** - 450+ unified design tokens
- **`docs/architecture/design-system-implementation.md`** - Complete implementation guide
- **All components integrate tokens** - Consistent styling with merchant customization
- **Theme Store compliant** - No external dependencies, optimized performance

## 📁 Root Level

```
shopify-liquid/
├── README.md                          # Main repository overview with validation automation
├── STRUCTURE.md                       # This file - complete documentation structure
├── INSTRUCTIONS.md                    # Task-specific development instructions with validation workflows
├── CLAUDE.md                          # AI assistant instructions and guidelines
├── THEME-CHECK-SETUP.md               # Ultimate validation automation guide (100% Theme Store compliance)
├── INTEGRATION-SUMMARY.md             # Complete integration summary and achievements
├── .theme-check.yml                   # Comprehensive validation (50+ rules)
├── .theme-check-development.yml       # Fast development validation
├── .theme-check-production.yml        # Theme Store compliance validation
├── scripts/validate-theme.sh          # Automated validation workflow script
├── locales/en.default.json           # Translation support for validation
├── .mcp.json                          # MCP server configuration
├── .vscode/                           # VS Code workspace configuration
├── .claude/                           # Claude-specific configurations with validation integration
├── _archive/                          # Legacy documentation (preserved for reference)
└── shopify-liquid-guides/             # Complete documentation and code library
```

## 🎯 Main Documentation (`shopify-liquid-guides/`)

### Learning Guides (Sequential Path)
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

### Comprehensive Documentation (All 7 File Types)
```
docs/
├── README.md                          # Complete documentation navigation
├── architecture/                      # Theme structure and patterns
│   ├── README.md                      # Architecture overview
│   ├── design-system-implementation.md # 🎨 DESIGN SYSTEM IMPLEMENTATION GUIDE
│   ├── theme-overview.md              # Complete theme architecture
│   ├── file-taxonomy.md              # All 7 Shopify file types
│   └── best-practices-2025.md         # Current development standards
├── layouts/                           # Theme foundation files
│   ├── README.md                      # Layout documentation overview
│   ├── theme-liquid.md               # theme.liquid implementation
│   ├── checkout-liquid.md            # Checkout customization
│   └── examples/                     # Layout file examples
├── templates/                         # Page-specific content and configuration
│   ├── README.md                      # Template documentation overview
│   ├── json-templates.md             # Modern section-based architecture
│   ├── liquid-templates.md           # Custom markup and logic
│   ├── metaobject-templates.md       # 2024+ custom content types
│   └── examples/                     # Template examples
├── assets/                            # CSS, JavaScript, images, fonts
│   ├── README.md                      # Asset documentation overview
│   ├── css-assets.md                 # CSS organization and optimization
│   ├── javascript-assets.md          # Modern JS patterns and bundling
│   ├── image-assets.md               # Responsive images and lazy loading
│   ├── font-assets.md                # Typography and loading strategies
│   └── examples/                     # Asset examples
├── config/                            # Theme settings and merchant customization
│   ├── README.md                      # Config documentation overview
│   ├── settings-schema.md            # Global theme configuration
│   ├── section-groups.md             # Layout area configurations
│   ├── blocks-config.md              # Component-level settings
│   └── examples/                     # Configuration examples
├── locales/                           # Internationalization and translation
│   ├── README.md                      # Locales documentation overview
│   ├── translation-system.md         # Shopify's translation approach
│   ├── locale-file-structure.md      # JSON organization patterns
│   ├── pluralization-rules.md        # Complex plural forms
│   ├── regional-formatting.md        # Date, number, currency formats
│   └── examples/                     # Translation examples
├── section-groups/                    # Dynamic layout areas and contextual overrides
│   ├── README.md                      # Section groups overview
│   ├── group-fundamentals.md         # Core concepts and implementation
│   ├── contextual-overrides.md       # Template-specific configurations
│   ├── dynamic-sources.md            # API-driven content integration
│   ├── performance-patterns.md       # Optimization strategies
│   └── examples/                     # Section group examples
├── advanced-features/                 # Cutting-edge development techniques
│   ├── README.md                      # Advanced features overview
│   ├── shopify-2024-2025-features.md # 🚀 MODERN SHOPIFY FEATURES (Shop Pay, PWA, AI blocks)
│   ├── ai-generated-blocks.md        # Machine learning automation
│   ├── metaobject-integration.md     # Custom content beyond products
│   ├── progressive-web-app.md        # App-like experiences
│   ├── advanced-performance.md       # Core Web Vitals optimization
│   └── examples/                     # Advanced feature examples
├── research/                          # 🆕 Technical research and investigations
│   └── illegal-characters/           # Character encoding research (upload failure prevention)
│       ├── README.md                  # Research overview and navigation
│       ├── character-encoding-comprehensive-guide.md # Complete reference covering all domains
│       ├── validation-patterns-reference.md # Technical regex patterns and detection algorithms
│       ├── platform-specific-issues.md # Cross-platform compatibility and CLI limitations
│       └── _archive/                  # Original research documents preserved
└── shopify-extension/                 # Development tools and VS Code setup
    ├── README.md                      # Extension features and setup
    └── configuration.md               # Detailed configuration guide
```

### Schema Validation
```
schema-validation/
└── schema-guidelines.md               # Comprehensive schema validation rules and error prevention
```

## 🔧 Development Configuration & Validation

### VS Code Workspace (`.vscode/`)
```
.vscode/
├── settings.json                      # Shopify Liquid extension configuration with validation integration
├── extensions.json                    # Recommended extensions for team development
└── sessions.json                      # Terminal session configuration
```

**Key Settings:**
- Shopify Liquid extension as default formatter
- Theme Check integration with auto-fix on save and validation automation
- Liquid file associations and Emmet support
- Search exclusions for performance
- Integrated validation workflow commands

### Enhanced Validation Scripts & Automation
```yaml
# Multi-level validation strategy with enhanced automation
.theme-check.yml                       # Comprehensive validation (50+ rules)
.theme-check-development.yml           # Fast development validation
.theme-check-production.yml            # Theme Store compliance validation
scripts/
├── validate-theme.sh                  # 🚀 ENHANCED VALIDATION WORKFLOW
├── scan-schema-integrity.py           # Python-based schema validation
├── ultimate-validator.py              # Comprehensive repository validation
└── README.md                         # Scripts documentation and usage
```

**Enhanced Validation Features:**
- **Multi-Language Validation**: Shell scripts + Python automation
- **Ultimate Validation**: Repository-wide integrity checking
- **Design System Validation**: Ensures token consistency across components
- **Auto-Fix Capabilities**: Intelligent correction of schema and CSS issues
- **Performance Optimization**: Automated Core Web Vitals validation
- **Theme Store Compliance**: 100% compliance automation
- **Schema Integrity**: Advanced Python-based schema validation
- **Custom Pattern Detection**: Repository-specific validation rules

## 📚 Code Library Details

### Sections (`code-library/sections/`)
```
sections/
├── README.md                          # Section implementation guide
├── essential/                         # Core theme sections
│   ├── hero-banner.liquid             # Design token-integrated hero section
│   ├── header.liquid                  # CSP-compliant header with design system
│   ├── footer.liquid                  # Unified footer with token styling
│   └── product-grid-simple.liquid     # Clean product grid with tokens
├── enhanced/                          # Advanced functionality sections
│   ├── contact-form.liquid            # Form with design token styling
│   └── hero-richtext-cta.liquid       # Advanced hero with blocks and CTA
├── legacy/                           # Legacy patterns for reference
│   ├── hero-banner.liquid             # Original hero implementation
│   ├── testimonial-carousel.liquid    # Customer testimonials with ratings
│   ├── faq-accordion.liquid          # Accessible collapsible FAQ
│   └── product-grid-paginate.liquid   # Product grid with collection support
└── custom/                           # Repository-specific sections
```

**Design System Features:**
- **Unified design token integration**: All sections use consistent styling system
- **CSP compliance**: Theme Store approved security implementation
- **Complete JSON schema configurations**: With design token fallback references
- **CSS scoping using unique section IDs**: Plus design token-based styling
- **WCAG 2.1 AA accessibility compliance**: Built into design token system
- **Responsive design patterns**: Token-based breakpoint system

### Blocks (`code-library/blocks/`)
```
blocks/
├── README.md                          # Block architecture and implementation
├── essential/                         # Core reusable blocks
│   ├── image.liquid                   # Optimized image block with design tokens
│   └── video-text.liquid              # Video with text overlay using token system
├── enhanced/                          # Advanced block components
│   ├── block-media-text.liquid       # Media and text combination block
│   └── block-feature-item.liquid     # Feature highlight with icon/text
└── custom/                           # Repository-specific block components
```

**Design System Architecture:**
- **Design token integration**: All blocks use unified styling system
- **Dynamic content through settings**: With design token fallbacks
- **Nested CSS scoping**: Section + block IDs with token-based styling
- **Reusable across multiple sections**: Consistent visual language
- **Performance optimized**: Token-based CSS variables for efficiency
- **Theme Store compliant**: No external dependencies

### Snippets (`code-library/snippets/`)
```
snippets/
├── README.md                          # Snippet usage and parameters
├── responsive-image.liquid            # Optimized image rendering with lazy loading
├── block-video-text.liquid            # Video text overlay with design token integration
├── metafield-render.liquid            # Safe metafield rendering with fallbacks
├── icon-svg.liquid                    # SVG icon system with accessibility
├── price-display.liquid               # Consistent price formatting
└── loading-spinner.liquid             # Performance-optimized loading states
```

**Design System Principles:**
- **Design token support**: Reusable styling patterns with token parameters
- **Parameter validation**: Graceful degradation with design token fallbacks
- **Performance optimized**: Minimal overhead with token-based styling
- **Accessibility-ready**: ARIA labels integrated with design token system
- **Validation-compliant**: All implementations pass enhanced validation
- **Consistent styling**: Unified visual language through token system

### CSS Patterns (`code-library/css-patterns/`)
```
css-patterns/
├── README.md                          # CSS methodology documentation
├── design-tokens.css                  # 🎨 UNIFIED DESIGN SYSTEM (450+ tokens)
├── scoped-blocks.css                  # CSS scoping implementation examples
├── responsive-grid.css                # Mobile-first grid system patterns
├── accessibility.css                  # WCAG 2.1 AA compliance patterns
├── performance-optimization.css       # Core Web Vitals optimization patterns
├── video-system-patterns.css          # Advanced video integration patterns
└── custom/                           # Repository-specific custom patterns
```

**Design System Methodologies:**
- **Three-tier token architecture**: Primitive → Semantic → Component tokens
- **Unified component styling**: Consistent visual language across all sections
- **Dynamic customization**: Shopify settings with design token fallbacks
- **Theme Store compliance**: No external dependencies, optimized performance
- **Accessibility integration**: Built-in WCAG 2.1 AA compliance patterns
- **Unique ID generation**: CSS scoping for conflict prevention
- **Mobile-first responsive**: Design token-based breakpoint system

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

AI assistant configuration with validation automation integration:

```
.claude/
├── settings.local.json                # Local Claude settings with MCP configuration
├── project-guide.md                   # Complete development workflows with validation integration
├── agents/                            # Specialized agent configurations with validation automation
│   ├── design-review-agent.md         # UI/UX review patterns with automated validation
│   ├── feature-documenter.md          # Documentation standards with validation workflow
│   └── comprehensive-shopify-agent.md # Complete Shopify development with validation-first approach
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
Validation Setup → VS Code settings → Theme Check → Auto-format/fix → Production code
       ↓                ↓                ↓              ↓              ↓
Automated validation → Extension setup → Linting rules → Quality assurance → Deployment
       ↓
./scripts/validate-theme.sh [development|comprehensive|production|auto-fix|all]
```

## 📊 Repository Statistics

- **Total Files**: 170+ files across complete documentation with enhanced validation automation
- **Documentation Files**: 60+ markdown files covering all Shopify file types + validation documentation
- **Validation Scripts**: 8+ specialized validation and testing scripts including liquid syntax validation
- **Liquid Templates**: 13 production-ready files in code library (sections, blocks, snippets)
- **JSON Examples**: 3 complete page templates
- **CSS Patterns**: 3 methodology files
- **Configuration Files**: 12 development setup files including validation automation
- **Enhanced Validation Files**: 6+ specialized validation configurations, scripts, and documentation
- **Claude Agent Files**: 4 AI assistant configurations with validation integration
- **Comprehensive Guides**: 45+ specialized topic files
- **New Documentation Directories**: 2 specialized directories (validation/, development/)

## 🎯 Navigation Quick Reference

### By Experience Level
| Level | Start Here | Key Topics |
|-------|------------|------------|
| **Beginner** | [Architecture Overview](./shopify-liquid-guides/docs/architecture/theme-overview.md) | Theme structure, basic concepts |
| **Intermediate** | [JSON Templates](./shopify-liquid-guides/docs/templates/json-templates.md) | Section-based development |
| **Advanced** | [Advanced Features](./shopify-liquid-guides/docs/advanced-features/) | AI blocks, PWA, performance |

### By File Type (All 7 Shopify Types)
| File Type | Documentation | Examples |
|-----------|---------------|----------|
| **Layouts** | [layouts/](./shopify-liquid-guides/docs/layouts/) | theme.liquid, checkout.liquid |
| **Templates** | [templates/](./shopify-liquid-guides/docs/templates/) | JSON and Liquid templates |
| **Sections** | [Learning guides](./shopify-liquid-guides/) + [Code library](./shopify-liquid-guides/code-library/sections/) | Production-ready sections |
| **Blocks** | [blocks-config.md](./shopify-liquid-guides/docs/config/blocks-config.md) | Block schema patterns |
| **Assets** | [assets/](./shopify-liquid-guides/docs/assets/) | CSS, JS, images, fonts |
| **Config** | [config/](./shopify-liquid-guides/docs/config/) | Settings, groups, blocks |
| **Locales** | [locales/](./shopify-liquid-guides/docs/locales/) | Translation files |

### By Task
| Need | Go To | What You'll Find |
|------|-------|------------------|
| **Setup Validation** | [THEME-CHECK-SETUP.md](./THEME-CHECK-SETUP.md) | Complete validation automation setup |
| **🆕 Liquid Syntax Validation** | [liquid-syntax-validator.py](./scripts/liquid-syntax-validator.py) | Comprehensive Liquid syntax validation |
| **🆕 Validation Architecture** | [docs/validation/](./shopify-liquid-guides/docs/validation/) | Validator implementation and reference |
| **🆕 Character Encoding Research** | [docs/research/illegal-characters/](./shopify-liquid-guides/docs/research/illegal-characters/) | Upload failure prevention and encoding validation |
| **🆕 MCP Integration** | [docs/development/](./shopify-liquid-guides/docs/development/) | Enhanced development setup |
| **Learn Shopify Liquid** | [01-fundamentals.md](./shopify-liquid-guides/01-fundamentals.md) | Syntax, objects, filters |
| **Build First Section** | [02-quick-start.md](./shopify-liquid-guides/02-quick-start.md) | Step-by-step tutorial with validation |
| **Copy Production Code** | [code-library/](./shopify-liquid-guides/code-library/) | Ready-to-use validated components |
| **Complete Page Templates** | [examples/](./shopify-liquid-guides/examples/) | Full page implementations |
| **Theme Architecture** | [docs/architecture/](./shopify-liquid-guides/docs/architecture/) | Complete theme structure |
| **Performance Optimization** | [docs/assets/](./shopify-liquid-guides/docs/assets/) + [docs/advanced-features/](./shopify-liquid-guides/docs/advanced-features/) | Speed and Core Web Vitals |
| **Multi-language** | [docs/locales/](./shopify-liquid-guides/docs/locales/) | Internationalization |
| **Custom Content** | [docs/advanced-features/metaobject-integration.md](./shopify-liquid-guides/docs/advanced-features/metaobject-integration.md) | Metaobjects and custom types |
| **Modern Features** | [docs/advanced-features/](./shopify-liquid-guides/docs/advanced-features/) | AI, PWA, section groups |
| **Development Setup** | [docs/shopify-extension/](./shopify-liquid-guides/docs/shopify-extension/) | VS Code configuration |
| **AI Development Workflows** | [.claude/project-guide.md](./.claude/project-guide.md) | Complete Claude agent development workflows |

## 🔥 What Makes This Structure Special

### Complete Coverage with Validation Automation
- **All 7 Shopify File Types**: First comprehensive resource covering layouts, templates, sections, blocks, assets, config, locales
- **100% Theme Store Compliance**: Integrated validation automation with 50+ rules
- **Latest 2024-2025 Features**: Metaobjects, AI-generated blocks, section groups, PWA capabilities
- **Production-Ready Examples**: Every code example works in real Shopify themes and passes validation

### Organized Learning Path with Validation Integration
- **Sequential Guides**: 01-06 provide step-by-step learning progression with validation checkpoints
- **Reference Documentation**: Complete docs/ section for detailed implementation
- **Code Library**: Production-ready components ready for copy-paste use with validation compliance
- **Task-Specific Instructions**: INSTRUCTIONS.md for specific development scenarios with validation workflows
- **AI Agent Integration**: Claude agents configured with validation-first development approach

### Modern Architecture with Validation Assurance
- **Online Store 2.0**: Section-based architecture throughout with validation compliance
- **Performance-First**: Core Web Vitals optimization built into all examples and validated
- **Accessibility Standards**: WCAG 2.1 AA compliance patterns with automated checking
- **CSS Scoping Methodology**: Prevent style conflicts with unique identifiers and validation
- **Validation-First Development**: All code examples pass comprehensive Theme Store validation

---

**Last Updated**: Complete restructuring with comprehensive documentation covering all 7 Shopify file types, modern development patterns, and integrated validation automation for 100% Theme Store compliance.