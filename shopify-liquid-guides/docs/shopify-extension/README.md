# Shopify Liquid VS Code Extension

Complete guide to the official Shopify Liquid Visual Studio Code extension - the essential tool for professional Shopify theme development.

## Quick Start

### Installation
The Shopify Liquid extension is available on the [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=Shopify.theme-check-vscode).

**Install via VS Code:**
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search for "Shopify Liquid"
4. Click "Install" on the official Shopify extension

**Install via Command Line:**
```bash
code --install-extension Shopify.theme-check-vscode
```

## Core Features Overview

The extension is built on Shopify's [Liquid Language Server](https://shopify.dev/docs/storefronts/themes/tools/cli/language-server) and provides comprehensive development support:

### 🎨 **Syntax Highlighting**
- Official Shopify-maintained grammar
- Same highlighting used by GitHub
- Accurate Liquid, HTML, and CSS syntax support

### 📖 **Documentation on Hover**
- Instant access to Liquid object definitions
- Type information and documentation
- Clickable links to official reference docs
- Works for Liquid tags, filters, objects, and HTML elements

### ⚡ **Intelligent Code Completion**
**Liquid Elements:**
- Tags, filters, objects, and properties
- Theme, section, and block settings
- Translation keys and snippet names

**HTML Elements:**
- Tags, attributes, and attribute values
- Contextual suggestions based on element type

**Schema Support:**
- JSON schema tag completion
- `config/settings_schema.json` completion
- Contextual schema property suggestions

**Keyboard Shortcuts:**
- Mac: `Ctrl+Space`
- Windows: `Ctrl+Space`

### 🔧 **Code Navigation**
- **File References**: Cmd+click (Mac) / Ctrl+click (Windows) to navigate to included files
- **HTML Element Renaming**: F2 to rename opening and closing tags together
- **Auto-create Missing Files**: Automatically create referenced files that don't exist

