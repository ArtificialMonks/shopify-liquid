#!/bin/bash

# ==============================================================================
# Pre-Commit Comprehensive Validation Hook
# ==============================================================================
#
# Automatically validates Shopify Liquid files against the comprehensive
# validation checklist standards before commits. Implements progressive
# validation levels from LIQUID-VALIDATION-CHECKLIST.md.
#
# Validation Standards: /LIQUID-VALIDATION-CHECKLIST.md
#
# Usage: Run as Git pre-commit hook or manually:
#   ./scripts/pre-commit-schema-check.sh [validation_level]
#
# Validation Levels:
#   development  - Fast feedback with critical error detection (default)
#   production   - Theme Store compliance validation
#   ultimate     - Zero tolerance comprehensive validation
#
# Requirements:
#   - Python 3.x
#   - scan-schema-integrity.py script
#   - ultimate-validator.py script
#   - LIQUID-VALIDATION-CHECKLIST.md compliance
#   - Git repository
# ==============================================================================

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git rev-parse --show-toplevel)"
SCHEMA_SCANNER="$SCRIPT_DIR/scan-schema-integrity.py"
ULTIMATE_VALIDATOR="$SCRIPT_DIR/ultimate-validator.py"
VALIDATION_CHECKLIST="$REPO_ROOT/LIQUID-VALIDATION-CHECKLIST.md"
VALIDATION_LEVEL="${1:-development}"
THEME_DIR="${2:-$REPO_ROOT}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛡️ Pre-Commit Comprehensive Validation${NC}"
echo -e "${BLUE}📋 Validation Level: ${VALIDATION_LEVEL}${NC}"
echo -e "${BLUE}📖 Standards: LIQUID-VALIDATION-CHECKLIST.md${NC}"
echo "=================================================="

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Not in a git repository${NC}"
    exit 1
fi

# Check if required validation tools exist
if [[ ! -f "$SCHEMA_SCANNER" ]]; then
    echo -e "${RED}❌ Error: Schema scanner not found at $SCHEMA_SCANNER${NC}"
    exit 1
fi

if [[ ! -f "$ULTIMATE_VALIDATOR" ]]; then
    echo -e "${RED}❌ Error: Ultimate validator not found at $ULTIMATE_VALIDATOR${NC}"
    exit 1
fi

if [[ ! -f "$VALIDATION_CHECKLIST" ]]; then
    echo -e "${YELLOW}⚠️  Warning: Validation checklist not found at $VALIDATION_CHECKLIST${NC}"
    echo -e "${YELLOW}   Proceeding with basic validation only${NC}"
fi

# Get list of staged .liquid files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.liquid$' || true)

if [[ -z "$STAGED_FILES" ]]; then
    echo -e "${GREEN}✅ No .liquid files staged for commit${NC}"
    exit 0
fi

echo -e "${BLUE}📄 Staged .liquid files:${NC}"
echo "$STAGED_FILES" | sed 's/^/  • /'
echo

# Run comprehensive validation based on checklist standards
echo -e "${BLUE}🔍 Running ${VALIDATION_LEVEL} validation per checklist standards...${NC}"

# Create temporary files for validation results
SCHEMA_LOG="/tmp/schema-check.log"
ULTIMATE_LOG="/tmp/ultimate-validation.log"
COMBINED_LOG="/tmp/combined-validation.log"

# Initialize validation status
SCHEMA_PASSED=true
ULTIMATE_PASSED=true

# Step 1: Schema integrity validation (always run)
echo -e "${BLUE}🔍 Step 1: Schema integrity validation...${NC}"
if ! python3 "$SCHEMA_SCANNER" "$THEME_DIR" > "$SCHEMA_LOG" 2>&1; then
    SCHEMA_PASSED=false
fi

