# Platform-Specific Character Encoding Issues

**Complete reference for cross-platform character encoding compatibility in Shopify theme development**

*Consolidated from comprehensive CLI parsing limitations and platform difference analysis*

---

## Executive Summary

Platform-specific character encoding differences are a major source of Shopify theme upload failures. This guide addresses:

- **Development vs Production Environment Gaps** - Local tolerance vs upload strictness
- **Platform-Specific Character Handling** - Windows vs macOS vs Linux differences
- **Shopify CLI Parser Restrictions** - Technical limitations and validation requirements
- **Cross-Platform Compatibility Solutions** - Automated detection and prevention strategies

**Critical Finding**: What works in local development may fail during theme upload due to platform-specific character encoding differences and CLI parser limitations.

---

## 🚨 Critical Platform Compatibility Issues

### UTF-8 BOM (Byte Order Mark) Problems

#### Detection and Impact
```python
# BOM Detection
BOM_SIGNATURES = {
    b'\xef\xbb\xbf': 'UTF-8 BOM (CRITICAL - breaks CLI)',
    b'\xff\xfe': 'UTF-16 LE BOM',
    b'\xfe\xff': 'UTF-16 BE BOM',
    b'\xff\xfe\x00\x00': 'UTF-32 LE BOM',
    b'\x00\x00\xfe\xff': 'UTF-32 BE BOM'
}

def detect_bom(file_path):
    with open(file_path, 'rb') as f:
        first_bytes = f.read(4)

    for signature, bom_type in BOM_SIGNATURES.items():
        if first_bytes.startswith(signature):
            return {
                'bom_detected': True,
                'bom_type': bom_type,
                'severity': 'CRITICAL' if 'UTF-8 BOM' in bom_type else 'ERROR'
            }

    return {'bom_detected': False}
```

#### Platform-Specific BOM Issues
```
❌ CRITICAL - Causes immediate CLI upload failure:
Windows Notepad: Automatically adds UTF-8 BOM
Some editors: Default UTF-8 with BOM setting
Legacy tools: BOM insertion for "Unicode compatibility"

✅ SAFE - Required for CLI compatibility:
VS Code: UTF-8 without BOM (default)
Sublime Text: UTF-8 (no BOM option)
Vim/Neovim: set nobomb
```

### Control Character Restrictions

#### Critical Control Characters
```python
CONTROL_CHARACTER_RANGES = {
    'null_bytes': (0x00, 0x00),  # Immediate CLI failure
    'low_control': (0x01, 0x08),  # Parser errors
    'high_control': (0x0E, 0x1F),  # Encoding conflicts
    'del_character': (0x7F, 0x7F),  # Delete character
    'high_control_ext': (0x80, 0x9F),  # Extended control range
}

ALLOWED_CONTROL_CHARS = {0x09, 0x0A, 0x0D}  # Tab, LF, CR

def detect_control_characters(content):
    issues = []
    for i, char in enumerate(content):
        char_code = ord(char)

        if char_code < 0x20 and char_code not in ALLOWED_CONTROL_CHARS:
            issues.append({
                'position': i,
                'char_code': char_code,
                'char_name': f'\\x{char_code:02x}',
                'severity': 'CRITICAL' if char_code == 0x00 else 'ERROR'
            })
        elif 0x7F <= char_code <= 0x9F:
            issues.append({
                'position': i,
                'char_code': char_code,
                'char_name': f'\\x{char_code:02x}',
                'severity': 'ERROR'
            })

    return issues
```

---

## 🖥️ Platform-Specific Character Handling

### Windows Platform Issues

#### Character Encoding Conflicts
```batch
REM Common Windows encoding problems

REM Code page conflicts
:: Default: CP1252 (Windows-1252)
:: Required: UTF-8 (65001)
chcp 65001

REM Smart quotes from MS Office applications
:: " " → " " (ASCII quotes)
:: ' ' → ' ' (ASCII apostrophes)

REM Line ending conflicts
:: Windows: \r\n (CRLF)
:: Unix/Linux: \n (LF)
:: Mixed: Causes parsing errors
```

#### Windows-Specific Solutions
```batch
:: Configure UTF-8 environment
chcp 65001
set PYTHONIOENCODING=utf-8

:: Configure Git for Windows
git config core.autocrlf true
git config core.quotepath false
git config core.safecrlf true

:: Remove BOM from files
powershell "$content = Get-Content 'file.liquid' -Raw; $content = $content.TrimStart([char]0xFEFF); Set-Content 'file.liquid' -Value $content -Encoding UTF8NoBOM"

:: Validate file encoding
powershell "Get-Content file.liquid -Encoding UTF8 | Out-String -Width 1000"
```

