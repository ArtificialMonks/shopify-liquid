# Shopify Theme Development Workflow

**Optimized development process with automated validation for Theme Store compliance**

## Quick Start

```bash
# 1. Setup validation hooks
git config core.hooksPath scripts/git-hooks

# 2. Validate before coding
./scripts/validate-theme.sh development

# 3. Develop with confidence
# Your changes are automatically validated on commit
```

## Complete Development Workflow

### Phase 1: Project Setup

1. **Clone and Setup**
   ```bash
   git clone <repository>
   cd <theme-directory>
   npm install  # if using build tools
   ```

2. **Install Git Hooks**
   ```bash
   # Option A: Repository-specific hooks
   git config core.hooksPath scripts/git-hooks

   # Option B: Global pre-commit framework
   pip install pre-commit
   pre-commit install
   ```

3. **Validate Environment**
   ```bash
   ./scripts/validate-theme.sh development
   shopify theme check
   ```

### Phase 2: Development Process

#### Before Starting Work

1. **Check Dependencies**
   ```bash
   # Verify all required assets exist
   python3 scripts/scan-schema-integrity.py .
   ```

2. **Branch from Main**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

#### During Development

1. **Code with Validation**
   - Make your changes
   - Validation runs automatically on file save (VS Code)
   - Pre-commit hooks validate before each commit

2. **Test Thoroughly**
   ```bash
   # Quick validation
   ./scripts/validate-theme.sh development

   # Deep validation before PR
   ./scripts/validate-theme.sh deep
   ```

3. **Fix Issues Immediately**
   ```bash
   # If validation fails
   python3 scripts/ultimate-validator.py .
   python3 scripts/scan-schema-integrity.py .
   ```

#### Commit Process

1. **Stage Changes**
   ```bash
   git add <files>
   ```

2. **Automatic Validation** (via pre-commit hook)
   - Schema integrity check
   - Liquid syntax validation
   - Asset dependency verification
   - Settings usage validation

3. **Commit with Confidence**
   ```bash
   git commit -m "feat: add enhanced video block with positioning controls"
   ```

### Phase 3: Pre-Deployment

#### Comprehensive Validation

```bash
# Ultimate validation suite
./scripts/validate-theme.sh all

# Manual verification
shopify theme dev
# Test in theme editor + preview mode
```

#### Performance Testing

```bash
# Run Lighthouse CI (if configured)
npm run lighthouse

# Manual performance check
# Open dev tools, test Core Web Vitals
```

### Phase 4: Deployment

#### Theme Store Submission

```bash
# Final validation
./scripts/validate-theme.sh production

# Package for submission
zip -r theme-v1.0.0.zip . -x "*.git*" "node_modules/*" "scripts/*"
```

#### Live Store Deployment

```bash
# Deploy to development store first
shopify theme push --development

# Test thoroughly, then deploy to live
shopify theme push --live
```

## Validation Standards

### Automatic Checks (Pre-Commit)

✅ **Schema Integrity**
- All settings defined are used in Liquid
- No unused schema definitions
- Valid setting types and ranges

✅ **Liquid Syntax**
- No hallucinated filters or objects
- Proper escaping and error handling
- Performance optimizations

✅ **Asset Dependencies**
- All referenced assets exist
- No broken snippet/section references
- Proper asset_url usage

### Manual Verification Points

🔍 **Theme Editor Testing**
- All settings work as expected
- No JavaScript errors in console
- Proper responsive behavior

🔍 **Preview Mode Testing**
- Scroll animations function
- Hover effects work correctly
- Performance meets standards

🔍 **Accessibility Compliance**
- WCAG 2.1 AA standards
- Keyboard navigation
- Screen reader compatibility

## Troubleshooting Common Issues

### Schema Validation Failures

```bash
# Problem: "Setting X defined but never used"
# Solution: Add Liquid usage or remove setting

# Problem: "Invalid range step calculation"
# Solution: Ensure (max - min) / step ≤ 101
```

### Asset Dependency Errors

```bash
# Problem: "Missing snippet X"
# Solution: Copy from code library or create

# Problem: "Asset not found"
# Solution: Check asset_url references and file existence
```

### Performance Issues

```bash
# Problem: Lighthouse score below 60
# Solution: Check image optimization, JS blocking, CSS size

# Problem: Slow theme editor
# Solution: Reduce complex animations, optimize CSS selectors
```

## Best Practices

### 🚀 **Performance First**
- Use CSS animations over JavaScript
- Optimize images with proper sizing
- Minimize global CSS/JS
- Implement lazy loading

### 🎯 **Schema Optimization**
- Only include settings that are actually used
- Group related settings logically
- Use appropriate setting types
- Provide helpful descriptions

### 🔧 **Development Efficiency**
- Use validation scripts early and often
- Fix issues immediately, don't accumulate
- Test in both editor and preview mode
- Document complex implementations

### 📱 **Mobile First**
- Test on real devices
- Use responsive design patterns
- Optimize touch interactions
- Consider slow network conditions

## Tool Configuration

### VS Code Settings

```json
{
  "liquid.format.enable": true,
  "liquid.validate.enable": true,
  "files.associations": {
    "*.liquid": "liquid"
  }
}
```

### Git Hooks

```bash
# .git/hooks/pre-commit (or scripts/git-hooks/pre-commit)
#!/bin/bash
exec ./scripts/pre-commit-schema-check.sh
```

### Theme Check Configuration

```yaml
# .theme-check.yml
extends: :theme_app_extension
ignore:
  - node_modules/**
  - scripts/**
ValidStaticBlockType:
  enabled: false  # For development themes
```

## Integration with Existing Tools

This workflow integrates seamlessly with:
- **Shopify CLI** theme development
- **GitHub Actions** for CI/CD
- **VS Code** Shopify Liquid extension
- **Theme Check** validation
- **Lighthouse CI** performance testing

---

*This workflow ensures Theme Store compliance and optimal developer experience while maintaining code quality and performance standards.*