# Step 2: Comprehensive validation based on checklist level
case "$VALIDATION_LEVEL" in
    "development")
        echo -e "${BLUE}🔍 Step 2: Development validation (fast feedback)...${NC}"
        echo -e "${BLUE}📋 Checklist compliance: Critical errors only${NC}"
        if ! python3 "$ULTIMATE_VALIDATOR" "$THEME_DIR" > "$ULTIMATE_LOG" 2>&1; then
            # Filter for critical/error issues only for development level
            if grep -q "CRITICAL\|ERROR" "$ULTIMATE_LOG"; then
                ULTIMATE_PASSED=false
            fi
        fi
        ;;
    "production")
        echo -e "${BLUE}🔍 Step 2: Production validation (Theme Store ready)...${NC}"
        echo -e "${BLUE}📋 Checklist compliance: All compliance violations${NC}"
        if ! python3 "$ULTIMATE_VALIDATOR" "$THEME_DIR" > "$ULTIMATE_LOG" 2>&1; then
            ULTIMATE_PASSED=false
        fi
        ;;
    "ultimate")
        echo -e "${BLUE}🔍 Step 2: Ultimate validation (zero tolerance)...${NC}"
        echo -e "${BLUE}📋 Checklist compliance: Zero tolerance for any issues${NC}"
        if ! python3 "$ULTIMATE_VALIDATOR" "$THEME_DIR" > "$ULTIMATE_LOG" 2>&1; then
            ULTIMATE_PASSED=false
        fi
        ;;
    *)
        echo -e "${YELLOW}⚠️  Unknown validation level: $VALIDATION_LEVEL${NC}"
        echo -e "${YELLOW}   Using development level validation${NC}"
        if ! python3 "$ULTIMATE_VALIDATOR" "$THEME_DIR" > "$ULTIMATE_LOG" 2>&1; then
            if grep -q "CRITICAL\|ERROR" "$ULTIMATE_LOG"; then
                ULTIMATE_PASSED=false
            fi
        fi
        ;;
esac

# Combine validation results
{
    echo "📋 COMPREHENSIVE VALIDATION REPORT"
    echo "=================================="
    echo "Validation Level: $VALIDATION_LEVEL"
    echo "Standards: LIQUID-VALIDATION-CHECKLIST.md"
    echo ""
    echo "📊 RESULTS SUMMARY:"
    echo "Schema Integrity: $(if $SCHEMA_PASSED; then echo "✅ PASSED"; else echo "❌ FAILED"; fi)"
    echo "Checklist Compliance: $(if $ULTIMATE_PASSED; then echo "✅ PASSED"; else echo "❌ FAILED"; fi)"
    echo ""
    if [[ -f "$SCHEMA_LOG" ]]; then
        echo "📄 SCHEMA VALIDATION:"
        echo "---------------------"
        cat "$SCHEMA_LOG"
        echo ""
    fi
    if [[ -f "$ULTIMATE_LOG" ]]; then
        echo "📄 CHECKLIST VALIDATION:"
        echo "------------------------"
        cat "$ULTIMATE_LOG"
        echo ""
    fi
} > "$COMBINED_LOG"

# Determine final result
if $SCHEMA_PASSED && $ULTIMATE_PASSED; then
    echo -e "${GREEN}✅ All validations passed!${NC}"
    echo -e "${GREEN}🎉 Code complies with checklist standards${NC}"

    # Show summary of validation
    if grep -q "📊" "$COMBINED_LOG"; then
        echo -e "${BLUE}📊 Validation Summary:${NC}"
        grep -A 5 "📊 RESULTS SUMMARY:" "$COMBINED_LOG"
    fi

    exit 0
else
    echo -e "${RED}❌ Validation failed!${NC}"
    echo
    echo -e "${YELLOW}⚠️  Issues found:${NC}"
    cat "$COMBINED_LOG"
    echo
    echo -e "${YELLOW}💡 To fix these issues:${NC}"
    echo "  1. Review the LIQUID-VALIDATION-CHECKLIST.md for standards"
    echo "  2. Fix critical issues flagged by validation"
    echo "  3. Test with: python3 scripts/ultimate-validator.py $THEME_DIR"
    echo "  4. Run schema check: python3 scripts/scan-schema-integrity.py $THEME_DIR"
    echo "  5. Stage your fixes and commit again"
    echo
    echo -e "${BLUE}📖 Validation Standards Reference:${NC}"
    echo "   $VALIDATION_CHECKLIST"
    echo
    echo -e "${RED}🛑 Commit blocked to prevent non-compliant code${NC}"
    exit 1
fi