#### Windows Development Environment Setup
```json
// VS Code settings.json for Windows
{
  "files.encoding": "utf8",
  "files.eol": "\n",
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true,
  "files.autoGuessEncoding": false,
  "editor.insertSpaces": true,
  "editor.tabSize": 2
}
```

### macOS Platform Issues

#### Unicode Normalization Conflicts
```bash
# macOS-specific Unicode normalization issues

# NFC vs NFD normalization differences
# APFS file system uses NFD (decomposed) normalization
# Web standards expect NFC (composed) normalization

# Example: café filename
# NFD: cafe\u0301 (e + combining acute accent)
# NFC: café (single precomposed character)

# Detection
python3 -c "
import unicodedata
import sys
filename = sys.argv[1]
nfc = unicodedata.normalize('NFC', filename)
nfd = unicodedata.normalize('NFD', filename)
if filename != nfc:
    print(f'Normalization issue: {filename} -> {nfc}')
" "café.liquid"
```

#### macOS-Specific Solutions
```bash
# Set proper UTF-8 locale environment
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Configure Git for macOS Unicode handling
git config core.precomposeunicode true
git config core.quotepath false

# Check and fix Unicode normalization
find . -name "*.liquid" -exec python3 -c "
import unicodedata
import sys
import os
filename = sys.argv[1]
normalized = unicodedata.normalize('NFC', filename)
if filename != normalized:
    print(f'Renaming: {filename} -> {normalized}')
    os.rename(filename, normalized)
" {} \;

# Remove invisible characters common on macOS
sed -i '' 's/\xE2\x80\x8B//g' *.liquid  # Zero-width space
sed -i '' 's/\xEF\xBB\xBF//g' *.liquid  # BOM removal
sed -i '' 's/\xE2\x80\x8C//g' *.liquid  # Zero-width non-joiner
sed -i '' 's/\xE2\x80\x8D//g' *.liquid  # Zero-width joiner
```

#### macOS Text Editor Issues
```bash
# Common macOS text editor problems

# TextEdit smart quotes (automatic)
# " " → " " (convert to ASCII)
# ' ' → ' ' (convert to ASCII)

# Xcode automatic indentation with non-breaking spaces
# \u00A0 (non-breaking space) → \u0020 (regular space)

# Terminal.app copy-paste encoding changes
# Smart quotes from web → ASCII quotes

# Prevention commands
defaults write NSGlobalDomain NSAutomaticQuoteSubstitutionEnabled -bool false
defaults write NSGlobalDomain NSAutomaticDashSubstitutionEnabled -bool false
```

### Linux Platform Issues

#### Locale and Character Set Problems
```bash
# Linux distribution character encoding differences

# Check current locale settings
locale
echo $LANG
echo $LC_ALL

# Common problematic configurations
LANG=C                    # ASCII only (breaks Unicode)
LC_CTYPE=en_US.iso88591  # ISO-8859-1 (breaks UTF-8)
LC_ALL=POSIX             # POSIX locale (limited Unicode)

# Required configuration
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8
```

#### Linux-Specific Solutions
```bash
# Ensure UTF-8 locale environment
if [ -z "$LC_ALL" ] || [ "$LC_ALL" != "en_US.UTF-8" ]; then
    export LANG=en_US.UTF-8
    export LC_ALL=en_US.UTF-8
fi

# Configure Git for Linux character handling
git config core.quotepath false
git config core.autocrlf input

# Character encoding validation
file -bi *.liquid | grep -v "charset=utf-8"

# Remove control characters (preserve tab, newline, CR)
tr -d '\000-\010\013\014\016-\037\177' < input.liquid > output.liquid

# Smart quote detection and replacement
grep -P '[""'']' *.liquid
sed -i 's/"/"/g; s/"/"/g; s/'/'"'"'/g; s/'/'"'"'/g' *.liquid

# Remove high control characters
sed -i 's/[\x80-\x9F]//g' *.liquid
```

---

## 🔧 Shopify CLI Parser Restrictions

### File Encoding Requirements

#### Mandatory Standards
```yaml
shopify_cli_requirements:
  encoding: "UTF-8 without BOM"
  line_endings: "Unix-style (LF) preferred"
  filename_charset: "ASCII-only recommended"
  control_characters: "Tab, LF, CR only"
  null_bytes: "Forbidden (immediate failure)"

validation_strictness:
  development_server: "Permissive (auto-correction)"
  theme_upload: "Strict (zero tolerance)"
  production_deploy: "Ultra-strict (compliance required)"
```

