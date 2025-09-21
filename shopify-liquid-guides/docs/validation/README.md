# Validation Documentation

This directory contains comprehensive documentation for Shopify theme validation tools and methodologies.

## Files

### `VALIDATOR_ARCHITECTURE_IMPROVEMENTS.md`
**Purpose**: Implementation summary of validator architecture improvements
**Contents**: Detailed documentation of how we enhanced the validator with official Theme Check compatibility
**When to use**: Understanding validator implementation details and architecture decisions

### `SHOPIFY_FILE_TYPE_VALIDATION_MATRIX.md`
**Purpose**: Official validation rules for 100% Theme Store compliance
**Contents**: Comprehensive matrix of validation rules for all 7 Shopify file types
**When to use**: Reference for building validators or understanding validation requirements

## Integration

These validation documents integrate with:
- **Ultimate Validator** (`scripts/ultimate-validator.py`) - Main validation implementation
- **Liquid Syntax Validator** (`scripts/liquid-syntax-validator.py`) - Comprehensive syntax validation
- **Validation Scripts** (`scripts/validate-theme.sh`) - Command-line validation workflows
- **Instructions** (`INSTRUCTIONS.md`) - Step-by-step development workflows

## Usage

Reference these documents when:
1. Building new validation logic
2. Understanding validation architecture
3. Troubleshooting validation issues
4. Ensuring Theme Store compliance
5. Contributing to validator improvements

For complete development workflows, see the main [INSTRUCTIONS.md](../../../INSTRUCTIONS.md).