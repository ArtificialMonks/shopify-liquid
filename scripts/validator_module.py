#!/usr/bin/env python3
"""
Import wrapper for ultimate-validator.py
Allows importing the validator classes from the hyphenated filename
"""

import importlib.util
import sys
from pathlib import Path

# Load the ultimate-validator.py module
script_dir = Path(__file__).parent
validator_path = script_dir / "ultimate-validator.py"

if not validator_path.exists():
    raise ImportError("ultimate-validator.py not found in scripts directory")

spec = importlib.util.spec_from_file_location("ultimate_validator", validator_path)
ultimate_validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ultimate_validator)

# Export the classes for import
UltimateShopifyValidator = ultimate_validator.ShopifyLiquidValidator  # Use actual class name
Severity = ultimate_validator.Severity
ValidationIssue = ultimate_validator.ValidationIssue

# Helper function for importing hyphenated modules
def import_hyphenated_module(filename, module_name=None):
    """
    Helper function to import Python modules with hyphenated filenames.

    Args:
        filename: The hyphenated filename (e.g., "liquid-syntax-validator.py")
        module_name: Optional module name for import (auto-generated if not provided)

    Returns:
        The imported module

    Example:
        liquid_validator = import_hyphenated_module("liquid-syntax-validator.py")
        validator = liquid_validator.ShopifyLiquidSyntaxValidator()
    """
    script_dir = Path(__file__).parent
    module_path = script_dir / filename

    if not module_path.exists():
        raise ImportError(f"{filename} not found in scripts directory")

    if module_name is None:
        # Convert hyphenated filename to module name
        module_name = filename.replace('-', '_').replace('.py', '')

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module