#### File Type Specific Restrictions
```python
FILE_TYPE_RESTRICTIONS = {
    'liquid': {
        'encoding': 'UTF-8 without BOM',
        'forbidden_chars': ['smart_quotes', 'em_dashes', 'unicode_variables'],
        'line_endings': 'Unix LF preferred',
        'validation_level': 'STRICT'
    },
    'json_schema': {
        'encoding': 'UTF-8 without BOM',
        'forbidden_chars': ['BOM', 'control_chars', 'html_entities'],
        'json_compliance': 'RFC 8259',
        'validation_level': 'ULTRA_STRICT'
    },
    'css': {
        'encoding': 'UTF-8 without BOM',
        'forbidden_chars': ['unicode_calc_operators', 'raw_unicode_content'],
        'charset_declaration': 'Optional @charset "UTF-8"',
        'validation_level': 'STRICT'
    },
    'javascript': {
        'encoding': 'UTF-8 without BOM',
        'forbidden_chars': ['liquid_interpolation', 'non_ascii_identifiers'],
        'context_separation': 'REQUIRED',
        'validation_level': 'STRICT'
    }
}
```

### Development vs Production Environment Gaps

#### Local Development Tolerance
```python
DEVELOPMENT_SERVER_BEHAVIOR = {
    'character_encoding': 'Permissive auto-correction',
    'browser_rendering': 'UTF-8 content handled gracefully',
    'hot_reload': 'May mask character encoding problems',
    'error_handling': 'Graceful degradation',
    'validation': 'Warning-level only'
}

PRODUCTION_UPLOAD_REALITY = {
    'character_encoding': 'Strict UTF-8 compliance required',
    'auto_correction': 'None - fails immediately',
    'binary_parsing': 'Fails silently with mixed encodings',
    'timeout_errors': 'Occur with problematic character sequences',
    'validation': 'Zero tolerance for violations'
}
```

#### Upload Validation Pipeline
```python
def simulate_cli_upload_validation(file_path):
    """Simulate Shopify CLI upload validation process"""

    # Step 1: Binary file analysis
    with open(file_path, 'rb') as f:
        raw_content = f.read()

    # Step 2: BOM detection (immediate failure)
    if raw_content.startswith(b'\xef\xbb\xbf'):
        return {'status': 'FAILED', 'error': 'UTF-8 BOM detected'}

    # Step 3: Null byte detection (immediate failure)
    if b'\x00' in raw_content:
        return {'status': 'FAILED', 'error': 'Null bytes detected'}

    # Step 4: UTF-8 decoding validation
    try:
        content = raw_content.decode('utf-8')
    except UnicodeDecodeError as e:
        return {'status': 'FAILED', 'error': f'Invalid UTF-8: {e}'}

    # Step 5: Control character scan
    control_chars = detect_control_characters(content)
    if any(c['severity'] == 'CRITICAL' for c in control_chars):
        return {'status': 'FAILED', 'error': 'Critical control characters'}

    # Step 6: File type specific validation
    if file_path.endswith('.liquid'):
        liquid_issues = validate_liquid_encoding(content)
        if any(i['severity'] == 'CRITICAL' for i in liquid_issues):
            return {'status': 'FAILED', 'error': 'Liquid encoding violations'}

    return {'status': 'PASSED', 'warnings': []}
```

---

## 🛠️ Cross-Platform Compatibility Solutions

### Automated Platform Detection and Normalization

#### Platform Environment Detection
```python
import platform
import sys
import locale

def detect_platform_environment():
    """Detect current platform and encoding environment"""

    env_info = {
        'platform': platform.system(),
        'platform_release': platform.release(),
        'python_version': sys.version,
        'default_encoding': sys.getdefaultencoding(),
        'filesystem_encoding': sys.getfilesystemencoding(),
        'locale_encoding': locale.getpreferredencoding(),
        'locale_info': locale.getlocale()
    }

    # Platform-specific checks
    if env_info['platform'] == 'Windows':
        env_info['code_page'] = get_windows_code_page()
        env_info['git_autocrlf'] = get_git_config('core.autocrlf')

    elif env_info['platform'] == 'Darwin':  # macOS
        env_info['unicode_normalization'] = get_macos_normalization()
        env_info['precompose_unicode'] = get_git_config('core.precomposeunicode')

    elif env_info['platform'] == 'Linux':
        env_info['lang_variable'] = os.environ.get('LANG', '')
        env_info['lc_all_variable'] = os.environ.get('LC_ALL', '')

    return env_info

def normalize_platform_encoding(content, target_platform='cli_compatible'):
    """Normalize content for cross-platform compatibility"""

    # Remove BOM if present
    if content.startswith('\ufeff'):
        content = content[1:]

    # Normalize line endings to Unix-style
    content = content.replace('\r\n', '\n').replace('\r', '\n')

    # Replace smart quotes with ASCII equivalents
    content = content.replace('"', '"').replace('"', '"')
    content = content.replace(''', "'").replace(''', "'")

    # Replace typography dashes with ASCII hyphens
    content = content.replace('—', '-').replace('–', '-')

    # Remove or replace control characters
    control_chars = ''.join(chr(i) for i in range(0x00, 0x20) if i not in [0x09, 0x0A, 0x0D])
    for char in control_chars:
        content = content.replace(char, '')

    # Platform-specific Unicode normalization
    if target_platform == 'macos' or target_platform == 'all':
        import unicodedata
        content = unicodedata.normalize('NFC', content)

    return content
```

