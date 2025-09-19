# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Core Execution Principles

Execute ALL research, analysis, and planning operations using parallel tool calls wherever technically feasible. This is non-negotiable for optimal performance.

**EXECUTION METHODOLOGY:**
1. **Parallel Task Execution**: Simultaneously execute all research, analysis, and planning tasks using parallel tool calls. Never execute sequentially what can be done in parallel.
2. **Critical Assessment Approach**: Apply rigorous, uncompromising evaluation standards. Identify genuine issues, architectural flaws, and implementation gaps without diplomatic softening. Act as a harsh critical evaluator who demands excellence.
3. **Evidence-Based Conclusions**: Every criticism must be backed by concrete evidence from codebase analysis or proven research findings, not assumptions or speculation.

**CORE PHILOSOPHY:** Simple, working solutions beat complex, broken architectures every time.

## Implementation Guidelines

When working with this Shopify Liquid documentation repository, prioritize practical, production-ready solutions that follow these principles:

1. **Theme Integration & Compatibility**: Ensure all Liquid code examples, CSS patterns, and schema configurations work seamlessly together and follow Shopify's current theme architecture. Verify that sections, blocks, and snippets integrate properly through the theme editor and render correctly on storefronts.

2. **Production-Ready & Theme Store Compliant**: Write Liquid code and CSS that can actually be deployed to live Shopify stores and passes Theme Store review standards. Use real implementations with proper performance optimization, accessibility compliance, and responsive design rather than simplified demos.

3. **Avoid Liquid Hallucination**: Only document Liquid syntax, objects, and filters that actually exist in Shopify's current API. Don't create examples with non-existent Liquid tags, fake object properties, or placeholder functionality that appears to work but doesn't exist in the Shopify ecosystem.

4. **Appropriate Complexity Level**: Choose the simplest Liquid patterns that meet merchant and developer needs. Avoid over-engineering with complex nested loops, unnecessary liquid logic, or premature CSS optimizations when straightforward section/block patterns will suffice.

5. **Clean, Maintainable Liquid**: Write clear, readable Liquid templates that theme developers can easily understand, customize, and extend. Prefer explicit, well-commented code with proper escaping and error handling over overly clever or deeply nested liquid logic.

6. **Development Efficiency Focus**: Select Liquid patterns and CSS methodologies that are both development-efficient (faster to implement and debug) and runtime-efficient (fast page loads, minimal CSS). Balance developer productivity with theme performance and merchant ease-of-use.

The goal is production-ready Liquid code and documentation that can be confidently used in live Shopify themes, maintained by theme developers, and extended without unnecessary complexity.

## Repository Overview

This is a **Shopify Liquid documentation repository** containing comprehensive guides, code examples, and best practices for building custom Shopify theme sections. The repository serves as both a learning resource and production code library with full VS Code development environment configuration.

**📁 Complete Structure**: See [STRUCTURE.md](./STRUCTURE.md) for detailed file tree and organization.

## Project Structure

The repository contains unified Shopify Liquid documentation, production code, and development configuration:

### 🚀 Development Environment (Root Level)
- `README.md` - Repository overview and quick start guide
- `STRUCTURE.md` - Complete file tree and navigation reference
- `CLAUDE.md` - This file - AI assistant instructions
- `.vscode/settings.json` - VS Code configuration for Shopify Liquid extension
- `.vscode/extensions.json` - Recommended VS Code extensions
- `.theme-check.yml` - Theme Check linting rules optimized for documentation
- `.mcp.json` - MCP server configuration for enhanced development

### 📚 Main Documentation (`shopify-liquid-guides/`)
- `README.md` - Entry point with navigation and philosophy
- `01-fundamentals.md` - Liquid syntax, objects, filters, control flow
- `02-quick-start.md` - Step-by-step implementation walkthrough
- `03-sections-and-schema.md` - Section development and schema configuration
- `04-blocks-and-css-scoping.md` - CSS methodology and block patterns
- `05-performance-and-accessibility.md` - Optimization and WCAG compliance
- `06-troubleshooting.md` - Common issues and debugging

### 🔧 Production Code Library (`code-library/`)
- `sections/` - Complete section templates with schema (5 production-ready sections)
- `blocks/` - Reusable block components with scoped CSS (2 essential blocks)
- `snippets/` - Utility functions and helpers (2 optimized snippets)
- `css-patterns/` - CSS methodologies and responsive patterns (3 pattern files)

