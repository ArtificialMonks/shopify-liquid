#!/bin/bash
# Pre-commit hook for CSS character encoding validation
# Prevents commits with CSS character encoding issues that break Shopify theme uploads

set -e

echo "🔍 CSS Character Encoding Validation..."

# Find the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CSS_VALIDATOR="$SCRIPT_DIR/css-character-validator.py"

# Check if validator exists
if [[ ! -f "$CSS_VALIDATOR" ]]; then
    echo "❌ CSS character validator not found: $CSS_VALIDATOR"
    exit 1
fi

# Find all CSS files staged for commit
staged_css_files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.css$' || true)

if [[ -z "$staged_css_files" ]]; then
    echo "✅ No CSS files to validate"
    exit 0
fi

echo "📄 Found CSS files to validate:"
echo "$staged_css_files" | sed 's/^/  • /'

# Create temporary directory for validation
temp_dir=$(mktemp -d)
validation_failed=false

# Validate each staged CSS file
while IFS= read -r file; do
    if [[ -f "$file" ]]; then
        echo "🔍 Validating: $file"

        # Copy file to temp location to avoid issues with git staging
        temp_file="$temp_dir/$(basename "$file")"
        cp "$file" "$temp_file"

        # Run validation
        if ! python3 "$CSS_VALIDATOR" --file "$temp_file" > /dev/null 2>&1; then
            echo "❌ CSS character encoding issues found in: $file"
            echo "   Run: python3 scripts/css-character-validator.py --file '$file' --fix"
            validation_failed=true
        else
            echo "   ✅ Passed"
        fi
    fi
done <<< "$staged_css_files"

# Cleanup
rm -rf "$temp_dir"

# Check validation results
if [[ "$validation_failed" = true ]]; then
    echo ""
    echo "🚨 CSS CHARACTER ENCODING VALIDATION FAILED!"
    echo ""
    echo "The following CSS files contain character encoding issues that will"
    echo "cause Shopify theme upload failures:"
    echo ""
    echo "💡 To fix issues automatically:"
    echo "   python3 scripts/css-character-validator.py --fix ."
    echo ""
    echo "💡 To validate specific files:"
    echo "   python3 scripts/css-character-validator.py --file path/to/file.css"
    echo ""
    echo "💡 To bypass this check (NOT RECOMMENDED):"
    echo "   git commit --no-verify"
    echo ""
    exit 1
fi

echo "✅ All CSS files passed character encoding validation!"
exit 0