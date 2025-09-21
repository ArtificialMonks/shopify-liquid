#!/bin/bash

# ==============================================================================
# Pre-Commit Schema Validation Hook
# ==============================================================================
#
# Automatically validates Shopify theme schema integrity before commits.
# Prevents schema errors from being committed to the repository.
#
# Usage: Run as Git pre-commit hook or manually:
#   ./scripts/pre-commit-schema-check.sh
#
# Requirements:
#   - Python 3.x
#   - scan-schema-integrity.py script
#   - Git repository
# ==============================================================================

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git rev-parse --show-toplevel)"
SCHEMA_SCANNER="$SCRIPT_DIR/scan-schema-integrity.py"
THEME_DIR="${1:-$REPO_ROOT}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Pre-Commit Schema Validation${NC}"
echo "=================================================="

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Not in a git repository${NC}"
    exit 1
fi

# Check if schema scanner exists
if [[ ! -f "$SCHEMA_SCANNER" ]]; then
    echo -e "${RED}❌ Error: Schema scanner not found at $SCHEMA_SCANNER${NC}"
    exit 1
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

# Run schema integrity validation
echo -e "${BLUE}🔍 Running schema integrity validation...${NC}"

if python3 "$SCHEMA_SCANNER" "$THEME_DIR" > /tmp/schema-check.log 2>&1; then
    echo -e "${GREEN}✅ Schema validation passed!${NC}"

    # Show summary of validation
    if grep -q "📊 Summary:" /tmp/schema-check.log; then
        echo -e "${BLUE}📊 Validation Summary:${NC}"
        grep -A 10 "📊 Summary:" /tmp/schema-check.log | head -6
    fi

    exit 0
else
    echo -e "${RED}❌ Schema validation failed!${NC}"
    echo
    echo -e "${YELLOW}⚠️  Issues found:${NC}"
    cat /tmp/schema-check.log
    echo
    echo -e "${YELLOW}💡 To fix these issues:${NC}"
    echo "  1. Review unused settings and remove them if not needed"
    echo "  2. Implement proper Liquid usage for defined settings"
    echo "  3. Run: python3 scripts/scan-schema-integrity.py $THEME_DIR"
    echo "  4. Stage your fixes and commit again"
    echo
    echo -e "${RED}🛑 Commit blocked to prevent schema issues${NC}"
    exit 1
fi