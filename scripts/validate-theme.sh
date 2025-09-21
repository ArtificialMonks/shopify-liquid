#!/bin/bash

# Ultimate Theme Validation Script
# Provides comprehensive validation with multiple levels

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Ultimate Shopify Theme Validation Suite${NC}"
echo "=================================================="

# Check if Shopify CLI is installed
if ! command -v shopify &> /dev/null; then
    echo -e "${RED}❌ Shopify CLI not found. Please install with: npm install -g @shopify/cli${NC}"
    exit 1
fi

# Get Shopify CLI version
SHOPIFY_VERSION=$(shopify version 2>/dev/null | head -1 || echo "Unknown")
echo -e "${GREEN}✅ Shopify CLI found: $SHOPIFY_VERSION${NC}"

# Function to run validation with specific config
run_validation() {
    local name="$1"
    local config="$2"
    local description="$3"

    echo ""
    echo -e "${BLUE}🔍 Running $name Validation${NC}"
    echo "Description: $description"
    echo "Config: $config"
    echo "----------------------------------------"

    if shopify theme check --config "$config"; then
        echo -e "${GREEN}✅ $name validation passed!${NC}"
        return 0
    else
        echo -e "${RED}❌ $name validation failed!${NC}"
        return 1
    fi
}

# Function to run auto-correction
run_auto_correct() {
    echo ""
    echo -e "${YELLOW}🔧 Running Auto-Correction${NC}"
    echo "Attempting to fix automatically correctable issues..."
    echo "----------------------------------------"

    if shopify theme check --auto-correct --config .theme-check-development.yml; then
        echo -e "${GREEN}✅ Auto-correction completed!${NC}"
    else
        echo -e "${YELLOW}⚠️  Some issues could not be auto-corrected${NC}"
    fi
}

# Function to run ultimate liquid validation
run_ultimate_validation() {
    echo ""
    echo -e "${YELLOW}🛡️ Running Ultimate Liquid Validation${NC}"
    echo "Zero tolerance validation with comprehensive checks..."
    echo "- Hallucinated filter detection"
    echo "- Over-engineering detection"
    echo "- Performance killer detection"
    echo "- Theme Store compliance"
    echo "- Schema integrity validation"
    echo "----------------------------------------"

    if python3 "${SCRIPT_DIR}/ultimate-validator.py" --all >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Ultimate validation passed!${NC}"
        return 0
    else
        echo -e "${RED}❌ Ultimate validation failed!${NC}"
        python3 "${SCRIPT_DIR}/ultimate-validator.py" --all
        return 1
    fi
}

# Function to run comprehensive schema integrity scan
run_schema_integrity_scan() {
    echo ""
    echo -e "${YELLOW}🔍 Running Schema Integrity Scan${NC}"
    echo "Deep validation of schema consistency and preset integrity..."
    echo "----------------------------------------"

    if python3 "${SCRIPT_DIR}/scan-schema-integrity.py" --all >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Schema integrity scan passed!${NC}"
        return 0
    else
        echo -e "${RED}❌ Schema integrity scan failed!${NC}"
        python3 "${SCRIPT_DIR}/scan-schema-integrity.py" --all
        return 1
    fi
}

# Function to generate JSON report
generate_json_report() {
    echo ""
    echo -e "${BLUE}📊 Generating JSON Report${NC}"
    echo "Creating detailed validation report..."
    echo "----------------------------------------"

    shopify theme check --output json --config .theme-check.yml > theme-validation-report.json
    echo -e "${GREEN}✅ JSON report saved to: theme-validation-report.json${NC}"
}

# Function to test different validation presets
test_presets() {
    echo ""
    echo -e "${BLUE}🎯 Testing Shopify Validation Presets${NC}"
    echo "----------------------------------------"

    echo "Testing recommended preset..."
    shopify theme check --config theme-check:recommended --fail-level warning || true

    echo ""
    echo "Testing all checks preset..."
    shopify theme check --config theme-check:all --fail-level error || true

    echo ""
    echo "Testing theme app extension preset..."
    shopify theme check --config theme-check:theme-app-extension --fail-level error || true
}

