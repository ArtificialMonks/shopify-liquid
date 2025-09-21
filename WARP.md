# WARP.md

## CRITICAL RULE: SUBSTANCE OVER PRAISE

**In all your responses, please focus on substance over praise. Skip unnecessary compliments, engage critically with my ideas, question my assumptions, identify my biases, and offer counterpoints when relevant. Don't shy away from disagreement, and ensure that any agreements you have are grounded in reason and evidence.**

**When writing your response, please ensure you include the following information:**
1. **A neutral, unbiased view of the request**, unfiltered by your desire to be a helpful and positive assistant
2. **A devil's advocate view**, pointing out any logical counterpoints or things that I have overlooked
3. **An encouraging, positive view of the request**

### Practical Application Guidelines

**Default Behavior**: Apply the full three-perspective format above.

**Exceptions** - Use streamlined responses for:
- Simple technical fixes with clear solutions ("How do I fix this TypeScript error?")
- Direct factual queries ("What's the syntax for X?")
- Routine implementation tasks with established patterns

**For exceptions**: Still maintain substance over praise and question assumptions, but focus on accuracy and directness rather than multiple perspectives.

**When in doubt**: Default to the full three-perspective format.

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is a **comprehensive Shopify theme development resource** with an advanced validation system containing documentation, production-ready code examples, and best practices for building modern Shopify themes. It covers all 7 Shopify file types with cutting-edge features and **enterprise-grade validation workflows**.

**Purpose**: Documentation and code library for professional Shopify theme development with **100% Theme Store compliance validation**.

## Follow-Up Request Protocol

**FOLLOW-UP REQUEST**:

Provide up to 4 additional high-value, necessary follow-up improvements for the Shopify Liquid documentation and code library repository. Apply strict criteria:

- **High-Value**: Must deliver measurable developer productivity improvements, theme performance gains, or merchant usability enhancements
- **Necessary**: Must address genuine gaps in Liquid implementation patterns, schema validation failures, or Theme Store compliance issues
- **Evidence-Based**: Must be justified by concrete issues in the current codebase, missing documentation patterns, or production deployment blockers
- **Scoped**: Must be implementable within the existing documentation structure and code library organization without requiring major architectural changes to the theme development workflow

Focus specifically on:
- Liquid template optimization and performance patterns
- Schema validation and Theme Store compliance gaps
- CSS scoping methodology improvements
- Production-ready section/block implementation missing pieces
- Developer experience enhancements for theme building
- Accessibility and responsive design pattern completeness

If fewer than the genuinely necessary improvements exist, provide fewer items rather than padding the list.

## Quick Start

### Prerequisites
- macOS with Homebrew at `/opt/homebrew/bin/brew`
- Node.js (for Shopify CLI)
- Shopify store access for testing

### Essential Setup
```bash
# Install core tools (Shopify CLI v3.84.2+ required)
npm install -g @shopify/cli

# Verify installation
shopify version

# Authenticate with Shopify
shopify login --store=your-store.myshopify.com
```

### First Commands - Enhanced Validation System + Shopify MCP
```bash
# 🚨 CRITICAL: Development validation with comprehensive checks (RECOMMENDED)
./scripts/validate-theme.sh development

# 🆕 Liquid syntax validation only (zero tolerance)
./scripts/validate-theme.sh syntax

# Complete validation suite with syntax validation
./scripts/validate-theme.sh all

# 🔍 Ultimate validation (comprehensive + liquid syntax)
./scripts/validate-theme.sh ultimate

# 🆕 Deep validation (ultimate + integrity + comprehensive)
./scripts/validate-theme.sh deep

# 🆕 Shopify MCP Server integration (when working with AI assistants)
# Note: These are used within Claude Code, not direct command line tools
# See shopify-liquid-guides/docs/development/SHOPIFY-MCP-SETUP.md for complete integration guide

# Browse code library structure (including custom directories)
ls -la shopify-liquid-guides/code-library/
ls -la shopify-liquid-guides/code-library/blocks/custom/
ls -la shopify-liquid-guides/code-library/sections/custom/
ls -la shopify-liquid-guides/code-library/css-patterns/custom/
```

## 🚀 Enhanced Validation System

### Ultimate Theme Validation Script + Liquid Syntax Validation
The repository now includes a comprehensive validation system with multi-language validation (Shell + Python) and advanced Liquid syntax checking:

