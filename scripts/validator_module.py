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