# Enhanced Shopify Liquid Validation Suite

**Comprehensive validation system implementing LIQUID-VALIDATION-CHECKLIST.md standards for production-ready Shopify themes.**

> 📋 **Validation Standards**: All validation follows the comprehensive standards defined in [`/LIQUID-VALIDATION-CHECKLIST.md`](../LIQUID-VALIDATION-CHECKLIST.md)

## 🛡️ What This Does

This integrated validation suite combines the best validation tools into a single, comprehensive workflow that enforces zero tolerance for:

- **🆕 Comprehensive Liquid syntax errors** (python-liquid integration with multi-level validation)
- **Hallucinated Liquid filters** (60+ official Shopify filters validated)
- **Over-engineered complexity** (10+ filter chains, deeply nested logic)
- **Performance killers** (looping all products, unbounded collections)
- **Theme Store violations** (external scripts, console statements)
- **Schema integrity issues** (undefined settings, invalid ranges)
- **Advanced syntax patterns** (tag pairing, schema block validation)

## 🚀 Quick Start

### Essential Commands

```bash
# 🆕 Liquid syntax validation only (zero tolerance)
./scripts/validate-theme.sh syntax

# Quick development validation with liquid syntax (recommended for daily use)
./scripts/validate-theme.sh development

# 🆕 Ultimate validation (comprehensive liquid syntax + theme validation)
./scripts/validate-theme.sh ultimate

# 🆕 Deep validation (ultimate + integrity + comprehensive)
./scripts/validate-theme.sh deep

# Complete validation for Theme Store submission
./scripts/validate-theme.sh all

# Advanced Python validation
python scripts/liquid-syntax-validator.py shopify-liquid-guides/code-library/
```

## 📋 Validation Workflows (Per LIQUID-VALIDATION-CHECKLIST.md)

### Development Level (`development`)
**Fast feedback with critical error detection** (Checklist Level 1)
- ✅ Critical Liquid syntax errors only
- ✅ Performance killer detection
- ✅ Hallucinated filter detection
- ✅ Security validation (error level)
- ⏱️ **~10-15 seconds**

### Production Level (`production`)
**Theme Store compliance validation** (Checklist Level 2)
- ✅ All development checks
- ✅ Theme Store compliance patterns
- ✅ Security requirements
- ✅ Accessibility validation
- ✅ Performance thresholds
- ⏱️ **~20-30 seconds**

### Ultimate Level (`ultimate`)
**Zero tolerance comprehensive validation** (Checklist Level 3)
- ✅ All production checks
- ✅ Code complexity analysis
- ✅ Cross-domain integration
- ✅ Complete accessibility compliance
- ✅ Advanced security patterns
- ⏱️ **~30-45 seconds**

### Deep Validation (`deep`) 🆕
**Pre-deployment validation**
- ✅ 🆕 Ultimate validation (liquid syntax + theme)
- ✅ Schema integrity scan
- ✅ Comprehensive theme-check
- ⏱️ **~30-45 seconds**

### Complete Validation (`all`)
**Theme Store submission ready**
- ✅ 🆕 Liquid syntax validation (comprehensive)
- ✅ Ultimate liquid validation (zero tolerance)
- ✅ Auto-correction
- ✅ Schema integrity scan
- ✅ Development theme-check
- ✅ Comprehensive theme-check
- ✅ Production theme-check
- ✅ JSON report generation
- ✅ Preset testing
- ⏱️ **~60-90 seconds**

## 🧩 Core Components

### 1. 🆕 Liquid Syntax Validator (`liquid-syntax-validator.py`)
**Comprehensive Liquid syntax validation with python-liquid integration**
- Multi-level validation (fast/standard/comprehensive)
- Python-liquid parser integration for accurate syntax checking
- Official Shopify filter validation (60+ documented filters)
- Tag pairing validation (for/endfor, if/endif, etc.)
- Schema block validation and exclusion
- Performance pattern detection
- Advanced error reporting with line numbers

### 2. Enhanced Ultimate Validator (`ultimate-validator.py`)
**The most comprehensive liquid validator with syntax integration**
- 800+ lines of zero-tolerance validation rules
- 🆕 Liquid syntax validation integration
- Official Shopify filter verification
- Complexity pattern detection
- Performance killer identification
- Theme Store compliance checking
- Schema integrity validation

### 3. Schema Integrity Scanner (`scan-schema-integrity.py`)
**Deep schema validation**
- Settings defined vs used analysis
- Range validation formula checking
- Preset integrity verification
- Block settings validation
- Duplicate ID detection

### 4. Theme Check Integration (`validate-theme.sh`)
**Orchestrates all validation layers**
- Multiple validation configurations
- 🆕 Liquid syntax validation integration
- Auto-correction capabilities
- JSON report generation
- Preset testing
- Color-coded results