```bash
# 🆕 Liquid syntax validation only (zero tolerance)
./scripts/validate-theme.sh syntax

# Development validation (fast, essential checks + liquid syntax)
./scripts/validate-theme.sh development

# 🆕 Ultimate validation (comprehensive liquid syntax + theme validation)
./scripts/validate-theme.sh ultimate

# 🆕 Deep validation (ultimate + integrity + comprehensive)
./scripts/validate-theme.sh deep

# Comprehensive validation (all available checks)
./scripts/validate-theme.sh comprehensive

# Production validation (Theme Store submission ready)
./scripts/validate-theme.sh production

# Auto-fix correctable issues
./scripts/validate-theme.sh auto-fix

# Generate detailed JSON report
./scripts/validate-theme.sh report

# Test Shopify validation presets
./scripts/validate-theme.sh presets

# Complete validation workflow (recommended)
./scripts/validate-theme.sh all

# Show help and usage
./scripts/validate-theme.sh help
```

### 🆕 Advanced Liquid Syntax Validation
```bash
# Python-based comprehensive Liquid syntax validation
python scripts/liquid-syntax-validator.py shopify-liquid-guides/code-library/

# Multi-level validation options:
# --validation-level fast      # Quick syntax checks
# --validation-level standard  # Standard validation (default)
# --validation-level comprehensive # Deep validation with all checks

# Integration with ultimate validator
python scripts/ultimate-validator.py --liquid-syntax
```

### Multi-Level Theme Check Configurations

#### Development Configuration (`.theme-check-development.yml`)
```bash
# Fast validation for development
shopify theme check --config .theme-check-development.yml

# Features:
# - Translation checks disabled for speed
# - Undefined objects allowed for documentation
# - Focus on critical syntax errors only
```

#### Comprehensive Configuration (`.theme-check.yml`)
```bash
# Complete validation with all checks (default)
shopify theme check

# Features:
# - All 50+ validation rules enabled
# - Schema validation (ValidSettingsKey, ValidSchemaName, etc.)
# - Content validation (ValidContentForArguments, etc.)
# - Security checks (ContentForHeaderModification, etc.)
```

#### Production Configuration (`.theme-check-production.yml`)
```bash
# Theme Store submission readiness
shopify theme check --config .theme-check-production.yml

# Features:
# - Maximum validation for Theme Store compliance
# - Translation requirements enforced
# - Required theme structure validation
# - Zero tolerance for critical errors
```

### Shopify CLI Advanced Features
```bash
# Auto-correct fixable issues
shopify theme check --auto-correct

# JSON output for CI/CD integration
shopify theme check --output json > validation-report.json

# Fail level configuration
shopify theme check --fail-level warning  # Fail on warnings and errors
shopify theme check --fail-level error    # Fail only on errors (default)

# Shopify validation presets
shopify theme check --config theme-check:recommended    # Shopify recommended
shopify theme check --config theme-check:all           # All available checks
shopify theme check --config theme-check:theme-app-extension  # App extension validation

# Serve theme locally (requires complete theme structure)
cd path/to/complete/theme
shopify theme serve

# Push/pull themes
shopify theme push --development
shopify theme pull --development
```

**⚠️ Important**: The validation system targets `shopify-liquid-guides/code-library/` which contains the production-ready theme files organized in standard Shopify directory structure (sections/, snippets/, blocks/, locales/). This ensures accurate validation against real theme file relationships.

**⚠️ Note**: `shopify theme serve` requires a complete theme with all 7 file types. The code library contains individual components for validation and reference - use complete themes from `shopify-liquid-guides/examples/` for serving.

## 🚀 Shopify MCP Server Integration

### Overview
The repository includes Shopify MCP server integration for enhanced AI-assisted development. The MCP (Model Context Protocol) server provides direct access to Shopify APIs and documentation when working with AI assistants like Claude Code.

### MCP Configuration
```bash
# View MCP configuration
cat .mcp.json

# Shopify MCP server is configured with optimal settings:
# - LIQUID: "true" (Liquid template support)
# - POLARIS_UNIFIED: "true" (Unified design system)
# - OPT_OUT_INSTRUMENTATION: "true" (Performance optimization)
```

### When to Use Shopify MCP (AI Assistant Context)
The Shopify MCP server is automatically available when working with Claude Code and provides these capabilities:

