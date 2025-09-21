#!/usr/bin/env python3
"""
Theme Check Integration Tests for Validator Accuracy
Tests our validator against official Theme Check CLI to ensure 100% accuracy
"""

import subprocess
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import tempfile
import shutil
import re

# Add the scripts directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from validator_module import UltimateShopifyValidator, Severity
except ImportError:
    print("ERROR: Could not import validator classes")
    print("Make sure ultimate-validator.py is in the same directory as this test file")
    sys.exit(1)

class ThemeCheckIntegrationTest:
    """Integration test suite comparing our validator with official Theme Check"""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.code_library = self.repo_root / "shopify-liquid-guides" / "code-library"
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "errors": [],
            "comparisons": []
        }

    def check_theme_check_installed(self) -> bool:
        """Check if Theme Check CLI is available"""
        try:
            result = subprocess.run(['theme', 'check', '--version'],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Theme Check CLI found: {result.stdout.strip()}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # Try alternative command
        try:
            result = subprocess.run(['shopify', 'theme', 'check', '--version'],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Shopify Theme Check found: {result.stdout.strip()}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        print("❌ Theme Check CLI not found")
        print("Install with: npm install -g @shopify/theme-check")
        print("Or: npm install -g @shopify/cli")
        return False

    def run_theme_check(self, theme_path: Path, config_file: Optional[str] = None) -> Dict:
        """Run official Theme Check on a theme directory"""
        cmd = ['theme', 'check', str(theme_path)]
        if config_file:
            cmd.extend(['--config', config_file])
        cmd.extend(['--output', 'json'])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            # Try alternative command if first fails
            if result.returncode != 0:
                cmd[0] = 'shopify'
                cmd.insert(1, 'theme')
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.stdout:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    # Parse text output if JSON fails
                    return self.parse_text_output(result.stdout)

            return {"files": [], "errors": []}

        except subprocess.TimeoutExpired:
            return {"files": [], "errors": ["Theme Check timeout"]}
        except Exception as e:
            return {"files": [], "errors": [f"Theme Check error: {str(e)}"]}

    def parse_text_output(self, output: str) -> Dict:
        """Parse Theme Check text output when JSON isn't available"""
        files = []
        current_file = None

        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue

            # File path line
            if line.endswith('.liquid') or line.endswith('.json'):
                if current_file:
                    files.append(current_file)
                current_file = {"path": line, "offenses": []}

            # Offense line (severity:line:column message)
            elif ':' in line and current_file:
                parts = line.split(':', 3)
                if len(parts) >= 3:
                    try:
                        severity = parts[0].strip()
                        line_num = int(parts[1]) if parts[1].isdigit() else 0
                        column = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
                        message = parts[3].strip() if len(parts) > 3 else parts[2].strip()

                        current_file["offenses"].append({
                            "severity": severity,
                            "line": line_num,
                            "column": column,
                            "message": message
                        })
                    except (ValueError, IndexError):
                        continue

        if current_file:
            files.append(current_file)

        return {"files": files, "errors": []}

    def run_our_validator(self, theme_path: Path) -> Dict:
        """Run our validator on a theme directory"""
        validator = UltimateShopifyValidator()

        # Find all liquid and json files
        issues = []
        for file_path in theme_path.rglob('*.liquid'):
            if any(skip in str(file_path) for skip in ['node_modules', '.git', 'dist']):
                continue
            validator.validate_file(file_path)

        for file_path in theme_path.rglob('*.json'):
            if any(skip in str(file_path) for skip in ['node_modules', '.git', 'dist']):
                continue
            if file_path.name.startswith('en.') or file_path.parent.name == 'locales':
                continue  # Skip locale files for now
            validator.validate_file(file_path)

        # Format results similar to Theme Check
        files = {}
        for issue in validator.issues:
            file_path = str(issue.file_path.relative_to(theme_path))
            if file_path not in files:
                files[file_path] = {"path": file_path, "offenses": []}

            files[file_path]["offenses"].append({
                "severity": issue.severity.value.lower(),
                "line": issue.line_number,
                "column": issue.column,
                "message": issue.message
            })

        return {"files": list(files.values()), "errors": []}

    def compare_results(self, theme_check_result: Dict, our_result: Dict, test_name: str) -> bool:
        """Compare results from Theme Check and our validator"""
        print(f"\n{'='*60}")
        print(f"Test: {test_name}")
        print(f"{'='*60}")

        theme_check_files = {f["path"]: f for f in theme_check_result.get("files", [])}
        our_files = {f["path"]: f for f in our_result.get("files", [])}

        all_files = set(theme_check_files.keys()) | set(our_files.keys())

        overall_match = True
        file_comparisons = []

        for file_path in sorted(all_files):
            tc_file = theme_check_files.get(file_path, {"path": file_path, "offenses": []})
            our_file = our_files.get(file_path, {"path": file_path, "offenses": []})

            tc_offenses = tc_file.get("offenses", [])
            our_offenses = our_file.get("offenses", [])

            # Normalize for comparison
            tc_normalized = self.normalize_offenses(tc_offenses)
            our_normalized = self.normalize_offenses(our_offenses)

            file_match = self.compare_offense_sets(tc_normalized, our_normalized)

            if not file_match:
                overall_match = False

            file_comparison = {
                "file": file_path,
                "match": file_match,
                "theme_check_count": len(tc_offenses),
                "our_count": len(our_offenses),
                "theme_check_offenses": tc_offenses,
                "our_offenses": our_offenses
            }
            file_comparisons.append(file_comparison)

            print(f"\n📁 {file_path}")
            print(f"   Theme Check: {len(tc_offenses)} issues")
            print(f"   Our Validator: {len(our_offenses)} issues")
            print(f"   Match: {'✅' if file_match else '❌'}")

            if not file_match:
                self.print_detailed_comparison(tc_offenses, our_offenses)

        comparison_result = {
            "test_name": test_name,
            "overall_match": overall_match,
            "files": file_comparisons
        }
        self.test_results["comparisons"].append(comparison_result)

        if overall_match:
            self.test_results["passed"] += 1
            print(f"\n✅ {test_name}: PASSED")
        else:
            self.test_results["failed"] += 1
            print(f"\n❌ {test_name}: FAILED")

        return overall_match

    def normalize_offenses(self, offenses: List[Dict]) -> List[Dict]:
        """Normalize offenses for comparison"""
        normalized = []
        for offense in offenses:
            normalized.append({
                "severity": offense.get("severity", "").lower(),
                "message": self.normalize_message(offense.get("message", "")),
                "line": offense.get("line", 0)
            })
        return normalized

    def normalize_message(self, message: str) -> str:
        """Normalize error messages for comparison"""
        # Remove file paths and line numbers
        message = re.sub(r'\b\d+:\d+\b', '', message)
        message = re.sub(r'\bline \d+\b', '', message)
        message = re.sub(r'\S+\.liquid\b', 'file.liquid', message)

        # Normalize common message variations
        normalizations = {
            "Missing schema block": "missing schema",
            "Schema block is required": "missing schema",
            "External stylesheet": "external asset",
            "Remote asset": "external asset"
        }

        for old, new in normalizations.items():
            if old.lower() in message.lower():
                return new

        return message.lower().strip()

    def compare_offense_sets(self, set1: List[Dict], set2: List[Dict]) -> bool:
        """Compare two sets of offenses for equivalence"""
        if len(set1) != len(set2):
            return False

        # For each offense in set1, find a matching offense in set2
        for offense1 in set1:
            found_match = False
            for offense2 in set2:
                if (offense1["severity"] == offense2["severity"] and
                    offense1["message"] == offense2["message"]):
                    found_match = True
                    break
            if not found_match:
                return False

        return True

    def print_detailed_comparison(self, tc_offenses: List[Dict], our_offenses: List[Dict]):
        """Print detailed comparison of offenses"""
        print(f"\n   🔍 Detailed Comparison:")

        if tc_offenses:
            print(f"   Theme Check Issues:")
            for i, offense in enumerate(tc_offenses, 1):
                print(f"     {i}. {offense.get('severity', 'unknown')}: {offense.get('message', 'no message')}")

        if our_offenses:
            print(f"   Our Validator Issues:")
            for i, offense in enumerate(our_offenses, 1):
                print(f"     {i}. {offense.get('severity', 'unknown')}: {offense.get('message', 'no message')}")

        if not tc_offenses and not our_offenses:
            print(f"   Both found no issues")

    def create_test_theme(self, name: str, files: Dict[str, str]) -> Path:
        """Create a temporary test theme with specified files"""
        test_dir = Path(tempfile.mkdtemp(prefix=f"theme_test_{name}_"))

        for file_path, content in files.items():
            full_path = test_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)

        return test_dir

    def test_basic_section(self):
        """Test basic section validation"""
        files = {
            "sections/hero.liquid": """
<div class="hero">
  <h1>{{ section.settings.heading | escape }}</h1>
</div>

{% schema %}
{
  "name": "Hero Section",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Welcome"
    }
  ]
}
{% endschema %}
""",
            "layout/theme.liquid": """
<!DOCTYPE html>
<html>
<head>
  <title>{{ page_title }}</title>
</head>
<body>
  {{ content_for_layout }}
</body>
</html>
"""
        }

        test_theme = self.create_test_theme("basic_section", files)
        try:
            tc_result = self.run_theme_check(test_theme)
            our_result = self.run_our_validator(test_theme)
            return self.compare_results(tc_result, our_result, "Basic Section Test")
        finally:
            shutil.rmtree(test_theme)

    def test_invalid_schema(self):
        """Test invalid schema detection"""
        files = {
            "sections/invalid.liquid": """
<div>Invalid section</div>

{% schema %}
{
  "name": "Invalid Section",
  "settings": [
    {
      "type": "range",
      "id": "count",
      "min": 1,
      "max": 100,
      "step": 33,
      "default": 50
    }
  ]
}
{% endschema %}
"""
        }

        test_theme = self.create_test_theme("invalid_schema", files)
        try:
            tc_result = self.run_theme_check(test_theme)
            our_result = self.run_our_validator(test_theme)
            return self.compare_results(tc_result, our_result, "Invalid Schema Test")
        finally:
            shutil.rmtree(test_theme)

    def test_app_blocks(self):
        """Test @app block validation"""
        files = {
            "sections/apps.liquid": """
<div class="apps-wrapper">
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
{% endschema %}
"""
        }

        test_theme = self.create_test_theme("app_blocks", files)
        try:
            tc_result = self.run_theme_check(test_theme)
            our_result = self.run_our_validator(test_theme)
            return self.compare_results(tc_result, our_result, "App Blocks Test")
        finally:
            shutil.rmtree(test_theme)

    def test_code_library(self):
        """Test our actual code library"""
        if not self.code_library.exists():
            print(f"❌ Code library not found at {self.code_library}")
            return False

        tc_result = self.run_theme_check(self.code_library)
        our_result = self.run_our_validator(self.code_library)
        return self.compare_results(tc_result, our_result, "Code Library Test")

    def run_all_tests(self):
        """Run all integration tests"""
        print("🔍 Theme Check Integration Tests")
        print("=" * 60)

        if not self.check_theme_check_installed():
            print("\n❌ Cannot run integration tests without Theme Check CLI")
            print("Install Theme Check and try again")
            return False

        tests = [
            self.test_basic_section,
            self.test_invalid_schema,
            self.test_app_blocks,
            self.test_code_library
        ]

        for test in tests:
            try:
                test()
            except Exception as e:
                self.test_results["failed"] += 1
                self.test_results["errors"].append(f"Test {test.__name__} failed: {str(e)}")
                print(f"❌ {test.__name__}: ERROR - {str(e)}")

        # Print summary
        print(f"\n{'='*60}")
        print("INTEGRATION TEST SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Passed: {self.test_results['passed']}")
        print(f"❌ Failed: {self.test_results['failed']}")
        print(f"🚨 Errors: {len(self.test_results['errors'])}")

        if self.test_results['errors']:
            print(f"\nErrors:")
            for error in self.test_results['errors']:
                print(f"  - {error}")

        success_rate = (self.test_results['passed'] /
                       (self.test_results['passed'] + self.test_results['failed']) * 100
                       if (self.test_results['passed'] + self.test_results['failed']) > 0 else 0)

        print(f"\nSuccess Rate: {success_rate:.1f}%")

        if success_rate >= 90:
            print("🎉 Validator accuracy is excellent!")
        elif success_rate >= 75:
            print("⚠️  Validator accuracy needs improvement")
        else:
            print("🚨 Validator accuracy is poor - major fixes needed")

        return success_rate >= 90

def main():
    """Run the integration test suite"""
    tester = ThemeCheckIntegrationTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()