### 📋 Complete Examples (`examples/`)
- `complete-homepage.json` - Full homepage with hero, products, testimonials, FAQ
- `product-page-sections.json` - Enhanced product page with reviews and features
- `collection-layout.json` - Collection page with filtering and features

### 📖 Tool Documentation (`docs/`)
- `shopify-extension/README.md` - VS Code extension features and setup
- `shopify-extension/configuration.md` - Detailed workspace configuration

### 🗂 Archive (`_archive/`)
- `shopify-liquid/` - Original comprehensive documentation (preserved)
- `shopify-liquid-gpt5/` - Original practical reference guide (preserved)

## Key Documentation Patterns

### Liquid Section Structure
All sections follow this pattern:
1. HTML/Liquid template code
2. Single `{% schema %}` JSON block defining:
   - Section name and settings
   - Block types (for repeatable content)
   - Presets for theme editor
   - Placement controls (`enabled_on`/`disabled_on`)

### Code Examples Philosophy
- **Copy-paste ready** - All examples are production-ready
- **Schema-driven** - Focus on section schema as the foundation
- **Performance-first** - Optimized images, minimal JS, SSR-first approach
- **Accessible** - WCAG 2.1 AA compliance patterns

## VS Code Development Environment

This repository is **pre-configured** for optimal Shopify Liquid development:

### ✅ Ready-to-Use Configuration
- **`.vscode/settings.json`** - Shopify Liquid extension with auto-formatting
- **`.vscode/extensions.json`** - Team recommendations for essential extensions
- **`.theme-check.yml`** - Linting rules optimized for documentation repository
- **File associations** - `.liquid` files recognized with proper syntax highlighting

### 🎯 Key Features Enabled
- **Intelligent Code Completion** - Liquid objects, filters, schema properties
- **Real-time Error Detection** - Red/yellow squiggles for Theme Check issues
- **Auto-formatting on Save** - Consistent code style with Shopify formatter
- **Hover Documentation** - Instant access to Liquid reference docs
- **File Navigation** - Click-to-jump to included snippets and sections

### 🚀 Immediate Benefits
Opening this project in VS Code provides:
- Syntax highlighting for all `.liquid` files in `code-library/`
- Schema completion for JSON configurations in examples
- Theme Check validation with documentation-friendly rules
- Emmet support for HTML within Liquid templates

## Working with This Repository

### 📁 Navigation Strategy
- **Complete Structure**: Reference [STRUCTURE.md](./STRUCTURE.md) for full file tree
- **Quick Navigation**: Use the navigation table in [README.md](./README.md)
- **Code Examples**: Browse `shopify-liquid-guides/code-library/` by category
- **Complete Templates**: Copy from `shopify-liquid-guides/examples/` for full pages

### 🔍 Finding Code Examples
- **Sections**: `shopify-liquid-guides/code-library/sections/` for complete templates
- **Blocks**: `shopify-liquid-guides/code-library/blocks/` for reusable components
- **Snippets**: `shopify-liquid-guides/code-library/snippets/` for utility functions
- **CSS Patterns**: `shopify-liquid-guides/code-library/css-patterns/` for styling methodologies
- **JSON Templates**: `shopify-liquid-guides/examples/` for complete page layouts

### 📚 Learning Path
1. **Start**: `shopify-liquid-guides/01-fundamentals.md` for Liquid syntax
2. **Build**: `shopify-liquid-guides/02-quick-start.md` for step-by-step implementation
3. **Advanced**: `shopify-liquid-guides/04-blocks-and-css-scoping.md` for CSS patterns
4. **Optimize**: `shopify-liquid-guides/05-performance-and-accessibility.md` for production readiness

### Common Tasks

#### Creating a New Section
1. Reference `shopify-liquid-guides/code-library/sections/hero-banner.liquid` as starting template
2. Study schema patterns in section examples
3. Follow accessibility guidelines in `shopify-liquid-guides/05-performance-and-accessibility.md`

#### Adding Blocks to Sections
1. Study `shopify-liquid-guides/code-library/blocks/` for reusable components
2. Follow CSS scoping methodology from `shopify-liquid-guides/04-blocks-and-css-scoping.md`
3. Reference complete examples in `shopify-liquid-guides/code-library/sections/`