**Core MCP Tools:**
- `learn_shopify_api` - Initialize Shopify API context (required first step)
- `validate_theme` - Real-time theme validation against live Shopify standards
- `validate_graphql_codeblocks` - Live GraphQL query validation
- `introspect_graphql_schema` - Live schema exploration for API development
- `search_docs_chunks` - Direct access to official Shopify documentation
- `fetch_full_docs` - Retrieve complete documentation pages

**Typical MCP Workflow (AI Assistant Usage):**
1. AI assistant initializes with `learn_shopify_api`
2. Real-time validation using `validate_theme` during development
3. GraphQL development using `introspect_graphql_schema` and `validate_graphql_codeblocks`
4. Documentation lookup using `search_docs_chunks` and `fetch_full_docs`
5. Continuous validation throughout development process

### MCP vs. Traditional Validation
**Traditional Development Workflow:**
```bash
# Local validation (always available)
./scripts/validate-theme.sh development
./scripts/validate-theme.sh production
shopify theme check
```

**Enhanced AI-Assisted Workflow:**
- **Traditional validation** + **MCP integration** for live Shopify API access
- Real-time documentation lookup during development
- Live GraphQL schema introspection for accurate API development
- Theme Store compliance validation against current Shopify standards

### Documentation and Setup
```bash
# Complete MCP setup guide
cat shopify-liquid-guides/docs/development/SHOPIFY-MCP-SETUP.md

# MCP integration examples and usage patterns
# (Documentation created during MCP server setup)
```

**Key Benefits:**
- **Live Shopify Documentation**: Direct access to current Shopify documentation
- **Real-time Validation**: Theme validation against live Shopify standards
- **GraphQL Development**: Live schema introspection and query validation
- **Enhanced Accuracy**: Prevents Liquid hallucinations with live API access
- **Theme Store Compliance**: Validation against current Theme Store requirements

### Documentation Navigation
```bash
# Explore comprehensive documentation
ls -la shopify-liquid-guides/docs/
ls -la shopify-liquid-guides/docs/architecture/
ls -la shopify-liquid-guides/docs/templates/

# Browse production-ready code
ls -la shopify-liquid-guides/code-library/sections/
ls -la shopify-liquid-guides/code-library/blocks/
ls -la shopify-liquid-guides/code-library/snippets/

# View complete examples
ls -la shopify-liquid-guides/examples/
```

### Optional Linting & Formatting
```bash
# Format with Prettier (if project uses it)
npx prettier --check "**/*.{liquid,json,md,css,js}"
npx prettier --write "**/*.{liquid,json,md,css,js}"

# Check Markdown (if project uses it)
npx markdownlint "**/*.md"
```

## Repository Architecture & Structure

### Top-Level Organization
```
shopify-liquid/
├── README.md                          # Repository overview
├── STRUCTURE.md                       # Complete file tree reference
├── INSTRUCTIONS.md                    # Task-specific development guidance
├── CLAUDE.md                          # AI assistant instructions
├── WARP.md                           # This file - Warp guidance
├── THEME-CHECK-SETUP.md              # Complete validation setup guide
├── .theme-check.yml                  # Comprehensive validation rules
├── .theme-check-development.yml      # Development validation config
├── .theme-check-production.yml       # Production/Theme Store validation
├── .vscode/                          # VS Code workspace configuration
├── .warp/                           # Warp workflows and configuration
├── scripts/                         # Advanced validation scripts
├── locales/                         # Translation files for validation
└── shopify-liquid-guides/            # Main documentation and code
```

### Core Documentation Structure (`shopify-liquid-guides/`)
```
shopify-liquid-guides/
├── 01-fundamentals.md                # Liquid syntax and basics
├── 02-quick-start.md                 # Step-by-step implementation
├── 03-sections-and-schema.md         # Section development patterns
├── 04-blocks-and-css-scoping.md      # CSS methodology (critical)
├── 05-performance-and-accessibility.md # Optimization best practices
├── 06-troubleshooting.md             # Common issues and solutions
├── schema-validation/                # Schema validation rules (critical)
├── docs/                            # Comprehensive documentation
├── code-library/                    # Production-ready code examples
│   ├── blocks/
│   │   ├── essential/               # Core blocks every theme needs
│   │   ├── advanced/                # Complex functionality blocks
│   │   ├── legacy/                  # Backward compatibility blocks
│   │   └── custom/                  # 🆕 Repository-specific custom blocks
│   ├── sections/
│   │   ├── essential/               # Core section templates
│   │   ├── enhanced/                # Advanced section functionality
│   │   ├── templates/               # Customer/gift card templates
│   │   └── custom/                  # 🆕 Repository-specific custom sections
│   ├── css-patterns/
│   │   ├── bem-scoping/            # BEM methodology with scoping
│   │   ├── responsive/              # Mobile-first patterns
│   │   └── custom/                  # 🆕 Repository-specific CSS patterns
│   └── snippets/                   # Reusable Liquid functionality
└── examples/                        # Complete templates and samples
```

