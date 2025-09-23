# Shopify CLI Parsing Limitations Research

## Research Summary

Investigation of Shopify CLI parsing limitations and character restrictions that cause theme upload failures across different platforms and development environments.

## Platform-Specific Character Encoding Issues

### Windows Platform Issues

**Problematic Scenarios**:
- Code page 1252 vs UTF-8 conflicts
- Smart quotes from MS Word copy-paste: `"` `"`
- BOM insertion by Notepad and legacy editors
- Backslash path separators in asset references

**Common Errors**:
```
Error: Invalid character encoding in theme file
Theme upload failed: Character encoding mismatch
```

**Solutions**:
- Use UTF-8 compatible editors (VS Code, Sublime Text)
- Configure Git with `core.autocrlf=true`
- Avoid Notepad for theme development

### macOS Platform Issues

**Unicode Normalization Conflicts**:
- NFC vs NFD normalization differences
- Accented characters in filenames: `café.liquid`
- AppleScript quote conversion in text editors

**Detection**:
```bash
# Check for Unicode normalization issues
LC_ALL=C find . -name "*.liquid" | grep -P '[^\x00-\x7F]'
```

### Linux Platform Issues

**Locale and Charset Problems**:
- LANG environment variable conflicts
- Different UTF-8 implementations across distributions
- Terminal encoding vs file encoding mismatches

## Shopify CLI Character Restrictions

### File Encoding Requirements

**Mandatory Standards**:
- UTF-8 encoding without BOM
- Unix-style line endings (LF) preferred
- ASCII-only filenames for cross-platform compatibility

**Validation**:
```bash
# Check file encoding
file -bi theme-file.liquid
# Should output: text/html; charset=utf-8
```

### Character Set Limitations

**Forbidden Characters in Filenames**:
- High Unicode characters: `🚀` `💡` `café`
- Windows reserved characters: `< > : " | ? * \`
- Leading/trailing spaces or dots

**Liquid Variable Name Restrictions**:
- ASCII letters, numbers, underscore only
- Cannot start with numbers
- No accented characters: `naïve` → `naive`

## Development Server vs Production Upload Differences

### Local Development Tolerance

**Shopify CLI Development Server**:
- More permissive character encoding
- Browser auto-corrects some encoding issues
- Hot reload may mask character problems

### Production Upload Strictness

**Theme Upload Validation**:
- Strict UTF-8 validation
- Zero tolerance for encoding inconsistencies
- BOM characters cause immediate failures

### Character Encoding Issue Detection

**Critical Patterns**:
```python
CLI_ENCODING_ISSUES = [
    {
        'pattern': r'^\ufeff',  # BOM detection
        'message': 'UTF-8 BOM detected - causes CLI upload failure',
        'severity': 'CRITICAL'
    },
    {
        'pattern': r'[\u0000-\u001F\u007F-\u009F]',  # Control characters
        'message': 'Control characters cause parsing errors',
        'severity': 'ERROR'
    },
    {
        'pattern': r'[""'']',  # Smart quotes
        'message': 'Smart quotes in code context cause encoding issues',
        'severity': 'WARNING'
    },
    {
        'pattern': r'[–—]',  # Em/en dashes
        'message': 'Typography dashes may cause encoding problems',
        'severity': 'WARNING'
    }
]
```

## Network and Transfer Encoding Issues

### HTTP Transfer Problems

**Character Encoding During Upload**:
- Content-Type header mismatches
- gzip compression encoding conflicts
- Network proxy character transformation

**Validation**:
```bash
# Test upload encoding
shopify theme push --development --verbose
```

### CDN and Asset Delivery

**Asset Encoding Issues**:
- CSS files with non-ASCII characters
- JavaScript files with Unicode literals
- Image alt text with high Unicode characters

## Automated Detection and Prevention

### Pre-Upload Validation Script

```python
def validate_cli_encoding_compatibility(file_path):
    """Validate file for Shopify CLI compatibility"""
    with open(file_path, 'rb') as f:
        raw_content = f.read()

    # Check for BOM
    if raw_content.startswith(b'\xef\xbb\xbf'):
        return {'error': 'UTF-8 BOM detected', 'severity': 'CRITICAL'}

    # Check for null bytes
    if b'\x00' in raw_content:
        return {'error': 'Null bytes detected', 'severity': 'CRITICAL'}

    # Validate UTF-8 encoding
    try:
        content = raw_content.decode('utf-8')
    except UnicodeDecodeError:
        return {'error': 'Invalid UTF-8 encoding', 'severity': 'CRITICAL'}

    return {'status': 'valid'}
```

### Character Substitution for CLI Compatibility

```python
def make_cli_compatible(content):
    """Convert content to CLI-compatible encoding"""

    # Remove BOM if present
    if content.startswith('\ufeff'):
        content = content[1:]

    # Replace smart quotes
    content = content.replace('"', '"').replace('"', '"')
    content = content.replace(''', "'").replace(''', "'")

    # Replace typography dashes
    content = content.replace('—', '-').replace('–', '-')

    # Remove or replace control characters
    control_chars = ''.join(chr(i) for i in range(0x00, 0x20) if i not in [0x09, 0x0A, 0x0D])
    for char in control_chars:
        content = content.replace(char, '')

    return content
```

## Platform-Specific Commands

### Windows Development Environment

```batch
:: Set UTF-8 code page
chcp 65001

:: Configure Git for Windows
git config core.autocrlf true
git config core.quotepath false

:: Validate file encoding
powershell "Get-Content file.liquid -Encoding UTF8"
```

### macOS Development Environment

```bash
# Set UTF-8 locale
export LC_ALL=en_US.UTF-8

# Configure Git for macOS
git config core.precomposeunicode true
git config core.quotepath false

# Check Unicode normalization
python3 -c "import unicodedata; print(unicodedata.normalize('NFC', 'café'))"
```

### Linux Development Environment

```bash
# Ensure UTF-8 locale
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Configure Git for Linux
git config core.quotepath false

# Validate character encoding
file -bi *.liquid | grep -v "charset=utf-8"
```

## Prevention Best Practices

### Editor Configuration

**VS Code Settings**:
```json
{
  "files.encoding": "utf8",
  "files.eol": "\n",
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true
}
```

**Git Configuration**:
```bash
# Prevent encoding issues in Git
git config core.safecrlf true
git config core.autocrlf input  # Linux/macOS
git config core.autocrlf true   # Windows
```

### Development Workflow

1. **Use UTF-8 compatible editors** (VS Code, Sublime Text, Vim)
2. **Configure proper Git settings** for line endings and encoding
3. **Validate encoding before commits** with pre-commit hooks
4. **Test uploads on target platform** before production deployment
5. **Use ASCII-only filenames** for maximum compatibility

## Error Message Reference

| Error Message | Cause | Solution |
|---------------|-------|----------|
| "Invalid character encoding" | BOM or non-UTF-8 | Save as UTF-8 without BOM |
| "Malformed file content" | Control characters | Remove invisible characters |
| "Theme upload failed" | Platform encoding mismatch | Normalize character encoding |
| "Asset processing error" | Non-ASCII filenames | Use ASCII-only filenames |

## Validation Integration

```bash
# Add to CI/CD pipeline
./scripts/validate-cli-encoding.py --strict
shopify theme check --category=encoding
```

This comprehensive research provides the foundation for preventing CLI upload failures through proper character encoding management across all development platforms.