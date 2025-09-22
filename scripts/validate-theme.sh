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

# Internal: run a command with timeout (works without GNU timeout)
run_with_timeout() {
    local seconds="$1"; shift
    # Start the command in a new process group so we can kill the whole tree
    setsid "$@" &
    local pid=$!
    local start=$(date +%s)
    while kill -0 "$pid" 2>/dev/null; do
        local now=$(date +%s)
        if (( now - start > seconds )); then
            echo -e "${YELLOW}⏰ Timeout after ${seconds}s; killing PID ${pid} (process group)${NC}"
            # Kill the entire process group
            kill -TERM -"$pid" 2>/dev/null || true
            pkill -TERM -P "$pid" 2>/dev/null || true
            sleep 1
            kill -KILL -"$pid" 2>/dev/null || true
            pkill -KILL -P "$pid" 2>/dev/null || true
            wait "$pid" 2>/dev/null
            return 124
        fi
        sleep 1
    done
    wait "$pid"
    return $?
}

# Per-file Theme Check with timeout and logging
run_theme_check_per_file() {
    local config="$1"
    local target_dir="${VALIDATION_TARGET_DIR:-shopify-liquid-guides/code-library}"
    local timeout_secs="${PER_FILE_TIMEOUT_SECS:-60}"

    echo ""
    echo -e "${BLUE}🧪 Per-file Validation (timeout ${timeout_secs}s)${NC}"
    local -a files
    mapfile -t files < <(find "$target_dir" -type f -name "*.liquid" | sort)
    local total="${#files[@]}"

    # Counters
    local c_theme_pass=0 c_theme_fail=0 c_theme_timeout=0
    local c_syntax_ok=0 c_syntax_fail=0 c_skipped=0

    local i=0
    for f in "${files[@]}"; do
        i=$((i+1))
        echo -e "${BLUE}[${i}/${total}]${NC} Checking: ${f}"

        # Determine strategy by path
        if [[ "$f" == *"/sections/"* || "$f" == *"/templates/"* ]]; then
            # Theme Check supported targets
            if run_with_timeout "$timeout_secs" shopify theme check --config "$config" "$f" --fail-level error; then
                echo -e "${GREEN}✔ ThemeCheck Pass: ${f}${NC}"; c_theme_pass=$((c_theme_pass+1))
            else
                status=$?
                if [ $status -eq 124 ]; then
                    echo -e "${RED}❌ ThemeCheck Timeout: ${f}${NC}"; echo "file_timeout: ${f}" >> theme-check-timeouts.log; c_theme_timeout=$((c_theme_timeout+1))
                else
                    echo -e "${YELLOW}⚠ ThemeCheck Fail (${status}): ${f}${NC}"; c_theme_fail=$((c_theme_fail+1))
                fi
            fi
        else
            # Blocks/snippets/assets: use Python validator (fast/standard)
            if run_with_timeout "$timeout_secs" python3 "${SCRIPT_DIR}/liquid-syntax-validator.py" --level standard "$f"; then
                echo -e "${GREEN}✔ Syntax OK: ${f}${NC}"; c_syntax_ok=$((c_syntax_ok+1))
            else
                status=$?
                if [ $status -eq 124 ]; then
                    echo -e "${RED}❌ Syntax Timeout: ${f}${NC}"; echo "syntax_timeout: ${f}" >> liquid-syntax-timeouts.log; c_theme_timeout=$((c_theme_timeout+1))
                else
                    echo -e "${RED}❌ Syntax Fail (${status}): ${f}${NC}"; c_syntax_fail=$((c_syntax_fail+1))
                fi
            fi
        fi
    done

    echo ""
    echo -e "${BLUE}📊 Per-file Validation Summary${NC}"
    echo "ThemeCheck: pass=$c_theme_pass fail=$c_theme_fail timeout=$c_theme_timeout"
    echo "Syntax:     ok=$c_syntax_ok fail=$c_syntax_fail"
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

    # Use current directory for ultimate validation unless explicitly targeting all
    local ultimate_target="${VALIDATION_TARGET_DIR:-$(pwd)}"

    # Run the validator and show progress (with a global timeout per file in the Python script not guaranteed)
    if python3 "${SCRIPT_DIR}/ultimate-validator.py" "$ultimate_target"; then
        echo -e "${GREEN}✅ Ultimate validation passed!${NC}"
        return 0
    else
        echo -e "${RED}❌ Ultimate validation failed!${NC}"
        return 1
    fi
}

# Function to run comprehensive schema integrity scan
run_schema_integrity_scan() {
    echo ""
    echo -e "${YELLOW}🔍 Running Schema Integrity Scan${NC}"
    echo "Deep validation of schema consistency and preset integrity..."
    echo "----------------------------------------"

    # Use target directory if specified, otherwise use --all flag
    local integrity_target="${VALIDATION_TARGET_DIR:-}"

    if [[ -n "$integrity_target" ]]; then
        # Target specific directory
        if python3 "${SCRIPT_DIR}/scan-schema-integrity.py" "$integrity_target"; then
            echo -e "${GREEN}✅ Schema integrity scan passed!${NC}"
            return 0
        else
            echo -e "${RED}❌ Schema integrity scan failed!${NC}"
            return 1
        fi
    else
        # Use --all flag for full scan
        if python3 "${SCRIPT_DIR}/scan-schema-integrity.py" --all; then
            echo -e "${GREEN}✅ Schema integrity scan passed!${NC}"
            return 0
        else
            echo -e "${RED}❌ Schema integrity scan failed!${NC}"
            return 1
        fi
    fi
}