### Documentation (`docs/`) - All 7 Shopify File Types
- `architecture/` - Complete theme structure and patterns
- `layouts/` - Theme foundation files (theme.liquid, checkout.liquid)
- `templates/` - Page-specific content (JSON vs Liquid templates)
- `assets/` - Resources (CSS, JS, images, fonts)
- `config/` - Settings and merchant customization
- `locales/` - Internationalization and translation
- `section-groups/` - Dynamic layout areas (Online Store 2.0)
- `advanced-features/` - Modern patterns (AI, PWA, metaobjects)

### 🆕 Custom Directories (`code-library/*/custom/`) - Repository-Specific Components
- `blocks/custom/` - Custom block components built for this repository
  - **advanced_video_text.liquid** - Advanced video + text positioning block
  - **Future custom blocks** - Additional repository-specific components
- `sections/custom/` - Custom section templates for specialized use cases
- `css-patterns/custom/` - Repository-specific CSS methodologies and scoping patterns
- **Validation**: All custom components MUST pass `./scripts/validate-theme.sh integrity`
- **Standards**: Follow same patterns as essential/advanced directories
- **Documentation**: Each custom directory includes comprehensive README.md

### Production Code Library (`code-library/`)
- `sections/` - Complete section templates with schema
- `blocks/` - Reusable block components
- `snippets/` - Utility functions and helpers
- `css-patterns/` - CSS methodologies and scoping patterns

### Examples (`examples/`)
- `complete-homepage.json` - Full homepage implementation
- `product-page-sections.json` - Enhanced product page
- `collection-layout.json` - Collection page with filtering

## Development Patterns & Conventions

### CSS Scoping Methodology (Critical)
**Every section/block MUST use unique ID scoping to prevent style conflicts:**

```liquid
{%- assign unique = section.id | replace: '_', '' | downcase -%}

{% style %}
  .component-{{ unique }} {
    /* Base styles with CSS custom properties */
    background: {{ section.settings.background_color | default: '#ffffff' }};
  }
  
  .component__element-{{ unique }} {
    /* Element styles */
  }
  
  @media (max-width: 749px) {
    .component-{{ unique }} {
      /* Mobile-first responsive styles */
    }
  }
{% endstyle %}

<div class="component-{{ unique }}" {{ section.shopify_attributes }}>
  <!-- Content with scoped classes -->
</div>
```

### Schema Validation Requirements
**Before creating ANY schema, reference**: `shopify-liquid-guides/schema-validation/schema-guidelines.md`

Critical validation rules:
- Range step calculation: `(max - min) / step ≤ 101`
- Use correct setting types (`video` not `file` for video uploads)
- No `enabled_on` in section schemas (app blocks only)
- Step values ≥ 0.1 for all ranges
- Valid JSON syntax (no trailing commas)
- Unique setting IDs within each section

### File Organization Standards
- **Naming**: Use kebab-case filenames (`section-name.liquid`)
- **Sections**: Self-contained with minimal external dependencies
- **Snippets**: Reusable fragments with parameter validation
- **Documentation**: Follow established structure in `docs/`
- **Code Library**: Production-ready, copy-paste examples only

### Performance & Accessibility Standards
- Always escape user input: `{{ text | escape }}`
- Guard optional settings: `{% if setting != blank %}`
- Use semantic HTML and ARIA labels
- Implement responsive images with `srcset` and `sizes`
- Follow WCAG 2.1 AA compliance patterns

## Key Reference Files

### Essential Development Files
- **`THEME-CHECK-SETUP.md`** - Complete validation system setup guide (START HERE)
- **`shopify-liquid-guides/docs/development/SHOPIFY-MCP-SETUP.md`** - 🆕 Shopify MCP server integration and usage guide
- **`.theme-check.yml`** - Comprehensive theme validation configuration
- **`.theme-check-development.yml`** - Fast development validation config
- **`.theme-check-production.yml`** - Theme Store submission validation
- **`scripts/validate-theme.sh`** - Advanced validation script with multiple levels
- **`.mcp.json`** - 🆕 MCP server configuration for enhanced AI-assisted development
- **`.vscode/settings.json`** - VS Code Shopify Liquid extension config
- **`.vscode/sessions.json`** - Terminal Keeper sessions (workflow reference)
- **`.warp/workflows.yaml`** - Warp terminal workflows for validation + MCP integration
- **`locales/en.default.json`** - Default translation file for validation
- **`INSTRUCTIONS.md`** - Comprehensive task-specific guidance

