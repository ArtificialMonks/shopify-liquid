# Extension Configuration

Detailed configuration guide for optimizing the Shopify Liquid VS Code extension for your development workflow.

## VS Code Settings Configuration

### Essential Settings

Create or update `.vscode/settings.json` in your theme root:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "Shopify.theme-check-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  },
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.detectIndentation": false,

  "liquid.format.enable": true,
  "liquid.completion.enable": true,
  "liquid.hover.enable": true,
  "liquid.links.enable": true,
  "liquid.validation.enable": true,

  "themeCheck.checkOnSave": true,
  "themeCheck.checkOnOpen": true,
  "themeCheck.onlySingleFileChecks": false,

  "files.associations": {
    "*.liquid": "liquid"
  },

  "emmet.includeLanguages": {
    "liquid": "html"
  },

  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/build": true,
    "**/.git": true
  }
}
```

### Performance Optimization Settings

For larger themes or slower machines:

```json
{
  "themeCheck.onlySingleFileChecks": true,
  "liquid.completion.maxItems": 50,
  "editor.suggest.maxVisibleSuggestions": 10,
  "editor.hover.delay": 300,
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/dist/**": true,
    "**/build/**": true
  }
}
```

## Theme Check Configuration

### Basic Configuration

Create `.theme-check.yml` in your theme root:

```yaml
# Basic Theme Check configuration

# Enable/disable checks globally
enabled: true

# Root directory for theme files
root: "."

# Exclude directories from checking
exclude:
  - "node_modules/**"
  - "dist/**"
  - "build/**"
  - "assets/vendor/**"

# Ignore specific files
ignore:
  - "snippets/third-party-*.liquid"
  - "sections/legacy-*.liquid"

# Check configuration
checks:
  # Liquid syntax and best practices
  LiquidTag:
    enabled: true
    severity: error

  UnknownFilter:
    enabled: true
    severity: warning

  DeprecatedFilter:
    enabled: true
    severity: warning

  # HTML validation
  ValidHTMLTranslation:
    enabled: true
    severity: error

  # Performance checks
  AssetSizeAppJSCSS:
    enabled: true
    threshold_in_bytes: 100000
    severity: warning

  # Security checks
  ContentForHeaderModification:
    enabled: true
    severity: error

  # Best practices
  UnusedAssign:
    enabled: true
    severity: info

  MissingRequiredTemplateFiles:
    enabled: true
    severity: error
```

### Advanced Theme Check Rules

```yaml
# Advanced configuration for production themes

# Custom severity levels
checks:
  # Performance rules
  AssetSizeAppJSCSS:
    enabled: true
    threshold_in_bytes: 50000  # Stricter limit
    severity: error

  AssetSizeCSS:
    enabled: true
    threshold_in_bytes: 25000
    severity: warning

  # Accessibility rules
  ImgLazyLoading:
    enabled: true
    severity: warning

  MissingRequiredTemplateFiles:
    enabled: true
    severity: error

  # Security rules
  ContentForHeaderModification:
    enabled: true
    severity: error

  # Code quality
  UnusedAssign:
    enabled: true
    severity: info

  UnusedSnippet:
    enabled: true
    severity: info

  # Translation rules
  TranslationKeyExists:
    enabled: true
    severity: warning

  ValidHTMLTranslation:
    enabled: true
    severity: error

# File-specific configurations
file_patterns:
  "sections/*.liquid":
    checks:
      MissingTemplate:
        enabled: false

  "snippets/*.liquid":
    checks:
      UnusedSnippet:
        enabled: false
```

## Workspace Configuration

### Team Settings

Create `.vscode/extensions.json` for team consistency:

```json
{
  "recommendations": [
    "Shopify.theme-check-vscode",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-json"
  ],
  "unwantedRecommendations": [
    "ms-vscode.vscode-typescript-next"
  ]
}
```

### Multi-root Workspace

For projects with multiple themes:

```json
{
  "folders": [
    {
      "name": "Main Theme",
      "path": "./themes/main"
    },
    {
      "name": "Mobile Theme",
      "path": "./themes/mobile"
    }
  ],
  "settings": {
    "liquid.format.enable": true,
    "themeCheck.checkOnSave": true
  }
}
```

## Language Server Configuration

### Custom Language Server Settings

For advanced users, configure the Liquid Language Server directly:

```json
{
  "liquid.languageServer.enabled": true,
  "liquid.languageServer.path": "/custom/path/to/server",
  "liquid.languageServer.flags": [
    "--experimental-features"
  ],
  "liquid.trace.server": "verbose"
}
```

### Debug Configuration

Enable detailed logging for troubleshooting:

```json
{
  "liquid.trace.server": "verbose",
  "liquid.debug": true,
  "themeCheck.debug": true,
  "developer.reload": true
}
```

## File Association Configuration

### Custom File Types

Associate additional file types with Liquid:

```json
{
  "files.associations": {
    "*.liquid": "liquid",
    "*.theme": "liquid",
    "*.shopify": "liquid",
    "*.liquid.html": "liquid",
    "*.liquid.css": "liquid"
  }
}
```

### Template-Specific Associations

```json
{
  "files.associations": {
    "*.product.liquid": "liquid",
    "*.collection.liquid": "liquid",
    "*.cart.liquid": "liquid",
    "*.blog.liquid": "liquid",
    "*.article.liquid": "liquid"
  }
}
```

## Formatting Configuration

### Prettier Integration

Create `.prettierrc` for consistent formatting:

```json
{
  "plugins": ["@shopify/prettier-plugin-liquid"],
  "overrides": [
    {
      "files": "*.liquid",
      "options": {
        "parser": "liquid-html",
        "printWidth": 120,
        "tabWidth": 2,
        "useTabs": false,
        "singleQuote": true,
        "liquidSingleQuote": false,
        "embeddedSingleQuote": true,
        "htmlWhitespaceSensitivity": "ignore"
      }
    }
  ]
}
```

### Editor-Specific Formatting

```json
{
  "[liquid]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "Shopify.theme-check-vscode",
    "editor.tabSize": 2,
    "editor.insertSpaces": true,
    "editor.wordWrap": "bounded",
    "editor.wordWrapColumn": 120
  }
}
```

## Snippet Configuration

### Custom Liquid Snippets

Create `.vscode/liquid.code-snippets`:

```json
{
  "Section Template": {
    "prefix": "section",
    "body": [
      "{% comment %} sections/${1:section-name}.liquid {% endcomment %}",
      "<section class=\"${1:section-name}\">",
      "  {% if section.settings.${2:title} != blank %}",
      "    <h2>{{ section.settings.${2:title} | escape }}</h2>",
      "  {% endif %}",
      "</section>",
      "",
      "<style>",
      "  .${1:section-name} {",
      "    $3",
      "  }",
      "</style>",
      "",
      "{% schema %}",
      "{",
      "  \"name\": \"${4:Section Name}\",",
      "  \"settings\": [",
      "    {\"type\": \"text\", \"id\": \"${2:title}\", \"label\": \"${5:Title}\"}",
      "  ]",
      "}",
      "{% endschema %}"
    ],
    "description": "Create a basic Shopify section template"
  },

  "Block Template": {
    "prefix": "block",
    "body": [
      "{% assign unique = block.id | replace: '_', '' | downcase %}",
      "",
      "{% style %}",
      "  .${1:block-name}-{{ unique }} {",
      "    $2",
      "  }",
      "{% endstyle %}",
      "",
      "<div class=\"${1:block-name}-{{ unique }}\" {{ block.shopify_attributes }}>",
      "  $0",
      "</div>"
    ],
    "description": "Create a scoped block template"
  }
}
```

## Git Integration

### Recommended .gitignore

```gitignore
# VS Code
.vscode/settings.json
.vscode/launch.json
.vscode/tasks.json

# Theme Check
.theme-check-cache/

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*

# Dependencies
node_modules/
```

### Pre-commit Hooks

Set up Theme Check as a pre-commit hook:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Shopify/theme-check
    rev: v1.14.0
    hooks:
      - id: theme-check
```

## Environment-Specific Configuration

### Development Environment

```json
{
  "liquid.completion.enable": true,
  "liquid.hover.enable": true,
  "themeCheck.checkOnSave": true,
  "themeCheck.severity": "warning"
}
```

### Production Environment

```json
{
  "themeCheck.severity": "error",
  "themeCheck.checkOnSave": true,
  "themeCheck.checkOnOpen": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  }
}
```

## Troubleshooting Configuration

### Reset Extension Settings

If experiencing issues, reset to defaults:

```bash
# Command Palette
# > Preferences: Open Settings (JSON)
# Remove all Shopify/Liquid related settings
```

### Language Server Restart

```bash
# Command Palette
# > Shopify Liquid: Restart Language Server
```

### Clear Cache

```bash
# Remove theme check cache
rm -rf .theme-check-cache/

# Restart VS Code
```

This configuration guide ensures optimal performance and functionality of the Shopify Liquid VS Code extension for professional theme development.