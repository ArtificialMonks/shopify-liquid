#!/bin/bash

# ==============================================================================
# Robust Timeout Test Runner with Investigation Warnings
# ==============================================================================
#
# Implements proper timeout handling with:
# - 30s warning with investigation
# - 60s hard termination
# - Process monitoring and analysis
# - Performance bottleneck identification
#
# Usage: ./scripts/test-with-timeout.sh <validation_command> [args...]
# ==============================================================================

set -e

# Configuration
WARN_TIMEOUT=30
KILL_TIMEOUT=60
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to get current timestamp
timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

# Function to log with timestamp
log() {
    echo -e "[$(timestamp)] $1"
}

# Function to investigate stuck process
investigate_process() {
    local pid=$1
    log "${YELLOW}🔍 INVESTIGATING STUCK PROCESS (PID: $pid)${NC}"

    # Check if process is still running
    if ! kill -0 $pid 2>/dev/null; then
        log "${GREEN}✅ Process completed during investigation${NC}"
        return 0
    fi

    # Get process info
    log "${BLUE}📊 Process Information:${NC}"
    ps -p $pid -o pid,ppid,cmd,pcpu,pmem,time 2>/dev/null || echo "  Process info unavailable"

    # Check open files
    log "${BLUE}📁 Open Files (last 10):${NC}"
    lsof -p $pid 2>/dev/null | tail -10 || echo "  File info unavailable"

    # Check what the process is doing
    log "${BLUE}🔍 Process Activity:${NC}"
    if command -v strace >/dev/null 2>&1; then
        timeout 3s strace -p $pid 2>&1 | head -5 || echo "  System call trace unavailable"
    else
        echo "  strace not available for detailed analysis"
    fi

    # Memory usage
    log "${BLUE}💾 Memory Usage:${NC}"
    ps -p $pid -o rss,vsz 2>/dev/null | tail -1 | awk '{printf "  RSS: %d KB, VSZ: %d KB\n", $1, $2}' || echo "  Memory info unavailable"

    return 1
}

# Function to run command with timeout monitoring
run_with_timeout() {
    local cmd="$*"
    log "${BLUE}🚀 Starting: $cmd${NC}"
    log "${BLUE}⏰ Timeout config: ${WARN_TIMEOUT}s warning, ${KILL_TIMEOUT}s termination${NC}"

    # Start the command in background
    $cmd &
    local pid=$!
    local start_time=$(date +%s)

    log "${GREEN}✅ Process started with PID: $pid${NC}"

    # Monitor the process
    local elapsed=0
    local warned=false

    while kill -0 $pid 2>/dev/null; do
        sleep 1
        elapsed=$(($(date +%s) - start_time))

        # 30 second warning
        if [ $elapsed -ge $WARN_TIMEOUT ] && [ "$warned" = false ]; then
            log "${YELLOW}⚠️  WARNING: Process running for ${elapsed}s (>${WARN_TIMEOUT}s)${NC}"
            log "${YELLOW}🔍 Initiating investigation...${NC}"

            if investigate_process $pid; then
                log "${GREEN}✅ Process completed during investigation after ${elapsed}s${NC}"
                wait $pid
                return $?
            fi

            log "${YELLOW}⚠️  Process still running after investigation${NC}"
            log "${YELLOW}📊 Performance analysis: Likely stuck on file processing${NC}"
            log "${YELLOW}💡 Possible issues:${NC}"
            log "${YELLOW}   - Large file processing${NC}"
            log "${YELLOW}   - Infinite loop in validation logic${NC}"
            log "${YELLOW}   - I/O blocking operation${NC}"
            log "${YELLOW}   - Memory allocation issues${NC}"
            warned=true
        fi

        # 60 second hard termination
        if [ $elapsed -ge $KILL_TIMEOUT ]; then
            log "${RED}🛑 HARD TIMEOUT: Terminating process after ${elapsed}s${NC}"

            # Try graceful termination first
            log "${YELLOW}🔄 Attempting graceful termination...${NC}"
            kill -TERM $pid 2>/dev/null
            sleep 3

            # Force kill if still running
            if kill -0 $pid 2>/dev/null; then
                log "${RED}💀 Force killing process...${NC}"
                kill -KILL $pid 2>/dev/null
                sleep 1
            fi

            # Final check
            if kill -0 $pid 2>/dev/null; then
                log "${RED}❌ Failed to terminate process${NC}"
                return 1
            else
                log "${YELLOW}✅ Process terminated successfully${NC}"
                return 124  # Timeout exit code
            fi
        fi
    done

    # Process completed normally
    wait $pid
    local exit_code=$?
    elapsed=$(($(date +%s) - start_time))

    if [ $exit_code -eq 0 ]; then
        log "${GREEN}✅ Process completed successfully in ${elapsed}s${NC}"
    else
        log "${RED}❌ Process failed with exit code $exit_code after ${elapsed}s${NC}"
    fi

    return $exit_code
}

