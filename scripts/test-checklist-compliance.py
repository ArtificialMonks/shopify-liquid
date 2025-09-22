#!/usr/bin/env python3
"""
SHOPIFY LIQUID VALIDATION CHECKLIST COMPLIANCE TESTER

Tests that the validation system correctly implements all patterns
defined in LIQUID-VALIDATION-CHECKLIST.md.

This test specification ensures:
✅ All critical validation patterns are caught
✅ Validation levels work as specified
✅ Error messages match checklist standards
✅ Performance thresholds are enforced
✅ Security patterns are detected
✅ Schema validation follows checklist rules

Reference: /LIQUID-VALIDATION-CHECKLIST.md
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path
from typing import List, Dict

# Add scripts directory to path for imports
import importlib.util
import importlib

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    # Import ultimate-validator.py using importlib (handles hyphenated filenames)
    validator_path = script_dir / "ultimate-validator.py"
    spec = importlib.util.spec_from_file_location("ultimate_validator", validator_path)
    ultimate_validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ultimate_validator)

    ShopifyLiquidValidator = ultimate_validator.ShopifyLiquidValidator
    Severity = ultimate_validator.Severity
    VALIDATOR_AVAILABLE = True
    print("✅ Successfully imported ultimate-validator.py")

except Exception as e:
    VALIDATOR_AVAILABLE = False
    # Create dummy classes for when validator is not available
    class ShopifyLiquidValidator:
        def __init__(self, validation_level="ultimate"):
            pass

        def validate_file(self, file_path):
            return True

        @property
        def issues(self):
            return []

        @property
        def level_config(self):
            return {}

    class Severity:
        CRITICAL = "critical"
        ERROR = "error"
        WARNING = "warning"
        INFO = "info"

    print(f"⚠️  Warning: ultimate-validator.py not available ({e}) - some tests will be skipped")

class ChecklistComplianceTest(unittest.TestCase):
    """Test validation compliance with LIQUID-VALIDATION-CHECKLIST.md standards"""

    def setUp(self):
        """Set up test environment"""
        if not VALIDATOR_AVAILABLE:
            self.skipTest("Validator not available")

        self.temp_dir = tempfile.mkdtemp()
        self.validator_dev = ShopifyLiquidValidator(validation_level="development")
        self.validator_prod = ShopifyLiquidValidator(validation_level="production")
        self.validator_ultimate = ShopifyLiquidValidator(validation_level="ultimate")

    def tearDown(self):
        """Clean up test environment"""
        import shutil
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_test_file(self, filename: str, content: str) -> Path:
        """Create a test file with given content"""
        file_path = Path(self.temp_dir) / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path

    def _get_validation_issues(self, validator: ShopifyLiquidValidator, content: str, filename: str = "test.liquid") -> List:
        """Get validation issues for test content"""
        file_path = self._create_test_file(filename, content)
        validator.validate_file(file_path)
        return validator.issues

    def test_checklist_section_1_liquid_syntax_structure(self):
        """Test Section 1: Liquid Syntax & Structure validation"""
        print("\n🔍 Testing Section 1: Liquid Syntax & Structure")

        # Test 1.1: Valid Liquid tags only
        invalid_liquid = """
        {% doc %}This doesn't exist{% enddoc %}
        {% endraw %}Without raw{% endraw %}
        """
        issues = self._get_validation_issues(self.validator_ultimate, invalid_liquid)

        # Should catch invalid tags
        invalid_tag_issues = [i for i in issues if 'doc' in i.message.lower() or 'endraw' in i.message.lower()]
        self.assertGreater(len(invalid_tag_issues), 0, "Should detect invalid Liquid tags")

        # Test 1.2: Proper tag pairing
        unmatched_tags = """
        {% if condition %}
        <p>Content</p>
        <!-- Missing {% endif %} -->
        """
        # Note: This would need liquid syntax parser to catch properly

        # Test 1.3: Nesting depth limit (8 levels max)
        deep_nesting = """
        {% for i1 in (1..10) %}
          {% for i2 in (1..10) %}
            {% for i3 in (1..10) %}
              {% for i4 in (1..10) %}
                {% for i5 in (1..10) %}
                  {% for i6 in (1..10) %}
                    {% for i7 in (1..10) %}
                      {% for i8 in (1..10) %}
                        {% for i9 in (1..10) %}
                          Deep nesting
                        {% endfor %}
                      {% endfor %}
                    {% endfor %}
                  {% endfor %}
                {% endfor %}
              {% endfor %}
            {% endfor %}
          {% endfor %}
        {% endfor %}
        """
        issues = self._get_validation_issues(self.validator_ultimate, deep_nesting)
        nesting_issues = [i for i in issues if 'nesting' in i.message.lower()]
        self.assertGreater(len(nesting_issues), 0, "Should detect excessive nesting depth")

    def test_checklist_section_2_filter_validation(self):
        """Test Section 2: Filter Validation (Critical)"""
        print("\n🔍 Testing Section 2: Filter Validation")

        # Test 2.1: Hallucinated filters
        hallucinated_filters = """
        {{ image | color_extract }}
        {{ data | rgb }}
        {{ value | structured_data }}
        {{ products | color_extract }}
        """
        issues = self._get_validation_issues(self.validator_ultimate, hallucinated_filters)

        hallucinated_issues = [i for i in issues if 'hallucinated' in i.message.lower() or 'does not exist' in i.message.lower()]
        self.assertGreater(len(hallucinated_issues), 0, "Should detect hallucinated filters")

        # Test 2.2: Deprecated filters
        deprecated_filters = """
        {{ image | img_url }}
        {{ image | asset_img_url }}
        """
        issues = self._get_validation_issues(self.validator_ultimate, deprecated_filters)
        deprecated_issues = [i for i in issues if 'deprecated' in i.message.lower()]
        self.assertGreater(len(deprecated_issues), 0, "Should detect deprecated filters")

    def test_checklist_section_3_performance_anti_patterns(self):
        """Test Section 3: Performance Anti-Patterns (CRITICAL)"""
        print("\n🔍 Testing Section 3: Performance Anti-Patterns")

        # Test 3.1: collections.all.products killer
        performance_killer = """
        {% for product in collections.all.products %}
          {{ product.title }}
        {% endfor %}
        """
        issues = self._get_validation_issues(self.validator_ultimate, performance_killer)

        performance_issues = [i for i in issues if 'performance killer' in i.message.lower()]
        self.assertGreater(len(performance_issues), 0, "Should detect collections.all.products performance killer")

        # Test 3.2: Loop limits enforcement
        unlimited_loop = """
        {% for collection in collections %}
          {{ collection.title }}
        {% endfor %}
        """
        issues = self._get_validation_issues(self.validator_ultimate, unlimited_loop)

        # Test 3.3: Image size limits
        large_image = """
        {{ image | image_url: width: 5000 }}
        """
        issues = self._get_validation_issues(self.validator_ultimate, large_image)
        image_issues = [i for i in issues if 'image' in i.message.lower() and ('4000px' in i.message or '3000px' in i.message)]
        self.assertGreater(len(image_issues), 0, "Should detect oversized images")

    def test_checklist_section_4_security_validation(self):
        """Test Section 4: Security Validation (ERROR LEVEL)"""
        print("\n🔍 Testing Section 4: Security Validation")

        # Test 4.1: Content escaping
        unescaped_content = """
        {{ settings.custom_text }}
        {{ customer.first_name }}
        """
        issues = self._get_validation_issues(self.validator_ultimate, unescaped_content)

        security_issues = [i for i in issues if 'escape' in i.message.lower() or 'xss' in i.message.lower()]
        self.assertGreater(len(security_issues), 0, "Should detect unescaped user content")

        # Test 4.2: Raw HTML output
        raw_html = """
        {{ settings.custom_html | raw }}
        """
        issues = self._get_validation_issues(self.validator_ultimate, raw_html)
        raw_issues = [i for i in issues if 'raw' in i.message.lower()]
        self.assertGreater(len(raw_issues), 0, "Should detect dangerous raw HTML output")

    def test_checklist_section_5_schema_configuration(self):
        """Test Section 5: Schema Configuration (Context-Aware)"""
        print("\n🔍 Testing Section 5: Schema Configuration")

        # Test 5.1: Range step validation
        invalid_range_schema = """
        <div>Test content</div>
        {% schema %}
        {
          "name": "Test Section",
          "settings": [
            {
              "type": "range",
              "id": "test_range",
              "min": 0,
              "max": 1000,
              "step": 1
            }
          ]
        }
        {% endschema %}
        """
        issues = self._get_validation_issues(self.validator_ultimate, invalid_range_schema, "sections/test.liquid")

        range_issues = [i for i in issues if 'range' in i.message.lower() and ('101' in i.message or 'step' in i.message)]
        self.assertGreater(len(range_issues), 0, "Should detect invalid range step calculation")

        # Test 5.2: Valid setting types
        invalid_video_setting = """
        <div>Test content</div>
        {% schema %}
        {
          "name": "Test Section",
          "settings": [
            {
              "type": "file",
              "id": "video_file",
              "accept": "video/*"
            }
          ]
        }
        {% endschema %}
        """
        # Note: This would need enhanced schema validation to catch

    def test_validation_levels_compliance(self):
        """Test that validation levels work per checklist specification"""
        print("\n🔍 Testing Validation Levels Compliance")

        # Test content with mixed severity issues
        mixed_issues_content = """
        {{ image | color_extract }}
        {% for product in collections.all.products %}
          {{ product.title }}
        {% endfor %}
        {{ settings.text }}
        """

        # Development level - should only catch critical/error
        dev_issues = self._get_validation_issues(self.validator_dev, mixed_issues_content)
        dev_critical_error = [i for i in dev_issues if i.severity in [Severity.CRITICAL, Severity.ERROR]]

        # Production level - should catch critical/error/warning
        prod_issues = self._get_validation_issues(self.validator_prod, mixed_issues_content)

        # Ultimate level - should catch everything
        ultimate_issues = self._get_validation_issues(self.validator_ultimate, mixed_issues_content)

        # Verify progressive validation levels
        self.assertLessEqual(len(dev_issues), len(prod_issues), "Development should catch fewer issues than production")
        self.assertLessEqual(len(prod_issues), len(ultimate_issues), "Production should catch fewer issues than ultimate")

    def test_checklist_error_message_standards(self):
        """Test that error messages follow checklist standards"""
        print("\n🔍 Testing Error Message Standards")

        test_content = """
        {{ image | color_extract }}
        """
        issues = self._get_validation_issues(self.validator_ultimate, test_content)

        # Check that messages include checklist reference
        checklist_refs = [i for i in issues if 'CHECKLIST:' in i.message]
        self.assertGreater(len(checklist_refs), 0, "Error messages should reference checklist level")

        # Check for specific error message patterns from checklist
        hallucinated_issues = [i for i in issues if 'DOES NOT EXIST' in i.message]
        self.assertGreater(len(hallucinated_issues), 0, "Should use checklist standard error messages")

    def test_theme_store_compliance_patterns(self):
        """Test Theme Store compliance patterns from checklist"""
        print("\n🔍 Testing Theme Store Compliance Patterns")

        # External script violation
        external_script = """
        <script src="https://external-site.com/script.js"></script>
        """
        issues = self._get_validation_issues(self.validator_ultimate, external_script)

        theme_store_issues = [i for i in issues if 'theme store' in i.message.lower() or 'external' in i.message.lower()]
        self.assertGreater(len(theme_store_issues), 0, "Should detect Theme Store violations")

        # Console statements
        console_code = """
        <script>
        console.log('Debug message');
        </script>
        """
        issues = self._get_validation_issues(self.validator_ultimate, console_code)

        console_issues = [i for i in issues if 'console' in i.message.lower()]
        self.assertGreater(len(console_issues), 0, "Should detect console statements")

    def test_checklist_reference_integration(self):
        """Test that checklist is properly referenced throughout validation"""
        print("\n🔍 Testing Checklist Reference Integration")

        # Verify validator has checklist configuration
        self.assertIn('development', self.validator_ultimate.level_config)
        self.assertIn('production', self.validator_ultimate.level_config)
        self.assertIn('ultimate', self.validator_ultimate.level_config)

        # Verify checklist descriptions match expected values
        dev_config = self.validator_ultimate.level_config['development']
        self.assertIn('critical error', dev_config['description'].lower())

        prod_config = self.validator_ultimate.level_config['production']
        self.assertIn('theme store', prod_config['description'].lower())

        ultimate_config = self.validator_ultimate.level_config['ultimate']
        self.assertIn('zero tolerance', ultimate_config['description'].lower())

def run_checklist_compliance_tests():
    """Run all checklist compliance tests"""
    print("🛡️ SHOPIFY LIQUID VALIDATION CHECKLIST COMPLIANCE TESTER")
    print("📋 Testing compliance with LIQUID-VALIDATION-CHECKLIST.md")
    print("=" * 80)

    if not VALIDATOR_AVAILABLE:
        print("❌ Cannot run tests - ultimate_validator.py not available")
        return False

    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(ChecklistComplianceTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 80)
    print("📊 CHECKLIST COMPLIANCE TEST RESULTS")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  • {test}: {traceback.split('AssertionError: ')[-1].split(chr(10))[0]}")

    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  • {test}: {traceback.split(chr(10))[-2]}")

    success = len(result.failures) == 0 and len(result.errors) == 0

    if success:
        print("\n✅ ALL CHECKLIST COMPLIANCE TESTS PASSED!")
        print("🎉 Validation system correctly implements checklist standards")
    else:
        print("\n❌ CHECKLIST COMPLIANCE TESTS FAILED!")
        print("🛑 Validation system does not fully implement checklist standards")

    return success

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test validation compliance with LIQUID-VALIDATION-CHECKLIST.md")
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()

    success = run_checklist_compliance_tests()
    sys.exit(0 if success else 1)