### Critical Documentation References
- **`shopify-liquid-guides/schema-validation/schema-guidelines.md`** - Schema validation rules (MUST READ)
- **`shopify-liquid-guides/04-blocks-and-css-scoping.md`** - CSS scoping methodology
- **`shopify-liquid-guides/docs/architecture/theme-overview.md`** - Complete theme architecture
- **`shopify-liquid-guides/docs/validation/VALIDATOR_ARCHITECTURE_IMPROVEMENTS.md`** - 🆕 Comprehensive validator implementation
- **`shopify-liquid-guides/docs/validation/SHOPIFY_FILE_TYPE_VALIDATION_MATRIX.md`** - 🆕 Official validation reference
- **`STRUCTURE.md`** - Complete file tree and navigation guide

### Production Code References
- **`shopify-liquid-guides/code-library/sections/`** - Copy-paste ready sections
- **`shopify-liquid-guides/code-library/css-patterns/`** - CSS scoping examples
- **`shopify-liquid-guides/examples/`** - Complete template implementations

## Environment Setup & Tooling

### macOS Setup (Homebrew at `/opt/homebrew/bin/brew`)
```bash
# Update Homebrew
/opt/homebrew/bin/brew update

# Install Node.js for Shopify CLI
/opt/homebrew/bin/brew install node

# Install Shopify CLI (v3.84.2+ required)
npm install -g @shopify/cli

# Verify installation
node -v
npm -v
shopify version
```

### Ruby & Theme Check Setup (Optional - for legacy gem usage)
```bash
# Install Ruby (if needed for gem version)
/opt/homebrew/bin/brew install ruby

# Install Theme Check gem (legacy)
gem install theme-check

# Verify installation
ruby -v
theme-check -v

# Note: Shopify CLI includes theme-check functionality
```

### Shopify Authentication
```bash
# Login to your development store
shopify login --store=your-development-store.myshopify.com

# Verify authentication
shopify whoami
```

### Optional Node.js Tooling
```bash
# Install Node.js (via nvm recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
nvm use node

# Verify installation
node -v
npm -v

# Test Prettier (on-demand usage)
npx prettier --version
```

### VS Code Integration (Optional)
1. Install "Shopify Liquid" extension from marketplace
2. The repository includes pre-configured settings in `.vscode/settings.json`
3. Terminal sessions are pre-configured in `.vscode/sessions.json`

## Warp Workflows (Optional)

The repository includes VS Code Terminal Keeper sessions in `.vscode/sessions.json`. You can mirror these as Warp Workflows by creating `.warp/workflows.yaml`:

