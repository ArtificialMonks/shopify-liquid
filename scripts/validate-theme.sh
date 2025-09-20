#!/bin/bash

# Ultimate Theme Validation Script
# Provides comprehensive validation with multiple levels

set -e

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

echo -e "${GREEN}✅ Shopify CLI found: $(shopify version)${NC}"

# Function to run validation with different configurations
run_validation() {
    local config_name=$1
    local config_file=$2
    local description=$3

    echo ""
    echo -e "${BLUE}🔍 Running $config_name Validation${NC}"
    echo "Description: $description"
    echo "Config: $config_file"
    echo "----------------------------------------"

    if shopify theme check --config "$config_file" --output text; then
        echo -e "${GREEN}✅ $config_name validation passed!${NC}"
        return 0
    else
        echo -e "${RED}❌ $config_name validation failed!${NC}"
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

# Main validation workflow
main() {
    case "${1:-all}" in
        "development")
            run_validation "Development" ".theme-check-development.yml" "Fast development validation with essential checks"
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
        "report")
            generate_json_report
            ;;
        "presets")
            test_presets
            ;;
        "all")
            echo "Running complete validation suite..."

            # 1. Development validation
            run_validation "Development" ".theme-check-development.yml" "Fast development validation"
            dev_result=$?

            # 2. Auto-correction
            run_auto_correct

            # 3. Comprehensive validation
            run_validation "Comprehensive" ".theme-check.yml" "Complete validation suite"
            comp_result=$?

            # 4. Production validation
            run_validation "Production" ".theme-check-production.yml" "Theme Store submission ready"
            prod_result=$?

            # 5. Generate report
            generate_json_report

            # 6. Test presets
            test_presets

            # Summary
            echo ""
            echo -e "${BLUE}📋 Validation Summary${NC}"
            echo "================================"

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
                echo -e "${YELLOW}⚠️  Theme needs fixes before Theme Store submission${NC}"
            fi
            ;;
        "help")
            echo "Usage: $0 [OPTION]"
            echo ""
            echo "Options:"
            echo "  development     Run development validation (fast)"
            echo "  production      Run production validation (Theme Store ready)"
            echo "  comprehensive   Run comprehensive validation (all checks)"
            echo "  auto-fix        Run auto-correction"
            echo "  report          Generate JSON validation report"
            echo "  presets         Test Shopify validation presets"
            echo "  all             Run complete validation suite (default)"
            echo "  help            Show this help message"
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

main "$@"