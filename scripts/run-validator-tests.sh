#!/bin/bash

# Validator Test Suite Runner
# Runs comprehensive tests for validator accuracy and integration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🧪 Validator Test Suite Runner"
echo "=============================="
echo "Repository: $REPO_ROOT"
echo "Test Date: $(date)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to run a test with error handling
run_test() {
    local test_name=$1
    local test_command=$2

    print_status $BLUE "Running $test_name..."
    echo "Command: $test_command"
    echo "----------------------------------------"

    if eval "$test_command"; then
        print_status $GREEN "✅ $test_name: PASSED"
        return 0
    else
        print_status $RED "❌ $test_name: FAILED"
        return 1
    fi
}

# Check Python availability
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_status $RED "❌ Python not found. Please install Python 3."
        exit 1
    fi

    print_status $GREEN "✅ Python found: $PYTHON_CMD"
}

# Check if validator exists
check_validator() {
    if [[ ! -f "$SCRIPT_DIR/ultimate-validator.py" ]]; then
        print_status $RED "❌ ultimate-validator.py not found in $SCRIPT_DIR"
        exit 1
    fi

    print_status $GREEN "✅ Validator found: $SCRIPT_DIR/ultimate-validator.py"
}

# Check if test files exist
check_test_files() {
    local missing_files=0

    for test_file in "test-validator-accuracy.py" "test-validator-integration.py"; do
        if [[ ! -f "$SCRIPT_DIR/$test_file" ]]; then
            print_status $RED "❌ Test file not found: $test_file"
            missing_files=$((missing_files + 1))
        else
            print_status $GREEN "✅ Test file found: $test_file"
        fi
    done

    if [[ $missing_files -gt 0 ]]; then
        print_status $RED "❌ Missing test files. Cannot proceed."
        exit 1
    fi
}

# Run syntax check on validator
check_validator_syntax() {
    print_status $BLUE "Checking validator syntax..."

    if $PYTHON_CMD -m py_compile "$SCRIPT_DIR/ultimate-validator.py"; then
        print_status $GREEN "✅ Validator syntax is valid"
    else
        print_status $RED "❌ Validator has syntax errors"
        exit 1
    fi
}

# Run accuracy tests
run_accuracy_tests() {
    echo ""
    print_status $BLUE "=========================================="
    print_status $BLUE "RUNNING VALIDATOR ACCURACY TESTS"
    print_status $BLUE "=========================================="

    cd "$SCRIPT_DIR"
    run_test "Validator Accuracy Tests" "$PYTHON_CMD test-validator-accuracy.py"
    return $?
}

# Run integration tests
run_integration_tests() {
    echo ""
    print_status $BLUE "=========================================="
    print_status $BLUE "RUNNING VALIDATOR INTEGRATION TESTS"
    print_status $BLUE "=========================================="

    cd "$SCRIPT_DIR"
    run_test "Validator Integration Tests" "$PYTHON_CMD test-validator-integration.py"
    return $?
}

# Run performance tests
run_performance_tests() {
    echo ""
    print_status $BLUE "=========================================="
    print_status $BLUE "RUNNING VALIDATOR PERFORMANCE TESTS"
    print_status $BLUE "=========================================="

    local code_library="$REPO_ROOT/shopify-liquid-guides/code-library"

    if [[ ! -d "$code_library" ]]; then
        print_status $YELLOW "⚠️  Code library not found. Skipping performance tests."
        return 0
    fi

    print_status $BLUE "Testing validator performance on code library..."

    local start_time=$(date +%s)
    cd "$SCRIPT_DIR"

    if $PYTHON_CMD ultimate-validator.py "$code_library" > /dev/null 2>&1; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))

        if [[ $duration -lt 5 ]]; then
            print_status $GREEN "✅ Performance test: Completed in ${duration}s (Excellent)"
            return 0
        elif [[ $duration -lt 10 ]]; then
            print_status $YELLOW "⚠️  Performance test: Completed in ${duration}s (Good)"
            return 0
        else
            print_status $RED "❌ Performance test: Completed in ${duration}s (Slow)"
            return 1
        fi
    else
        print_status $RED "❌ Performance test: Validator failed on code library"
        return 1
    fi
}

# Generate test report
generate_report() {
    local accuracy_result=$1
    local integration_result=$2
    local performance_result=$3

    echo ""
    print_status $BLUE "=========================================="
    print_status $BLUE "VALIDATOR TEST REPORT"
    print_status $BLUE "=========================================="

    echo "Test Date: $(date)"
    echo "Repository: $REPO_ROOT"
    echo "Validator: $SCRIPT_DIR/ultimate-validator.py"
    echo ""

    echo "Test Results:"
    if [[ $accuracy_result -eq 0 ]]; then
        print_status $GREEN "✅ Accuracy Tests: PASSED"
    else
        print_status $RED "❌ Accuracy Tests: FAILED"
    fi

    if [[ $integration_result -eq 0 ]]; then
        print_status $GREEN "✅ Integration Tests: PASSED"
    else
        print_status $RED "❌ Integration Tests: FAILED"
    fi

    if [[ $performance_result -eq 0 ]]; then
        print_status $GREEN "✅ Performance Tests: PASSED"
    else
        print_status $RED "❌ Performance Tests: FAILED"
    fi

    echo ""

    local total_tests=3
    local passed_tests=0

    [[ $accuracy_result -eq 0 ]] && passed_tests=$((passed_tests + 1))
    [[ $integration_result -eq 0 ]] && passed_tests=$((passed_tests + 1))
    [[ $performance_result -eq 0 ]] && passed_tests=$((passed_tests + 1))

    local success_rate=$((passed_tests * 100 / total_tests))

    echo "Overall Results:"
    echo "- Passed: $passed_tests/$total_tests tests"
    echo "- Success Rate: $success_rate%"

    if [[ $success_rate -eq 100 ]]; then
        print_status $GREEN "🎉 All tests passed! Validator is ready for production."
        return 0
    elif [[ $success_rate -ge 67 ]]; then
        print_status $YELLOW "⚠️  Most tests passed. Minor improvements needed."
        return 1
    else
        print_status $RED "🚨 Many tests failed. Significant improvements needed."
        return 1
    fi
}

# Main execution
main() {
    print_status $BLUE "Starting validator test suite..."

    # Pre-flight checks
    check_python
    check_validator
    check_test_files
    check_validator_syntax

    # Run test suites
    accuracy_result=1
    integration_result=1
    performance_result=1

    run_accuracy_tests && accuracy_result=0
    run_integration_tests && integration_result=0
    run_performance_tests && performance_result=0

    # Generate final report
    generate_report $accuracy_result $integration_result $performance_result
    return $?
}

# Allow running specific test types
case "${1:-all}" in
    "accuracy")
        check_python
        check_validator
        check_test_files
        check_validator_syntax
        run_accuracy_tests
        ;;
    "integration")
        check_python
        check_validator
        check_test_files
        check_validator_syntax
        run_integration_tests
        ;;
    "performance")
        check_python
        check_validator
        run_performance_tests
        ;;
    "all"|"")
        main
        ;;
    *)
        echo "Usage: $0 [accuracy|integration|performance|all]"
        echo ""
        echo "Test Types:"
        echo "  accuracy     - Run validator accuracy tests"
        echo "  integration  - Run Theme Check integration tests"
        echo "  performance  - Run validator performance tests"
        echo "  all          - Run all test suites (default)"
        exit 1
        ;;
esac