# Main validation logic
main() {
    case "${1:-all}" in
        "development")
            echo "Running development validation with ultimate checks..."

            # 1. Ultimate liquid validation (includes schema integrity)
            run_ultimate_validation
            ultimate_result=$?

            # 2. Basic development validation
            run_validation "Development" ".theme-check-development.yml" "Fast development validation"
            dev_result=$?

            # Summary for development mode
            echo ""
            echo -e "${BLUE}📋 Development Validation Summary${NC}"
            echo "================================"

            if [ $ultimate_result -eq 0 ]; then
                echo -e "${GREEN}✅ Ultimate validation: PASSED${NC}"
            else
                echo -e "${RED}❌ Ultimate validation: FAILED${NC}"
            fi

            if [ $dev_result -eq 0 ]; then
                echo -e "${GREEN}✅ Theme Check: PASSED${NC}"
            else
                echo -e "${RED}❌ Theme Check: FAILED${NC}"
            fi

            if [ $ultimate_result -eq 0 ] && [ $dev_result -eq 0 ]; then
                echo -e "${GREEN}🎉 Development validation passed!${NC}"
                exit 0
            else
                echo -e "${RED}🚨 Development validation failed!${NC}"
                exit 1
            fi
            ;;
        "production")
            run_validation "Production" ".theme-check-production.yml" "Comprehensive Theme Store submission validation"
            ;;
        "comprehensive")
            run_validation "Comprehensive" ".theme-check.yml" "Complete validation with all available checks"
            ;;
        "auto-fix")
            run_auto_correct
            ;;
        "ultimate")
            run_ultimate_validation
            ;;
        "integrity")
            run_schema_integrity_scan
            ;;
        "report")
            generate_json_report
            ;;
        "presets")
            test_presets
            ;;
        "deep")
            echo "Running deep validation with ultimate checks..."

            # 1. Ultimate liquid validation (comprehensive)
            run_ultimate_validation
            ultimate_result=$?

            # 2. Schema integrity scan (specialized)
            run_schema_integrity_scan
            integrity_result=$?

            # 3. Comprehensive validation (theme-check)
            run_validation "Comprehensive" ".theme-check.yml" "Complete validation suite"
            comp_result=$?

            # Summary
            echo ""
            echo -e "${BLUE}📋 Deep Validation Summary${NC}"
            echo "================================"

            if [ $ultimate_result -eq 0 ]; then
                echo -e "${GREEN}✅ Ultimate liquid validation: PASSED${NC}"
            else
                echo -e "${RED}❌ Ultimate liquid validation: FAILED${NC}"
            fi

            if [ $integrity_result -eq 0 ]; then
                echo -e "${GREEN}✅ Schema integrity scan: PASSED${NC}"
            else
                echo -e "${RED}❌ Schema integrity scan: FAILED${NC}"
            fi

            if [ $comp_result -eq 0 ]; then
                echo -e "${GREEN}✅ Comprehensive validation: PASSED${NC}"
            else
                echo -e "${RED}❌ Comprehensive validation: FAILED${NC}"
            fi

            if [ $ultimate_result -eq 0 ] && [ $integrity_result -eq 0 ] && [ $comp_result -eq 0 ]; then
                echo -e "${GREEN}🎉 All deep validation checks passed!${NC}"
                exit 0
            else
                echo -e "${RED}🚨 Some validation checks failed!${NC}"
                exit 1
            fi
            ;;
        "all")
            echo "Running complete validation suite..."

            # 1. Ultimate liquid validation (most comprehensive)
            run_ultimate_validation
            ultimate_result=$?

            # 2. Auto-correction
            run_auto_correct

            # 3. Schema integrity scan (specialized checks)
            run_schema_integrity_scan
            integrity_result=$?

            # 4. Development validation
            run_validation "Development" ".theme-check-development.yml" "Fast development validation"
            dev_result=$?

            # 5. Comprehensive validation
            run_validation "Comprehensive" ".theme-check.yml" "Complete validation suite"
            comp_result=$?

            # 6. Production validation
            run_validation "Production" ".theme-check-production.yml" "Theme Store submission ready"
            prod_result=$?

            # 7. Generate report
            generate_json_report

            # 8. Test presets
            test_presets

            # Summary
            echo ""
            echo -e "${BLUE}📋 Complete Validation Summary${NC}"
            echo "================================"

            if [ $ultimate_result -eq 0 ]; then
                echo -e "${GREEN}✅ Ultimate liquid validation: PASSED${NC}"
            else
                echo -e "${RED}❌ Ultimate liquid validation: FAILED${NC}"
            fi

            if [ $integrity_result -eq 0 ]; then
                echo -e "${GREEN}✅ Schema integrity scan: PASSED${NC}"
            else
                echo -e "${RED}❌ Schema integrity scan: FAILED${NC}"
            fi

            if [ $dev_result -eq 0 ]; then
                echo -e "${GREEN}✅ Development validation: PASSED${NC}"
            else
                echo -e "${RED}❌ Development validation: FAILED${NC}"
            fi

            if [ $comp_result -eq 0 ]; then
                echo -e "${GREEN}✅ Comprehensive validation: PASSED${NC}"
            else
                echo -e "${RED}❌ Comprehensive validation: FAILED${NC}"
            fi

            if [ $prod_result -eq 0 ]; then
                echo -e "${GREEN}✅ Production validation: PASSED${NC}"
                echo -e "${GREEN}🎉 Theme is ready for Theme Store submission!${NC}"
            else
                echo -e "${RED}❌ Production validation: FAILED${NC}"
                echo -e "${RED}🚨 Theme requires fixes before Theme Store submission!${NC}"
            fi
            ;;
        *)
            echo "Usage: $0 [validation_type]"
            echo ""
            echo "Available validation types:"
            echo "  development    - Fast development with ultimate validation"
            echo "  comprehensive  - Complete validation suite"
            echo "  production     - Theme Store ready validation"
            echo "  ultimate       - Ultimate liquid validation (zero tolerance)"
            echo "  integrity      - Deep schema integrity scan"
            echo "  deep          - Ultimate + integrity + comprehensive validation"
            echo "  auto-fix       - Automatically fix correctable issues"
            echo "  report         - Generate detailed JSON report"
            echo "  presets        - Test different validation presets"
            echo "  all           - Complete validation workflow (default)"
            echo ""
            echo "🛡️ RECOMMENDED WORKFLOWS:"
            echo "  $0 development  # Quick dev check with ultimate validation"
            echo "  $0 deep         # Deep validation for pre-deployment"
            echo "  $0 all          # Complete validation for Theme Store"
            echo "  $0 ultimate     # Zero tolerance liquid validation only"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"