#### CSS Development and Scoping
1. Study the scoping methodology in `shopify-liquid-guides/04-blocks-and-css-scoping.md`
2. Reference `shopify-liquid-guides/code-library/css-patterns/scoped-blocks.css` for implementation patterns
3. Use block-scoped CSS to prevent style collisions and enable true modularity

## MCP Server Configuration

This repository includes MCP server configuration in `.mcp.json`:
- **context7**: Documentation lookup and library research
- **exa**: Web search and content crawling
- **sequential-thinking**: Complex problem-solving workflows

MCP servers are enabled in `.claude/settings.local.json` for enhanced development capabilities.

## Key Principles for This Codebase

### Liquid Development Standards
- **Escape all user content**: Always use `| escape` filter for text/headings
- **Guard optional settings**: Check for nil values before accessing properties
- **SSR-first approach**: Render with Liquid, use JS sparingly
- **Responsive images**: Always provide `srcset`, `sizes`, and `loading="lazy"`

### Schema Best Practices
- **Valid JSON only**: Schema must be valid JSON (no Liquid inside)
- **Clear labels**: Use descriptive labels and helpful `info` text
- **Sensible limits**: Keep `max_blocks` reasonable (≤50)
- **Logical grouping**: Group related settings together

### Performance Requirements
- **Paginate large lists**: Use `{% paginate %}` for >50 items
- **Optimize images**: Request appropriate sizes with `image_url: width:`
- **Scoped CSS/JS**: Use section-scoped styles to avoid global conflicts
- **Minimal globals**: Avoid heavy loops on global objects like `all_products`

## Documentation Sources

The documentation is compiled from:
- Official Shopify Dev Documentation
- Shopify Liquid Code Examples
- Context7 Documentation
- GitHub Code Samples
- Performance Best Practices from Theme Store requirements

## Key Benefits of the Unified Structure

### Single Source of Truth
- No confusion about which documentation to follow
- Consistent terminology and patterns throughout
- Clear learning progression from basics to advanced

### CSS-First Development
- Comprehensive CSS scoping methodology prevents style collisions
- Production-ready examples with responsive patterns
- Block-scoped CSS enables true component modularity

### Developer Experience
- Copy-paste ready code examples
- Clear file organization by purpose
- Immediate access to both learning materials and implementation code

## File Navigation Quick Reference

### 🎯 By Task
| Need | Start Here |
|------|------------|
| **Repository Overview** | [README.md](./README.md) |
| **Complete File Structure** | [STRUCTURE.md](./STRUCTURE.md) |
| **Learn Shopify Liquid** | [01-fundamentals.md](./shopify-liquid-guides/01-fundamentals.md) |
| **Build First Section** | [02-quick-start.md](./shopify-liquid-guides/02-quick-start.md) |
| **Copy Production Code** | [code-library/](./shopify-liquid-guides/code-library/) |
| **Complete Page Templates** | [examples/](./shopify-liquid-guides/examples/) |
| **Set Up VS Code** | [docs/shopify-extension/](./shopify-liquid-guides/docs/shopify-extension/) |
| **CSS Methodology** | [04-blocks-and-css-scoping.md](./shopify-liquid-guides/04-blocks-and-css-scoping.md) |
| **Debug Issues** | [06-troubleshooting.md](./shopify-liquid-guides/06-troubleshooting.md) |

### 🔧 By File Type
- **`.liquid` templates** → `shopify-liquid-guides/code-library/sections/`, `blocks/`, `snippets/`
- **`.json` examples** → `shopify-liquid-guides/examples/`
- **`.css` patterns** → `shopify-liquid-guides/code-library/css-patterns/`
- **Configuration** → `.vscode/`, `.theme-check.yml`
- **Documentation** → `shopify-liquid-guides/*.md`, `docs/`

### 📚 Entry Points
- **New Developers**: Start with [shopify-liquid-guides/README.md](./shopify-liquid-guides/README.md)
- **Experienced Developers**: Jump to [code-library/](./shopify-liquid-guides/code-library/)
- **VS Code Users**: Configure with [docs/shopify-extension/](./shopify-liquid-guides/docs/shopify-extension/)
- **Project Understanding**: Review [STRUCTURE.md](./STRUCTURE.md)