# Function to analyze validation performance
analyze_validation_performance() {
    log "${BLUE}📊 VALIDATION PERFORMANCE ANALYSIS${NC}"
    log "${BLUE}=====================================${NC}"

    # Count files by type
    log "${BLUE}📁 File Analysis:${NC}"
    find . -name "*.liquid" | wc -l | xargs printf "  Total .liquid files: %d\n"
    find . -name "*.liquid" -path "*/sections/*" | wc -l | xargs printf "  Section files: %d\n"
    find . -name "*.liquid" -path "*/blocks/*" | wc -l | xargs printf "  Block files: %d\n"
    find . -name "*.liquid" -path "*/snippets/*" | wc -l | xargs printf "  Snippet files: %d\n"

    # Find large files
    log "${BLUE}📈 Large Files (>10KB):${NC}"
    find . -name "*.liquid" -size +10k -exec ls -lh {} \; | awk '{print "  " $9 " (" $5 ")"}' | head -5

    # Check for complex patterns that might cause slowdowns
    log "${BLUE}🔍 Complexity Indicators:${NC}"
    complex_files=$(find . -name "*.liquid" -exec grep -l "{% for.*{% for" {} \; | wc -l)
    printf "  Files with nested loops: %d\n" $complex_files

    large_schema_files=$(find . -name "*.liquid" -exec grep -l "{% schema %}" {} \; -exec wc -c {} \; | awk 'NR%2==0 && $1>5000 {print prev} {prev=$2}' | wc -l)
    printf "  Large files with schemas: %d\n" $large_schema_files
}

# Main execution
main() {
    if [ $# -eq 0 ]; then
        echo "Usage: $0 <validation_command> [args...]"
        echo ""
        echo "Examples:"
        echo "  $0 ./scripts/validate-theme.sh development ."
        echo "  $0 python3 scripts/ultimate-validator.py --level development ."
        echo ""
        exit 1
    fi

    log "${BLUE}🛡️ ROBUST TIMEOUT TEST RUNNER${NC}"
    log "${BLUE}==============================${NC}"

    # Pre-flight analysis
    analyze_validation_performance
    echo ""

    # Run the command with timeout monitoring
    run_with_timeout "$@"
    local result=$?

    # Post-execution analysis
    echo ""
    log "${BLUE}📋 EXECUTION SUMMARY${NC}"
    log "${BLUE}====================${NC}"

    case $result in
        0)
            log "${GREEN}✅ SUCCESS: Validation completed successfully${NC}"
            ;;
        124)
            log "${RED}⏰ TIMEOUT: Validation exceeded ${KILL_TIMEOUT}s limit${NC}"
            log "${YELLOW}💡 Recommendations:${NC}"
            log "${YELLOW}   1. Use more specific file targeting${NC}"
            log "${YELLOW}   2. Implement per-file timeout limits${NC}"
            log "${YELLOW}   3. Optimize validation algorithms${NC}"
            log "${YELLOW}   4. Process files in smaller batches${NC}"
            ;;
        *)
            log "${RED}❌ FAILURE: Validation failed with exit code $result${NC}"
            ;;
    esac

    return $result
}

# Execute main function with all arguments
main "$@"