### 5. 🆕 Enhanced Testing Suite
**Comprehensive validation testing and benchmarking**

#### Validation Accuracy Testing (`test-validator-accuracy.py`)
- Tests validator accuracy against known issues
- Validates detection of hallucinated filters
- Performance pattern recognition testing
- Schema validation accuracy

#### Integration Testing (`test-validator-integration.py`)
- End-to-end validation workflow testing
- Cross-validator integration validation
- File type detection accuracy
- Error reporting consistency

#### Test Suite Runner (`run-validator-tests.sh`)
- Orchestrates complete test suite
- Accuracy and integration testing
- Performance benchmarking
- Test result reporting

#### Performance Benchmarking (`benchmark-validator.py`)
- Validation performance analysis
- Large codebase testing
- Memory usage optimization
- Speed optimization validation

## 🔧 Advanced Usage

### Individual Validators

```bash
# 🆕 Run only liquid syntax validation
./scripts/validate-theme.sh syntax

# Run ultimate validation (liquid syntax + theme)
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
# Method 1: Using the validator_module wrapper (RECOMMENDED)
from scripts.validator_module import UltimateShopifyValidator, import_hyphenated_module
from pathlib import Path

# Ultimate validator (easy import)
validator = UltimateShopifyValidator(validation_level="production")
success = validator.scan_directory(Path("theme_directory"))

# Other hyphenated modules using helper function
liquid_validator = import_hyphenated_module("liquid-syntax-validator.py")
validator = liquid_validator.ShopifyLiquidSyntaxValidator()
success = validator.validate_directory(Path("theme_directory"))

schema_integrity = import_hyphenated_module("scan-schema-integrity.py")
success = schema_integrity.scan_directory(Path("theme_directory"))
```

```python
# Method 2: Manual importlib (for reference)
import importlib.util
from pathlib import Path

# Ultimate validator with validation level support
spec = importlib.util.spec_from_file_location("ultimate_validator", "scripts/ultimate-validator.py")
ultimate_validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ultimate_validator)
validator = ultimate_validator.ShopifyLiquidValidator(validation_level="development")
success = validator.scan_directory(Path("theme_directory"))
```

## 📊 Validation Levels (LIQUID-VALIDATION-CHECKLIST.md Compliance)

| Level | Checklist Level | Description | Severity Filter | Use Case | Speed |
|-------|----------------|-------------|-----------------|----------|-------|
| `development` | Level 1 | Fast feedback | Critical + Error only | Daily dev | Fast |
| `production` | Level 2 | Theme Store ready | Critical + Error + Warning | Pre-deployment | Medium |
| `ultimate` | Level 3 | Zero tolerance | All issues | Code review | Medium |
| `syntax` | - | Liquid syntax only | All syntax issues | Syntax checking | Very Fast |
| `integrity` | - | Schema deep scan | Schema issues | Pre-commit | Medium |
| `deep` | - | All validations | All issues | Comprehensive | Slow |
| `all` | - | Complete workflow | All issues | Theme Store | Slowest |

## 🚨 Error Categories

### Critical Errors (Block Deployment)
- 🆕 Liquid syntax errors (comprehensive python-liquid validation)
- Hallucinated filters (60+ official Shopify filters validated)
- Schema violations
- Performance killers
- Theme Store violations
- Tag pairing errors
- Invalid filter combinations

### Warnings (Review Recommended)
- Code complexity
- Unused settings
- Style inconsistencies
- 🆕 Advanced Liquid patterns
- Performance patterns

### Info (Advisory)
- Performance suggestions
- Best practice recommendations
- 🆕 Syntax optimization suggestions
- Filter usage improvements

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

## 🎯 Best Practices (Following LIQUID-VALIDATION-CHECKLIST.md)

### Daily Development (Level 1 - Development)
```bash
# Fast feedback with critical error detection
./scripts/validate-theme.sh development
```

### Pre-Deployment (Level 2 - Production)
```bash
# Theme Store compliance validation
./scripts/validate-theme.sh production
```

### Code Review (Level 3 - Ultimate)
```bash
# Zero tolerance comprehensive validation
./scripts/validate-theme.sh ultimate
```

### Theme Store Submission
```bash
# Complete validation workflow
./scripts/validate-theme.sh all
```

### Checklist Compliance Testing
```bash
# Test that validation implements checklist standards
python scripts/test-checklist-compliance.py
```

## 📋 LIQUID-VALIDATION-CHECKLIST.md Integration

This validation suite implements all standards defined in [`/LIQUID-VALIDATION-CHECKLIST.md`](../LIQUID-VALIDATION-CHECKLIST.md):

### Progressive Validation Levels
- **Development**: Fast feedback - critical errors only
- **Production**: Theme Store compliance - errors + warnings
- **Ultimate**: Zero tolerance - all issues