# Function to run comprehensive Liquid syntax validation (per-file with timeout)
run_liquid_syntax_validation() {
    echo ""
    echo -e "${YELLOW}🔤 Running Comprehensive Liquid Syntax Validation${NC}"
    echo "Advanced parser-based syntax checking for all Liquid files (per-file timeout)..."
    echo "----------------------------------------"

    local target_dir="${VALIDATION_TARGET_DIR:-$(pwd)}"
    local timeout_secs="${PER_FILE_TIMEOUT_SECS:-60}"

    mapfile -t files < <(find "${target_dir}" -type f -name "*.liquid" | sort)
    local total="${#files[@]}"
    local i=0
    local any_fail=0
    for f in "${files[@]}"; do
        i=$((i+1))
        echo -e "${BLUE}[${i}/${total}]${NC} Syntax check: ${f}"
        if run_with_timeout "$timeout_secs" python3 "${SCRIPT_DIR}/liquid-syntax-validator.py" --level comprehensive "$f"; then
            echo -e "${GREEN}✔ Syntax OK: ${f}${NC}"
        else
            status=$?
            any_fail=1
            if [ $status -eq 124 ]; then
                echo -e "${RED}✖ Syntax Timeout: ${f}${NC}"
                echo "syntax_timeout: ${f}" >> liquid-syntax-timeouts.log
            else
                echo -e "${YELLOW}⚠ Syntax Fail (${status}): ${f}${NC}"
            fi
        fi
    done

    if [ $any_fail -eq 0 ]; then
        echo -e "${GREEN}✅ Liquid syntax validation passed!${NC}"
        return 0
    else
        echo -e "${RED}❌ Liquid syntax validation had failures/timeouts.${NC}"
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
    # Parse arguments for directory support
    local validation_type="${1:-all}"
    local target_directory=""

    # Check if second argument is a directory path
    if [[ -n "$2" && -d "$2" ]]; then
        target_directory="$2"
        # Convert to absolute path if needed
        if [[ ! "$target_directory" = /* ]]; then
            target_directory="$(pwd)/$target_directory"
        fi
        export VALIDATION_TARGET_DIR="$target_directory"
        echo -e "${BLUE}🎯 Target Directory: $target_directory${NC}"
        # Don't change directory, just use the absolute path
    elif [[ -n "$2" ]]; then
        echo -e "${RED}❌ Invalid directory: $2${NC}"
        echo "Please provide a valid directory path as the second argument."
        exit 1
    fi

    case "$validation_type" in
        "development")
            echo "Running development validation per LIQUID-VALIDATION-CHECKLIST.md..."
            echo "📋 Level: Development (Fast feedback with critical error detection)"

            # 1. Ultimate liquid validation with development level
            echo -e "${BLUE}🔍 Running development-level validation...${NC}"
            if python3 "${SCRIPT_DIR}/ultimate-validator.py" --level development "$ultimate_target"; then
                echo -e "${GREEN}✅ Development validation passed!${NC}"
                ultimate_result=0
            else
                echo -e "${RED}❌ Development validation failed!${NC}"
                ultimate_result=1
            fi

            # 2. Per-file Theme Check with timeout to avoid hangs
            run_theme_check_per_file ".theme-check-development.yml"

            # 3. Basic development validation
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
            echo "Running production validation per LIQUID-VALIDATION-CHECKLIST.md..."
            echo "📋 Level: Production (Theme Store compliance validation)"

            # 1. Ultimate liquid validation with production level
            echo -e "${BLUE}🔍 Running production-level validation...${NC}"
            if python3 "${SCRIPT_DIR}/ultimate-validator.py" --level production "$ultimate_target"; then
                echo -e "${GREEN}✅ Production validation passed!${NC}"
                prod_result=0
            else
                echo -e "${RED}❌ Production validation failed!${NC}"
                prod_result=1
            fi

            # 2. Per-file Theme Check first to avoid hangs
            run_theme_check_per_file ".theme-check-production.yml"

            # 3. Standard Theme Check validation
            run_validation "Production" ".theme-check-production.yml" "Theme Store submission validation"
            theme_check_result=$?

            # Summary for production mode
            echo ""
            echo -e "${BLUE}📋 Production Validation Summary${NC}"
            echo "================================"

            if [ $prod_result -eq 0 ]; then
                echo -e "${GREEN}✅ Checklist compliance: PASSED${NC}"
            else
                echo -e "${RED}❌ Checklist compliance: FAILED${NC}"
            fi

            if [ $theme_check_result -eq 0 ]; then
                echo -e "${GREEN}✅ Theme Check: PASSED${NC}"
            else
                echo -e "${RED}❌ Theme Check: FAILED${NC}"
            fi

            if [ $prod_result -eq 0 ] && [ $theme_check_result -eq 0 ]; then
                echo -e "${GREEN}🎉 Production validation passed - Theme Store ready!${NC}"
                exit 0
            else
                echo -e "${RED}🚨 Production validation failed!${NC}"
                exit 1
            fi
            ;;
        "comprehensive")
            run_validation "Comprehensive" ".theme-check.yml" "Complete validation with all available checks"
            ;;
        "auto-fix")
            run_auto_correct
            ;;
        "ultimate")
            echo "Running ultimate validation per LIQUID-VALIDATION-CHECKLIST.md..."
            echo "📋 Level: Ultimate (Zero tolerance comprehensive validation)"

            # Ultimate liquid validation with ultimate level
            echo -e "${BLUE}🔍 Running ultimate-level validation...${NC}"
            if python3 "${SCRIPT_DIR}/ultimate-validator.py" --level ultimate "$ultimate_target"; then
                echo -e "${GREEN}✅ Ultimate validation passed!${NC}"
                echo -e "${GREEN}🎉 Code is production-ready with zero tolerance compliance!${NC}"
                exit 0
            else
                echo -e "${RED}❌ Ultimate validation failed!${NC}"
                echo -e "${RED}🛑 Fix ALL issues before deployment - zero tolerance policy${NC}"
                exit 1
            fi
            ;;
        "integrity")
            run_schema_integrity_scan
            ;;
        "syntax")
            run_liquid_syntax_validation
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

            # 3. Liquid syntax validation (comprehensive parser-based)
            run_liquid_syntax_validation
            liquid_result=$?

            # 4. Comprehensive validation (theme-check)
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

            if [ $liquid_result -eq 0 ]; then
                echo -e "${GREEN}✅ Liquid syntax validation: PASSED${NC}"
            else
                echo -e "${RED}❌ Liquid syntax validation: FAILED${NC}"
            fi

            if [ $comp_result -eq 0 ]; then
                echo -e "${GREEN}✅ Comprehensive validation: PASSED${NC}"
            else
                echo -e "${RED}❌ Comprehensive validation: FAILED${NC}"
            fi

            if [ $ultimate_result -eq 0 ] && [ $integrity_result -eq 0 ] && [ $liquid_result -eq 0 ] && [ $comp_result -eq 0 ]; then
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

            # 4. Liquid syntax validation (comprehensive parser-based)
            run_liquid_syntax_validation
            liquid_result=$?

            # 5. Per-file Theme Check (development) with timeout
            run_theme_check_per_file ".theme-check-development.yml"

            # 6. Development validation
            run_validation "Development" ".theme-check-development.yml" "Fast development validation"
            dev_result=$?

            # 7. Comprehensive validation
            run_validation "Comprehensive" ".theme-check.yml" "Complete validation suite"
            comp_result=$?

            # 8. Per-file Theme Check (production) with timeout
            run_theme_check_per_file ".theme-check-production.yml"

            # 9. Production validation
            run_validation "Production" ".theme-check-production.yml" "Theme Store submission ready"
            prod_result=$?

            # 8. Generate report
            generate_json_report

            # 9. Test presets
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

            if [ $liquid_result -eq 0 ]; then
                echo -e "${GREEN}✅ Liquid syntax validation: PASSED${NC}"
            else
                echo -e "${RED}❌ Liquid syntax validation: FAILED${NC}"
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
            echo "Usage: $0 [validation_type] [target_directory]"
            echo ""
            echo "Arguments:"
            echo "  validation_type    - Type of validation to run (default: all)"
            echo "  target_directory   - Directory to validate (default: current directory)"
            echo ""
            echo "Available validation types (per LIQUID-VALIDATION-CHECKLIST.md):"
            echo "  development    - Fast feedback with critical error detection"
            echo "  production     - Theme Store compliance validation"
            echo "  ultimate       - Zero tolerance comprehensive validation"
            echo "  comprehensive  - Complete Theme Check validation suite"
            echo "  integrity      - Deep schema integrity scan"
            echo "  syntax         - Comprehensive Liquid syntax validation"
            echo "  deep          - Ultimate + integrity + syntax + comprehensive validation"
            echo "  auto-fix       - Automatically fix correctable issues"
            echo "  report         - Generate detailed JSON report"
            echo "  presets        - Test different validation presets"
            echo "  all           - Complete validation workflow (default)"
            echo ""
            echo "🛡️ RECOMMENDED WORKFLOWS (LIQUID-VALIDATION-CHECKLIST.md):"
            echo "  $0 development                    # Fast feedback (critical errors only)"
            echo "  $0 production /path/to/theme     # Theme Store ready validation"
            echo "  $0 ultimate                      # Zero tolerance (all issues)"
            echo "  $0 deep /path/to/theme           # Comprehensive validation suite"
            echo ""
            echo "Examples:"
            echo "  $0 all                           # Validate current directory"
            echo "  $0 development ./my-theme        # Validate ./my-theme directory"
            echo "  $0 ultimate ../other-theme       # Ultimate validation on ../other-theme"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"