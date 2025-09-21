# Ultimate Shopify Liquid Validation Suite

**Zero tolerance validation system for production-ready Shopify themes.**

## 🛡️ What This Does

This integrated validation suite combines the best validation tools into a single, comprehensive workflow that enforces zero tolerance for:

- **Hallucinated Liquid filters** (like `color_extract`, `rgb`)
- **Over-engineered complexity** (10+ filter chains, deeply nested logic)
- **Performance killers** (looping all products, unbounded collections)
- **Theme Store violations** (external scripts, console statements)
- **Schema integrity issues** (undefined settings, invalid ranges)
- **Syntax errors** (malformed JSON, broken Liquid)

## 🚀 Quick Start

### Essential Commands

```bash
# Quick development validation (recommended for daily use)
./scripts/validate-theme.sh development

# Deep validation before deployment
./scripts/validate-theme.sh deep

# Complete validation for Theme Store submission
./scripts/validate-theme.sh all

# Zero tolerance liquid validation only
./scripts/validate-theme.sh ultimate
```

## 📋 Validation Workflows

### Development Workflow (`development`)
**Fast validation for daily development work**
- ✅ Ultimate liquid validation (zero tolerance)
- ✅ Development theme-check (essential errors only)
- ⏱️ **~10-15 seconds**

### Deep Validation (`deep`)
**Pre-deployment validation**
- ✅ Ultimate liquid validation
- ✅ Schema integrity scan
- ✅ Comprehensive theme-check
- ⏱️ **~30-45 seconds**

### Complete Validation (`all`)
**Theme Store submission ready**
- ✅ Ultimate liquid validation
- ✅ Auto-correction
- ✅ Schema integrity scan
- ✅ Development theme-check
- ✅ Comprehensive theme-check
- ✅ Production theme-check
- ✅ JSON report generation
- ✅ Preset testing
- ⏱️ **~60-90 seconds**

## 🧩 Core Components

### 1. Ultimate Validator (`ultimate-validator.py`)
**The most comprehensive liquid validator**
- 758 lines of zero-tolerance validation rules
- Official Shopify filter verification
- Complexity pattern detection
- Performance killer identification
- Theme Store compliance checking
- Schema integrity validation

### 2. Schema Integrity Scanner (`scan-schema-integrity.py`)
**Deep schema validation**
- Settings defined vs used analysis
- Range validation formula checking
- Preset integrity verification
- Block settings validation
- Duplicate ID detection

### 3. Theme Check Integration (`validate-theme.sh`)
**Orchestrates all validation layers**
- Multiple validation configurations
- Auto-correction capabilities
- JSON report generation
- Preset testing
- Color-coded results

## 🔧 Advanced Usage

### Individual Validators

```bash
# Run only ultimate validation
./scripts/validate-theme.sh ultimate

# Run only schema integrity
./scripts/validate-theme.sh integrity

# Auto-fix correctable issues
./scripts/validate-theme.sh auto-fix

# Generate detailed JSON report
./scripts/validate-theme.sh report
```

### Python API Usage

```python
# Ultimate validator
from ultimate_validator import ShopifyLiquidValidator
validator = ShopifyLiquidValidator()
success = validator.scan_directory(Path("theme_directory"))

# Schema integrity
from scan_schema_integrity import scan_directory
success = scan_directory(Path("theme_directory"))
```

## 📊 Validation Levels

| Level | Description | Use Case | Speed |
|-------|-------------|----------|-------|
| `ultimate` | Zero tolerance liquid | Code review | Fast |
| `development` | Essential + ultimate | Daily dev | Fast |
| `integrity` | Schema deep scan | Pre-commit | Medium |
| `deep` | Ultimate + integrity + comprehensive | Pre-deployment | Medium |
| `all` | Complete validation | Theme Store | Slow |

## 🚨 Error Categories

### Critical Errors (Block Deployment)
- Hallucinated filters
- Schema violations
- Performance killers
- Theme Store violations

### Warnings (Review Recommended)
- Code complexity
- Unused settings
- Style inconsistencies

### Info (Advisory)
- Performance suggestions
- Best practice recommendations

## 🛠️ Configuration Files

### Development (`.theme-check-development.yml`)
- Fast validation for daily development
- Essential error checking only
- Translation checks disabled
- Undefined objects allowed for documentation

### Production (`.theme-check-production.yml`)
- Maximum validation for Theme Store
- All available checks enabled
- Translation requirements enforced
- Required theme structure validated

### Comprehensive (`.theme-check.yml`)
- Complete validation suite
- All checks at default levels
- Balanced between strictness and usability

## 📈 Integration Examples

### Git Pre-commit Hook
```bash
#!/bin/bash
# Add to .git/hooks/pre-commit
./scripts/validate-theme.sh development
if [ $? -ne 0 ]; then
    echo "❌ Validation failed - commit blocked"
    exit 1
fi
```

### CI/CD Pipeline
```yaml
# GitHub Actions example
- name: Validate Theme
  run: ./scripts/validate-theme.sh deep
```

### VS Code Task
```json
{
    "label": "Validate Theme",
    "type": "shell",
    "command": "./scripts/validate-theme.sh development",
    "group": "build"
}
```

## 🔍 What We Removed

**Redundant/Broken Scripts (Deleted):**
- ❌ `validate-all.py` - Broken orchestrator
- ❌ `advanced-liquid-validator.py` - Redundant with ultimate-validator
- ❌ `validate-richtext-presets.py` - Functionality absorbed
- ❌ `validate-schema-presets.sh` - Shell version redundant

**Why These Were Removed:**
- `validate-all.py` had critical Shopify CLI integration failures
- Multiple scripts had overlapping validation logic
- Shell and Python versions of same functionality
- Inconsistent execution environments

## 🎯 Best Practices

### Daily Development
```bash
# Before committing changes
./scripts/validate-theme.sh development
```

### Before Deployment
```bash
# Deep validation
./scripts/validate-theme.sh deep
```

### Theme Store Submission
```bash
# Complete validation
./scripts/validate-theme.sh all
```

### Code Review
```bash
# Focus on liquid quality
./scripts/validate-theme.sh ultimate
```

## 📚 Validation Rules

### Hallucinated Filters Detection
Catches non-existent filters like:
- `color_extract` → Use `color_brightness`, `color_lighten`
- `rgb` → Use CSS `rgb()` directly
- `get` → Use bracket notation `[key]`

### Performance Killers
Prevents theme-breaking patterns:
- `{% for product in collections.all.products %}`
- `collections.all.products.size`
- Unbounded collection loops

### Complexity Limits
Enforces readable code:
- Max 10 filter chains
- Max 4 nested if statements
- Max 3 nested loops

### Theme Store Compliance
Ensures Theme Store approval:
- No external scripts
- No console statements
- No alert dialogs

## 🆘 Troubleshooting

### Validation Fails
1. Run `./scripts/validate-theme.sh ultimate` to isolate issues
2. Check error messages for specific line numbers
3. Use `./scripts/validate-theme.sh auto-fix` for correctable issues

### Shopify CLI Issues
```bash
# Update Shopify CLI
npm install -g @shopify/cli@latest

# Verify installation
shopify version
```

### Performance Issues
- Large codebases: Use `development` mode for daily work
- CI/CD: Cache dependencies and use `deep` mode
- Local development: Run `ultimate` for quick feedback

## 📞 Support

- **File Issues**: Create GitHub issues for validation problems
- **Feature Requests**: Suggest improvements via GitHub discussions
- **Documentation**: All validation rules documented in source code

---

**This validation suite is designed for zero tolerance - if it passes here, it will work in production Shopify themes.**