### 🎯 **Code Formatting**
Powered by the [Liquid Prettier plugin](https://shopify.dev/docs/storefronts/themes/tools/liquid-prettier-plugin):

- **Format on Save**: Automatic formatting when saving files
- **Manual Formatting**: Right-click → "Format Document"
- **Command Palette**: "Format Document" command
- **Keyboard Shortcut**:
  - Mac: `Shift+Option+F`
  - Windows: `Shift+Alt+F`

### 🔄 **Auto-Closing Pairs**
Automatic closing of:
- Liquid tags: `{% if %}` → `{% endif %}`
- HTML elements: `<div>` → `</div>`
- Brackets and quotes

### 🔍 **Theme Check Integration**
Built-in linting powered by [Theme Check](https://shopify.dev/docs/storefronts/themes/tools/theme-check/configuration):

- **Real-time Error Detection**: Red wavy lines for errors
- **Warning Highlights**: Yellow wavy lines for warnings
- **Problems Panel**: View all issues in VS Code's Problems tab
- **Keyboard Shortcut**:
  - Mac: `Shift+Cmd+M`
  - Windows: `Ctrl+Shift+M`

### ⚡ **Auto-Fixes**
Automatic code corrections indicated by blue light bulbs:

- **Apply on Save**: Automatic fixes when saving
- **Manual Application**: Click light bulb or use keyboard shortcut
- **Keyboard Shortcut**:
  - Mac: `Option+Cmd+.`
  - Windows: `Ctrl+Alt+.`

### 💡 **Suggestions**
Smart suggestions indicated by yellow light bulbs:

- **Multiple Options**: Often provides several suggestion alternatives
- **Manual Review Required**: Suggestions require developer review
- **Keyboard Shortcut**:
  - Mac: `Cmd+.`
  - Windows: `Ctrl+.`

## Development Workflow Integration

### Recommended VS Code Settings

Create `.vscode/settings.json` in your theme root:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "Shopify.theme-check-vscode",
  "liquid.format.enable": true,
  "liquid.completion.enable": true,
  "liquid.hover.enable": true,
  "liquid.links.enable": true,
  "themeCheck.onlySingleFileChecks": false,
  "files.associations": {
    "*.liquid": "liquid"
  },
  "emmet.includeLanguages": {
    "liquid": "html"
  }
}
```

### Workspace Configuration

For team consistency, add `.vscode/extensions.json`:

```json
{
  "recommendations": [
    "Shopify.theme-check-vscode",
    "esbenp.prettier-vscode"
  ]
}
```

### File Structure Support

The extension recognizes standard Shopify theme structure:

```
theme/
├── assets/
├── config/
│   └── settings_schema.json    # Full schema completion
├── layout/
├── locales/
├── sections/                   # Section schema completion
├── snippets/                   # Snippet name completion
└── templates/
```

## Advanced Features

### Schema Tag Intelligence

When working in section files, the extension provides:

- **Schema Property Completion**: All valid schema properties
- **Setting Type Validation**: Ensures correct setting types
- **Block Configuration**: Proper block schema structure
- **Preset Templates**: Common preset patterns

Example schema completion:
```liquid
{% schema %}
{
  "name": "Custom Section",
  "settings": [
    {
      "type": "|"  // Auto-completes with valid types
    }
  ]
}
{% endschema %}
```

### Translation Key Support

Automatic completion for translation keys:
```liquid
{{ 'general.cart.add_to_cart' | t }}
     ↑ Auto-completes from locales files
```

### Object Property Intelligence

Smart completion for Shopify objects:
```liquid
{{ product.| }}
           ↑ Shows all available product properties
```

## Theme Check Configuration

### Custom Rules

Create `.theme-check.yml` in theme root:

```yaml
# Enable/disable specific checks
DeprecatedFilter:
  enabled: false

UnknownFilter:
  enabled: true

# Custom severity levels
MissingTemplate:
  severity: error

# Ignore specific files
ignore:
  - "snippets/third-party.liquid"
  - "sections/legacy-*.liquid"
```

### Performance Optimization

For large themes, optimize performance:

```yaml
# .theme-check.yml
exclude:
  - "node_modules/**"
  - "dist/**"
  - "build/**"

# Only check modified files in large projects
onlySingleFileChecks: true
```

## Best Practices

### 1. Extension Settings Optimization

**Enable all language features:**
```json
{
  "liquid.completion.enable": true,
  "liquid.hover.enable": true,
  "liquid.links.enable": true,
  "liquid.format.enable": true,
  "themeCheck.checkOnSave": true
}
```

### 2. Code Organization

**Use consistent file naming:**
- Sections: `section-name.liquid`
- Snippets: `snippet-name.liquid`
- Follow the naming patterns the extension expects

### 3. Documentation Integration

**Leverage hover documentation:**
- Hover over unfamiliar Liquid objects
- Use clickable links to reference docs
- Review suggested properties and methods

### 4. Error Prevention

**Address issues immediately:**
- Fix red wavy lines (errors) before committing
- Review yellow wavy lines (warnings) for best practices
- Use auto-fixes when available

### 5. Team Consistency

**Share workspace configuration:**
- Include `.vscode/` folder in version control
- Document extension requirements in README
- Use consistent formatting rules across team

## Troubleshooting

### Common Issues

**Extension not working:**
1. Verify you have the official Shopify extension installed
2. Check VS Code is recognizing `.liquid` files correctly
3. Restart VS Code language server: Cmd/Ctrl+Shift+P → "Restart Language Server"

**No code completion:**
1. Ensure file is recognized as Liquid (check status bar)
2. Verify theme structure follows Shopify conventions
3. Check if file associations are correct in settings

**Formatting not working:**
1. Verify Prettier is installed
2. Check default formatter is set to Shopify extension
3. Ensure format on save is enabled

**Theme Check errors:**
1. Review `.theme-check.yml` configuration
2. Check if files are in ignore list
3. Verify theme structure is valid

### Performance Issues

For large themes:
1. Enable `onlySingleFileChecks` in Theme Check config
2. Exclude build directories and node_modules
3. Use workspace-specific settings
4. Close unused files to reduce memory usage

## Integration with Shopify CLI

The extension works seamlessly with [Shopify CLI](https://shopify.dev/docs/themes/tools/cli):

```bash
# Initialize new theme with proper structure
shopify theme init my-theme

# Serve theme with hot reload
shopify theme serve

# Deploy theme
shopify theme deploy
```

The extension provides enhanced development experience when used alongside CLI tools.

## Updates and Contributing

### Staying Updated

The extension auto-updates through VS Code. To manually check:
1. Go to Extensions panel
2. Find Shopify Liquid extension
3. Click update if available

### Contributing

The extension is open source and part of Shopify's [theme-tools repository](https://github.com/Shopify/theme-tools).

**How to contribute:**
1. Visit [contributing guidelines](https://github.com/Shopify/theme-tools/blob/main/docs/contributing.md)
2. Report issues on GitHub
3. Submit feature requests
4. Contribute code improvements

## Next Steps

1. **Install the extension** if you haven't already
2. **Configure your workspace** with recommended settings
3. **Explore the features** by working with a Shopify theme
4. **Integrate with CLI tools** for complete development workflow

The Shopify Liquid VS Code extension is essential for professional theme development - it transforms VS Code into a powerful Shopify development environment with intelligent code assistance, error prevention, and seamless workflow integration.