### Pre-Commit Platform Validation

#### Git Hook Integration
```bash
#!/bin/bash
# .git/hooks/pre-commit
# Cross-platform character encoding validation

echo "🔍 Validating character encoding across platforms..."

# Get list of modified files
MODIFIED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(liquid|json|css|js)$')

if [ -z "$MODIFIED_FILES" ]; then
    echo "✅ No theme files to validate"
    exit 0
fi

# Validate each file
VALIDATION_FAILED=false

for file in $MODIFIED_FILES; do
    echo "Checking: $file"

    # BOM detection
    if file "$file" | grep -q "UTF-8 Unicode (with BOM)"; then
        echo "❌ UTF-8 BOM detected in $file"
        VALIDATION_FAILED=true
    fi

    # Control character detection
    if grep -P '[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]' "$file" > /dev/null 2>&1; then
        echo "❌ Control characters detected in $file"
        VALIDATION_FAILED=true
    fi

    # Smart quote detection
    if grep -P '[""'']' "$file" > /dev/null 2>&1; then
        echo "⚠️ Smart quotes detected in $file"
    fi

    # Platform-specific validation
    python3 -c "
import sys
sys.path.append('./scripts')
from platform_encoding_validator import validate_file_platform_compatibility
result = validate_file_platform_compatibility('$file')
if result['critical_issues']:
    print(f'❌ Platform compatibility issues in $file')
    sys.exit(1)
"

    if [ $? -ne 0 ]; then
        VALIDATION_FAILED=true
    fi
done

if [ "$VALIDATION_FAILED" = true ]; then
    echo "❌ Character encoding validation failed"
    echo "Run: python3 scripts/fix-platform-encoding.py --auto-fix"
    exit 1
fi

echo "✅ All files pass platform character encoding validation"
exit 0
```

### Automated Fix Scripts