```yaml
# Advanced Warp Workflows (already created at .warp/workflows.yaml)
workflows:
  # Validation workflows
  validation-dev:
    name: "Development Validation"
    command: ./scripts/validate-theme.sh development

  validation-full:
    name: "Complete Validation Suite"
    command: ./scripts/validate-theme.sh all

  validation-prod:
    name: "Production Validation"
    command: ./scripts/validate-theme.sh production

  auto-fix:
    name: "Auto-Fix Issues"
    command: ./scripts/validate-theme.sh auto-fix

  # Legacy theme-check
  theme-check:
    name: "Legacy Theme Check"
    command: |
      cd shopify-liquid-guides/code-library
      theme-check .

  # 🚀 MCP Integration workflows
  mcp-setup-check:
    name: "Check MCP Configuration"
    command: |
      echo "🔧 MCP Configuration:"
      cat .mcp.json | jq '."shopify-dev-mcp"'
      echo ""
      echo "📖 MCP Setup Guide:"
      ls -la shopify-liquid-guides/docs/development/SHOPIFY-MCP-SETUP.md

  mcp-documentation:
    name: "MCP Documentation and Guide"
    command: |
      echo "📚 Shopify MCP Integration Guide:"
      echo "- shopify-liquid-guides/docs/development/SHOPIFY-MCP-SETUP.md - Complete setup and usage guide"
      echo "- .mcp.json - MCP server configuration"
      echo ""
      echo "🔧 MCP Tools Available (when using AI assistants):"
      echo "- learn_shopify_api - Initialize Shopify API context"
      echo "- validate_theme - Real-time theme validation"
      echo "- validate_graphql_codeblocks - GraphQL query validation"
      echo "- introspect_graphql_schema - Live schema exploration"
      echo "- search_docs_chunks - Official Shopify documentation search"
      echo "- fetch_full_docs - Complete documentation pages"
      echo ""
      echo "💡 Note: MCP tools are used within AI assistants like Claude Code"
      echo "💡 See shopify-liquid-guides/docs/development/SHOPIFY-MCP-SETUP.md for complete usage examples"

  # Documentation and navigation
  docs-browse:
    name: "Browse Documentation"
    command: |
      echo "📚 Documentation structure:"
      ls -la shopify-liquid-guides/docs/
      echo ""
      echo "🔧 Code library:"
      ls -la shopify-liquid-guides/code-library/
      echo ""
      echo "🚀 MCP Integration:"
      ls -la shopify-liquid-guides/docs/development/SHOPIFY-MCP-SETUP.md

  # Shopify CLI workflows
  serve-theme:
    name: "Serve Shopify Theme"
    parameters:
      - name: theme_path
        description: "Path to complete theme directory"
        required: true
    command: |
      cd {{theme_path}}
      shopify theme serve
```

## Troubleshooting & Fix-First Policy

### Fix-First Protocol
**When ANY issue, bug, or validation error is detected:**
1. **STOP** all other work immediately
2. **FIX** the issue completely before proceeding
3. **VERIFY** the fix by re-running the failing command
4. **DOCUMENT** any caveats or learnings

### Common Issues & Solutions

#### Theme Check Errors
```bash
# Re-run theme check to verify fixes
cd shopify-liquid-guides/code-library
theme-check .

# Check specific file
theme-check path/to/specific/file.liquid

# Generate fresh config if needed
theme-check --init
```

#### Schema Validation Errors
**Always reference**: `shopify-liquid-guides/schema-validation/schema-guidelines.md`

Common fixes:
- Range step too small: Ensure `(max - min) / step ≤ 101`
- Invalid setting type: Use `video` not `file` for video uploads
- Trailing commas: Remove from JSON schema
- Missing required properties: Add `id`, `type`, `label` to all settings

#### Shopify CLI Issues
```bash
# Verify authentication
shopify whoami

# Re-authenticate if needed
shopify login --store=your-store.myshopify.com

# Ensure you're in a complete theme directory for serve/push commands
# Check for: config/, layout/, sections/, snippets/, templates/, assets/, locales/
```

#### Path and Directory Issues
```bash
# Verify current directory
pwd

# Navigate to correct location
cd shopify-liquid-guides/code-library  # for Theme Check
cd path/to/complete/theme              # for Shopify CLI commands
```

### Getting Help
- **Validation System Setup**: `THEME-CHECK-SETUP.md` - Complete validation system guide
- **Schema Issues**: `shopify-liquid-guides/schema-validation/schema-guidelines.md`
- **CSS Issues**: `shopify-liquid-guides/04-blocks-and-css-scoping.md`
- **Architecture Questions**: `shopify-liquid-guides/docs/architecture/`
- **Task-Specific Guidance**: `INSTRUCTIONS.md`
- **Complete Structure**: `STRUCTURE.md`

## Maintenance Guidelines

### Keep WARP.md Updated
Contributors should update this file when:
- New commands or workflows are added
- Repository structure changes (directories, reorganization)
- Development patterns evolve (CSS scoping, schema rules)
- Tooling versions update (Shopify CLI, Theme Check)
- New troubleshooting scenarios are discovered

### Sync with Other Config Files
Maintain alignment between:
- `WARP.md` ↔ `.vscode/sessions.json` (mirror workflows)
- `WARP.md` ↔ `.warp/workflows.yaml` (if created)
- `WARP.md` ↔ `INSTRUCTIONS.md` (cross-reference task guidance)

---

**Ready to develop with Shopify Liquid?** Start with the Quick Start section above, then reference the comprehensive documentation in `shopify-liquid-guides/docs/` and production code in `shopify-liquid-guides/code-library/`.

**For complete validation system details**, see `THEME-CHECK-SETUP.md` - your ultimate guide to the enterprise-grade validation system with 100% Theme Store compliance.