### Implemented Checklist Sections
- ✅ **Section 1**: Liquid Syntax & Structure validation
- ✅ **Section 2**: Filter validation (60+ official Shopify filters)
- ✅ **Section 3**: Performance anti-patterns (CRITICAL)
- ✅ **Section 4**: Security validation (ERROR LEVEL)
- ✅ **Section 5**: Schema configuration (Context-aware)

### Automated Validation Criteria
- Performance killer detection (`collections.all.products`)
- Hallucinated filter detection (`color_extract`, `rgb`, etc.)
- Security pattern validation (unescaped content)
- Schema integrity checks (range steps, valid types)
- Accessibility compliance (WCAG 2.1 AA)

### Manual Review Integration
- Clear error messages with checklist references
- Severity filtering based on validation level
- Actionable suggestions for issue resolution
- Cross-domain validation intersections

### Compliance Testing
```bash
# Verify checklist implementation
python scripts/test-checklist-compliance.py

# Pre-commit with checklist standards
./scripts/pre-commit-schema-check.sh development

# Production readiness with checklist
./scripts/validate-theme.sh production
```

## 📚 Enhanced Validation Rules

### 🆕 Comprehensive Liquid Syntax Validation
**Python-liquid integration with multi-level validation:**
- **Fast**: Quick syntax checks for development
- **Standard**: Complete syntax validation (default)
- **Comprehensive**: Deep validation with all checks

### Official Shopify Filter Validation (60+ Filters)
Validates against official Shopify filter documentation:
- **Existing filters**: `escape`, `truncate`, `date`, `money`, etc.
- **Deprecated filters**: Warns about legacy usage
- **Invalid filters**: Catches hallucinated filters

### Hallucinated Filters Detection
Catches non-existent filters like:
- `color_extract` → Use `color_brightness`, `color_lighten`
- `rgb` → Use CSS `rgb()` directly
- `get` → Use bracket notation `[key]`
- `nonexistent_filter` → Validated against official filter list

### 🆕 Advanced Performance Pattern Detection
Prevents theme-breaking patterns:
- `{% for product in collections.all.products %}`
- `collections.all.products.size`
- Unbounded collection loops
- Complex nested loops with performance implications
- Heavy computation in liquid templates
- Inefficient data access patterns

### 🆕 Enhanced Complexity Limits
Enforces readable code:
- Max 10 filter chains
- Max 4 nested if statements
- Max 3 nested loops
- Tag pairing validation (for/endfor, if/endif)
- Schema block validation and exclusion
- Proper liquid tag structure

### Theme Store Compliance
Ensures Theme Store approval:
- No external scripts
- No console statements
- No alert dialogs

## 🆘 Troubleshooting

### Validation Fails
1. Run `./scripts/validate-theme.sh syntax` to isolate Liquid syntax issues
2. Run `./scripts/validate-theme.sh ultimate` to check comprehensive validation
3. Check error messages for specific line numbers
4. Use `./scripts/validate-theme.sh auto-fix` for correctable issues
5. Run individual Python validators for detailed analysis:
   ```bash
   python scripts/liquid-syntax-validator.py shopify-liquid-guides/code-library/
   ```

### Shopify CLI Issues
```bash
# Update Shopify CLI
npm install -g @shopify/cli@latest

# Verify installation
shopify version
```

### Performance Issues
- Large codebases: Use `syntax` or `development` mode for daily work
- CI/CD: Cache dependencies and use `deep` mode
- Local development: Run `syntax` for quick syntax feedback
- Comprehensive validation: Use `ultimate` for thorough checking
- Testing: Use the test suite to validate performance:
  ```bash
  ./scripts/run-validator-tests.sh
  python scripts/benchmark-validator.py
  ```

## 📞 Support

- **File Issues**: Create GitHub issues for validation problems
- **Feature Requests**: Suggest improvements via GitHub discussions
- **Documentation**: All validation rules documented in source code

---

## 🆕 **Recent Enhancements**

### Latest Updates
- **Comprehensive Liquid Syntax Validation**: Python-liquid integration with multi-level validation
- **Official Shopify Filter Validation**: 60+ documented filters validation
- **Enhanced Testing Suite**: Accuracy, integration, and performance testing
- **Performance Benchmarking**: Advanced performance analysis and optimization
- **Tag Pairing Validation**: Complete Liquid syntax structure validation
- **Schema Block Validation**: Advanced schema validation with exclusion support

### New Commands
- `syntax` - Liquid syntax validation only
- `ultimate` - Enhanced with comprehensive liquid syntax validation
- `deep` - Enhanced with ultimate validation integration

---

**This enhanced validation suite with comprehensive Liquid syntax validation is designed for zero tolerance - if it passes here, it will work in production Shopify themes.**