#### Cross-Platform Character Normalization
```python
#!/usr/bin/env python3
"""
Cross-platform character encoding normalization script
Ensures files work correctly across Windows, macOS, and Linux
"""

import os
import sys
import glob
import argparse
import unicodedata
from pathlib import Path

class PlatformEncodingFixer:
    def __init__(self, auto_fix=False):
        self.auto_fix = auto_fix
        self.fixes_applied = []
        self.issues_found = []

    def fix_file(self, file_path):
        """Fix character encoding issues in a single file"""

        # Read file in binary mode to detect BOM
        with open(file_path, 'rb') as f:
            raw_content = f.read()

        fixes = []

        # Fix BOM
        if raw_content.startswith(b'\xef\xbb\xbf'):
            raw_content = raw_content[3:]
            fixes.append('Removed UTF-8 BOM')

        # Decode to text
        try:
            content = raw_content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                content = raw_content.decode('utf-8', errors='replace')
                fixes.append('Fixed UTF-8 decoding errors')
            except:
                self.issues_found.append(f'Cannot decode {file_path}')
                return False

        # Normalize Unicode (important for macOS)
        normalized_content = unicodedata.normalize('NFC', content)
        if normalized_content != content:
            content = normalized_content
            fixes.append('Normalized Unicode to NFC')

        # Fix line endings
        if '\r\n' in content or '\r' in content:
            content = content.replace('\r\n', '\n').replace('\r', '\n')
            fixes.append('Normalized line endings to Unix-style')

        # Fix smart quotes
        original_content = content
        content = content.replace('"', '"').replace('"', '"')
        content = content.replace(''', "'").replace(''', "'")
        if content != original_content:
            fixes.append('Replaced smart quotes with ASCII quotes')

        # Fix typography dashes
        original_content = content
        content = content.replace('—', '-').replace('–', '-')
        if content != original_content:
            fixes.append('Replaced typography dashes with ASCII hyphens')

        # Remove control characters (except tab, LF, CR)
        control_chars_removed = 0
        cleaned_content = ''
        for char in content:
            char_code = ord(char)
            if char_code < 0x20 and char_code not in [0x09, 0x0A, 0x0D]:
                control_chars_removed += 1
            elif 0x7F <= char_code <= 0x9F:
                control_chars_removed += 1
            else:
                cleaned_content += char

        if control_chars_removed > 0:
            content = cleaned_content
            fixes.append(f'Removed {control_chars_removed} control characters')

        # Apply fixes if auto-fix enabled
        if fixes and self.auto_fix:
            with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)

            self.fixes_applied.append({
                'file': file_path,
                'fixes': fixes
            })

            return True

        elif fixes:
            self.issues_found.append({
                'file': file_path,
                'fixes_needed': fixes
            })

            return False

        return True

    def fix_directory(self, directory):
        """Fix all theme files in directory"""

        theme_file_patterns = [
            '**/*.liquid',
            '**/*.json',
            '**/*.css',
            '**/*.js'
        ]

        files_processed = 0

        for pattern in theme_file_patterns:
            for file_path in glob.glob(os.path.join(directory, pattern), recursive=True):
                if os.path.isfile(file_path):
                    self.fix_file(file_path)
                    files_processed += 1

        return files_processed

    def report_results(self):
        """Print summary of fixes and issues"""

        if self.fixes_applied:
            print(f"✅ Applied fixes to {len(self.fixes_applied)} files:")
            for fix in self.fixes_applied:
                print(f"  📁 {fix['file']}")
                for fix_description in fix['fixes']:
                    print(f"    🔧 {fix_description}")

        if self.issues_found:
            print(f"⚠️ Found issues in {len(self.issues_found)} files:")
            for issue in self.issues_found:
                if isinstance(issue, dict):
                    print(f"  📁 {issue['file']}")
                    for fix_needed in issue['fixes_needed']:
                        print(f"    ❌ {fix_needed}")
                else:
                    print(f"  ❌ {issue}")

        if not self.fixes_applied and not self.issues_found:
            print("✅ All files already have correct platform encoding")

def main():
    parser = argparse.ArgumentParser(description='Fix cross-platform character encoding issues')
    parser.add_argument('path', nargs='?', default='.', help='File or directory to fix')
    parser.add_argument('--auto-fix', action='store_true', help='Automatically fix issues')
    parser.add_argument('--check-only', action='store_true', help='Check only, do not fix')

    args = parser.parse_args()

    fixer = PlatformEncodingFixer(auto_fix=args.auto_fix and not args.check_only)

    if os.path.isfile(args.path):
        fixer.fix_file(args.path)
    elif os.path.isdir(args.path):
        files_processed = fixer.fix_directory(args.path)
        print(f"Processed {files_processed} theme files")
    else:
        print(f"Error: {args.path} is not a valid file or directory")
        sys.exit(1)

    fixer.report_results()

    if fixer.issues_found and not args.auto_fix:
        print("\nRun with --auto-fix to automatically resolve these issues")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

## 📋 Platform Compatibility Checklist

### Development Environment Setup

#### Windows Development
- [ ] Set UTF-8 code page: `chcp 65001`
- [ ] Configure Git: `core.autocrlf=true`, `core.quotepath=false`
- [ ] Use UTF-8 compatible editors (VS Code, Sublime Text)
- [ ] Avoid Notepad for theme development
- [ ] Test with PowerShell UTF-8 validation

#### macOS Development
- [ ] Set UTF-8 locale: `export LC_ALL=en_US.UTF-8`
- [ ] Configure Git: `core.precomposeunicode=true`
- [ ] Disable smart quotes: System Preferences → Keyboard
- [ ] Use Unicode NFC normalization
- [ ] Test with Terminal.app encoding

#### Linux Development
- [ ] Ensure UTF-8 locale: `LANG=en_US.UTF-8`
- [ ] Configure Git: `core.quotepath=false`
- [ ] Validate character encoding tools available
- [ ] Test with distribution-specific tools
- [ ] Check terminal encoding settings

### Pre-Upload Validation
- [ ] Run BOM detection on all files
- [ ] Validate UTF-8 encoding compliance
- [ ] Check for control characters
- [ ] Test smart quote detection
- [ ] Verify line ending consistency
- [ ] Run platform compatibility script

### Post-Upload Verification
- [ ] Confirm theme upload success
- [ ] Test theme functionality across browsers
- [ ] Validate international character display
- [ ] Check for encoding errors in logs
- [ ] Verify cross-platform file accessibility

---

*This platform-specific guide ensures consistent character encoding behavior across all development environments and eliminates CLI upload failures due to platform differences.*