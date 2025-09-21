#!/usr/bin/env python3
"""
Validator Accuracy Test Suite
Tests specific validation scenarios to ensure our validator catches all issues correctly
"""

import sys
import os
from pathlib import Path
import tempfile
import shutil
import json

# Add the scripts directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from validator_module import UltimateShopifyValidator, Severity
except ImportError:
    print("ERROR: Could not import validator classes")
    print("Make sure ultimate-validator.py is in the same directory as this test file")
    sys.exit(1)

class ValidatorAccuracyTest:
    """Test suite for validator accuracy"""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.test_cases = []

    def create_test_file(self, filename: str, content: str) -> Path:
        """Create a temporary test file"""
        test_dir = Path(tempfile.mkdtemp(prefix="validator_test_"))
        file_path = test_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return file_path

    def run_validator_on_content(self, filename: str, content: str) -> list:
        """Run validator on test content and return issues"""
        test_file = self.create_test_file(filename, content)
        validator = UltimateShopifyValidator()

        try:
            validator.validate_file(test_file)
            return validator.issues
        finally:
            shutil.rmtree(test_file.parent)

    def test_case(self, name: str, filename: str, content: str, expected_issues: list, should_have_issues: bool = True):
        """Run a single test case"""
        print(f"\n🧪 {name}")
        print("-" * 50)

        issues = self.run_validator_on_content(filename, content)

        # Check if we got the expected number of issues
        actual_count = len(issues)
        expected_count = len(expected_issues)

        if should_have_issues:
            if actual_count == 0 and expected_count > 0:
                print(f"❌ Expected {expected_count} issues, but found none")
                self.failed += 1
                return False

            # Check for expected issue types
            found_expected = []
            for expected in expected_issues:
                found = False
                for issue in issues:
                    if expected.lower() in issue.message.lower():
                        found = True
                        break
                found_expected.append(found)

            if all(found_expected):
                print(f"✅ Found all {expected_count} expected issues")
                for i, issue in enumerate(issues):
                    print(f"   {i+1}. {issue.severity.value}: {issue.message}")
                self.passed += 1
                return True
            else:
                print(f"❌ Missing expected issues")
                print(f"Expected: {expected_issues}")
                print(f"Found: {[issue.message for issue in issues]}")
                self.failed += 1
                return False
        else:
            if actual_count == 0:
                print(f"✅ Correctly found no issues")
                self.passed += 1
                return True
            else:
                print(f"❌ Found unexpected issues:")
                for issue in issues:
                    print(f"   - {issue.severity.value}: {issue.message}")
                self.failed += 1
                return False

    def test_file_type_detection(self):
        """Test file type detection accuracy"""
        print("\n" + "=" * 60)
        print("FILE TYPE DETECTION TESTS")
        print("=" * 60)

        # Layout file should have content_for_header
        self.test_case(
            "Layout File - Missing Required Objects",
            "layout/theme.liquid",
            """<!DOCTYPE html>
<html>
<head><title>{{ page_title }}</title></head>
<body>{{ content_for_layout }}</body>
</html>""",
            ["Layout missing required object: content_for_header"],
            should_have_issues=True
        )

        # Snippet should not require schema
        self.test_case(
            "Snippet File - No Schema Required",
            "snippets/product-card.liquid",
            """<div class="product-card">
  <h3>{{ product.title | escape }}</h3>
  <p>{{ product.price | money }}</p>
</div>""",
            [],
            should_have_issues=False
        )

        # Section should require schema
        self.test_case(
            "Section File - Schema Required",
            "sections/hero.liquid",
            """<div class="hero">
  <h1>{{ section.settings.heading | escape }}</h1>
</div>""",
            ["Section requires schema block"],
            should_have_issues=True
        )

    def test_schema_validation(self):
        """Test schema validation rules"""
        print("\n" + "=" * 60)
        print("SCHEMA VALIDATION TESTS")
        print("=" * 60)

        # Invalid range step - (max-min)/step > 101
        self.test_case(
            "Invalid Range Step Validation",
            "sections/invalid-range.liquid",
            """<div>Content</div>

{% schema %}
{
  "name": "Invalid Range",
  "settings": [
    {
      "type": "range",
      "id": "count",
      "min": 1,
      "max": 1000,
      "step": 1,
      "default": 50
    }
  ]
}
{% endschema %}""",
            ["Range setting 'count' violates (max-min)/step <= 101"],
            should_have_issues=True
        )

        # Valid range step
        self.test_case(
            "Valid Range Step",
            "sections/valid-range.liquid",
            """<div>Content</div>

{% schema %}
{
  "name": "Valid Range",
  "settings": [
    {
      "type": "range",
      "id": "count",
      "min": 1,
      "max": 100,
      "step": 1,
      "default": 50
    }
  ]
}
{% endschema %}""",
            [],
            should_have_issues=False
        )

    def test_app_block_validation(self):
        """Test @app block validation"""
        print("\n" + "=" * 60)
        print("APP BLOCK VALIDATION TESTS")
        print("=" * 60)

        # @app block with limit (invalid)
        self.test_case(
            "@app Block with Limit (Invalid)",
            "sections/app-with-limit.liquid",
            """<div class="app-wrapper">
  {% for block in section.blocks %}
    {% render block %}
  {% endfor %}
</div>

{% schema %}
{
  "name": "App Section",
  "blocks": [
    {
      "type": "@app",
      "limit": 5
    }
  ]
}
{% endschema %}""",
            ["@app blocks cannot have 'limit' parameter"],
            should_have_issues=True
        )

        # @app block without limit (valid)
        self.test_case(
            "@app Block without Limit (Valid)",
            "sections/app-valid.liquid",
            """<div class="app-wrapper">
  {% for block in section.blocks %}
    {% render block %}
  {% endfor %}
</div>

{% schema %}
{
  "name": "App Section",
  "blocks": [
    {
      "type": "@app"
    }
  ]
}
{% endschema %}""",
            [],
            should_have_issues=False
        )

    def test_static_block_ids(self):
        """Test static block ID uniqueness (note: validator checks across files, not within single file)"""
        print("\n" + "=" * 60)
        print("STATIC BLOCK ID TESTS")
        print("=" * 60)

        # Single file with valid blocks (duplicate ID validation requires multiple files)
        self.test_case(
            "Valid Block IDs in Single Section",
            "sections/valid-blocks.liquid",
            """<div>
  {% for block in section.blocks %}
    {% case block.type %}
      {% when 'text' %}
        <p>{{ block.settings.content }}</p>
    {% endcase %}
  {% endfor %}
</div>

{% schema %}
{
  "name": "Section with Valid Block IDs",
  "blocks": [
    {
      "type": "text",
      "name": "Text Block 1",
      "id": "text_block_1",
      "settings": [
        {
          "type": "text",
          "id": "content",
          "label": "Content"
        }
      ]
    },
    {
      "type": "text",
      "name": "Text Block 2",
      "id": "text_block_2",
      "settings": [
        {
          "type": "text",
          "id": "content2",
          "label": "Content 2"
        }
      ]
    }
  ]
}
{% endschema %}""",
            [],
            should_have_issues=False
        )

    def test_liquid_validation(self):
        """Test Liquid validation (filters, patterns, etc.)"""
        print("\n" + "=" * 60)
        print("LIQUID VALIDATION TESTS")
        print("=" * 60)

        # Test for deprecated filters
        self.test_case(
            "Deprecated Filter Usage",
            "sections/deprecated-filter.liquid",
            """<div>
  {% if product.featured_image %}
    <img src="{{ product.featured_image | img_url: '300x300' }}" alt="{{ product.title }}">
  {% endif %}
</div>

{% schema %}
{
  "name": "Section with Deprecated Filter"
}
{% endschema %}""",
            ["Deprecated filter: | img_url"],
            should_have_issues=True
        )

        # Valid modern syntax
        self.test_case(
            "Valid Modern Liquid",
            "sections/valid-liquid.liquid",
            """<div>
  {% for product in collections.all.products limit: 4 %}
    <h3>{{ product.title | escape }}</h3>
    <p>{{ product.price | money }}</p>
  {% endfor %}
</div>

{% schema %}
{
  "name": "Valid Modern Section"
}
{% endschema %}""",
            [],
            should_have_issues=False
        )

    def test_performance_validation(self):
        """Test performance-related validation"""
        print("\n" + "=" * 60)
        print("PERFORMANCE VALIDATION TESTS")
        print("=" * 60)

        # Excessive nesting
        self.test_case(
            "Excessive Block Nesting",
            "sections/deep-nesting.liquid",
            """<div>
  {% for i in (1..10) %}
    {% for j in (1..10) %}
      {% for k in (1..10) %}
        {% for l in (1..10) %}
          {% for m in (1..10) %}
            {% for n in (1..10) %}
              {% for o in (1..10) %}
                {% for p in (1..10) %}
                  {% for q in (1..10) %}
                    <span>Deep nesting</span>
                  {% endfor %}
                {% endfor %}
              {% endfor %}
            {% endfor %}
          {% endfor %}
        {% endfor %}
      {% endfor %}
    {% endfor %}
  {% endfor %}
</div>

{% schema %}
{
  "name": "Deep Nesting Section"
}
{% endschema %}""",
            ["nesting depth", "exceeds"],
            should_have_issues=True
        )

    def test_template_restrictions(self):
        """Test template restriction validation"""
        print("\n" + "=" * 60)
        print("TEMPLATE RESTRICTION TESTS")
        print("=" * 60)

        # Section with template restrictions (should generate warning)
        self.test_case(
            "Section with Template Restrictions",
            "sections/template-restricted.liquid",
            """<div class="product-specific">
  <h2>{{ section.settings.heading }}</h2>
</div>

{% schema %}
{
  "name": "Product Section",
  "enabled_on": {
    "templates": ["product"]
  },
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading"
    }
  ]
}
{% endschema %}""",
            ["Regular sections should not use enabled_on/disabled_on"],
            should_have_issues=True
        )

    def run_all_tests(self):
        """Run all accuracy tests"""
        print("🎯 Validator Accuracy Test Suite")
        print("=" * 60)

        test_groups = [
            self.test_file_type_detection,
            self.test_schema_validation,
            self.test_app_block_validation,
            self.test_static_block_ids,
            self.test_liquid_validation,
            self.test_performance_validation,
            self.test_template_restrictions
        ]

        for test_group in test_groups:
            try:
                test_group()
            except Exception as e:
                print(f"❌ Test group {test_group.__name__} failed: {str(e)}")
                self.failed += 1

        # Print summary
        total_tests = self.passed + self.failed
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0

        print(f"\n{'='*60}")
        print("ACCURACY TEST SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Passed: {self.passed}/{total_tests}")
        print(f"❌ Failed: {self.failed}/{total_tests}")
        print(f"📊 Success Rate: {success_rate:.1f}%")

        if success_rate >= 95:
            print("🎉 Validator accuracy is excellent!")
            return True
        elif success_rate >= 85:
            print("⚠️  Validator accuracy is good but could be improved")
            return False
        else:
            print("🚨 Validator accuracy needs significant improvement")
            return False

def main():
    """Run the accuracy test suite"""
    tester = ValidatorAccuracyTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()