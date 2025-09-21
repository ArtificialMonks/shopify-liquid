#!/usr/bin/env python3
"""
Validator Performance Benchmark Suite
Measures and optimizes validator performance across different scenarios
"""

import time
import psutil
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import statistics
import tempfile
import shutil
import json

# Add the scripts directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from validator_module import UltimateShopifyValidator, Severity
except ImportError:
    print("ERROR: Could not import validator classes")
    sys.exit(1)

class ValidatorBenchmark:
    """Performance benchmark suite for the Shopify Liquid validator"""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.code_library = self.repo_root / "shopify-liquid-guides" / "code-library"
        self.results = {}
        self.baseline_metrics = {}

    def measure_memory_usage(self, func, *args, **kwargs):
        """Measure memory usage during function execution"""
        process = psutil.Process(os.getpid())

        # Get baseline memory
        baseline_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Execute function
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        # Get peak memory
        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = peak_memory - baseline_memory

        return {
            'result': result,
            'duration': end_time - start_time,
            'memory_used_mb': memory_used,
            'peak_memory_mb': peak_memory
        }

    def create_test_files(self, file_count: int, complexity: str = 'simple') -> Path:
        """Create test files for benchmarking"""
        test_dir = Path(tempfile.mkdtemp(prefix=f"benchmark_{complexity}_"))

        templates = {
            'simple': {
                'content': '''<div class="simple-section">
  <h2>{{ section.settings.heading | escape }}</h2>
  <p>{{ section.settings.text | escape }}</p>
</div>

{% schema %}
{
  "name": "Simple Section",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading"
    },
    {
      "type": "textarea",
      "id": "text",
      "label": "Text"
    }
  ]
}
{% endschema %}''',
                'prefix': 'simple-section'
            },
            'complex': {
                'content': '''<div class="complex-section"
     data-section-id="{{ section.id }}"
     data-section-type="{{ section.type }}">

  {% if section.settings.show_heading %}
    <h2 class="section-heading">{{ section.settings.heading | escape }}</h2>
  {% endif %}

  <div class="blocks-container">
    {% for block in section.blocks %}
      {% case block.type %}
        {% when 'text' %}
          <div class="text-block" {{ block.shopify_attributes }}>
            <h3>{{ block.settings.heading | escape }}</h3>
            <div class="text-content">
              {{ block.settings.content }}
            </div>
          </div>

        {% when 'image' %}
          <div class="image-block" {{ block.shopify_attributes }}>
            {% if block.settings.image %}
              <img src="{{ block.settings.image | image_url: width: 800 }}"
                   alt="{{ block.settings.image.alt | escape }}"
                   loading="lazy"
                   width="800"
                   height="600">
            {% endif %}
          </div>

        {% when 'button' %}
          <div class="button-block" {{ block.shopify_attributes }}>
            {% if block.settings.button_url %}
              <a href="{{ block.settings.button_url }}" class="btn">
                {{ block.settings.button_text | escape }}
              </a>
            {% endif %}
          </div>
      {% endcase %}
    {% endfor %}
  </div>
</div>

{% schema %}
{
  "name": "Complex Section",
  "settings": [
    {
      "type": "checkbox",
      "id": "show_heading",
      "label": "Show heading",
      "default": true
    },
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Featured Content"
    }
  ],
  "blocks": [
    {
      "type": "text",
      "name": "Text Block",
      "settings": [
        {
          "type": "text",
          "id": "heading",
          "label": "Heading"
        },
        {
          "type": "richtext",
          "id": "content",
          "label": "Content"
        }
      ]
    },
    {
      "type": "image",
      "name": "Image Block",
      "settings": [
        {
          "type": "image_picker",
          "id": "image",
          "label": "Image"
        }
      ]
    },
    {
      "type": "button",
      "name": "Button Block",
      "settings": [
        {
          "type": "text",
          "id": "button_text",
          "label": "Button text"
        },
        {
          "type": "url",
          "id": "button_url",
          "label": "Button URL"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Complex Section",
      "blocks": [
        {
          "type": "text"
        },
        {
          "type": "image"
        },
        {
          "type": "button"
        }
      ]
    }
  ]
}
{% endschema %}''',
                'prefix': 'complex-section'
            }
        }

        template = templates[complexity]

        # Create sections directory
        sections_dir = test_dir / "sections"
        sections_dir.mkdir(parents=True)

        # Create test files
        for i in range(file_count):
            file_path = sections_dir / f"{template['prefix']}-{i:03d}.liquid"
            file_path.write_text(template['content'])

        # Create a layout file
        layout_dir = test_dir / "layout"
        layout_dir.mkdir()
        layout_file = layout_dir / "theme.liquid"
        layout_file.write_text('''<!DOCTYPE html>
<html>
<head>
  <title>{{ page_title }}</title>
  {{ content_for_header }}
</head>
<body>
  {{ content_for_layout }}
</body>
</html>''')

        return test_dir

    def benchmark_single_file(self, file_path: Path, iterations: int = 5) -> Dict:
        """Benchmark validation of a single file"""
        print(f"   📄 Benchmarking: {file_path.name}")

        durations = []
        memory_usages = []

        for i in range(iterations):
            validator = UltimateShopifyValidator()

            def validate_file():
                validator.validate_file(file_path)
                return len(validator.issues)

            metrics = self.measure_memory_usage(validate_file)
            durations.append(metrics['duration'])
            memory_usages.append(metrics['memory_used_mb'])

        return {
            'file': str(file_path.name),
            'iterations': iterations,
            'avg_duration_ms': statistics.mean(durations) * 1000,
            'min_duration_ms': min(durations) * 1000,
            'max_duration_ms': max(durations) * 1000,
            'std_duration_ms': statistics.stdev(durations) * 1000 if len(durations) > 1 else 0,
            'avg_memory_mb': statistics.mean(memory_usages),
            'max_memory_mb': max(memory_usages)
        }

    def benchmark_directory(self, directory: Path, iterations: int = 3) -> Dict:
        """Benchmark validation of an entire directory"""
        print(f"   📁 Benchmarking directory: {directory.name}")

        durations = []
        memory_usages = []
        file_counts = []

        for i in range(iterations):
            validator = UltimateShopifyValidator()

            def validate_directory():
                issue_count = 0
                file_count = 0

                for file_path in directory.rglob('*.liquid'):
                    if any(skip in str(file_path) for skip in ['node_modules', '.git']):
                        continue
                    validator.validate_file(file_path)
                    file_count += 1

                return len(validator.issues), file_count

            metrics = self.measure_memory_usage(validate_directory)
            issues, files = metrics['result']

            durations.append(metrics['duration'])
            memory_usages.append(metrics['memory_used_mb'])
            file_counts.append(files)

        avg_files = statistics.mean(file_counts)

        return {
            'directory': str(directory.name),
            'iterations': iterations,
            'avg_files_processed': avg_files,
            'avg_duration_s': statistics.mean(durations),
            'min_duration_s': min(durations),
            'max_duration_s': max(durations),
            'files_per_second': avg_files / statistics.mean(durations),
            'avg_memory_mb': statistics.mean(memory_usages),
            'max_memory_mb': max(memory_usages)
        }

    def benchmark_scalability(self) -> Dict:
        """Test validator performance at different scales"""
        print("\n📊 Running Scalability Benchmarks")
        print("=" * 50)

        scales = [1, 5, 10, 25, 50, 100]
        results = {}

        for scale in scales:
            print(f"\n🔬 Testing scale: {scale} files")
            test_dir = self.create_test_files(scale, 'simple')

            try:
                result = self.benchmark_directory(test_dir, iterations=3)
                result['scale'] = scale
                results[f"scale_{scale}"] = result

                print(f"   ✅ {scale} files: {result['avg_duration_s']:.2f}s, "
                      f"{result['files_per_second']:.1f} files/s")

            finally:
                shutil.rmtree(test_dir)

        return results

    def benchmark_complexity(self) -> Dict:
        """Test validator performance on different complexity levels"""
        print("\n🧩 Running Complexity Benchmarks")
        print("=" * 50)

        complexities = ['simple', 'complex']
        file_count = 10
        results = {}

        for complexity in complexities:
            print(f"\n🔬 Testing complexity: {complexity}")
            test_dir = self.create_test_files(file_count, complexity)

            try:
                result = self.benchmark_directory(test_dir, iterations=5)
                result['complexity'] = complexity
                result['file_count'] = file_count
                results[f"complexity_{complexity}"] = result

                print(f"   ✅ {complexity}: {result['avg_duration_s']:.2f}s, "
                      f"{result['files_per_second']:.1f} files/s")

            finally:
                shutil.rmtree(test_dir)

        return results

    def benchmark_real_codebase(self) -> Dict:
        """Benchmark on the actual code library"""
        print("\n🏭 Running Real Codebase Benchmark")
        print("=" * 50)

        if not self.code_library.exists():
            print("❌ Code library not found - skipping real codebase benchmark")
            return {}

        result = self.benchmark_directory(self.code_library, iterations=5)
        result['codebase'] = 'shopify-liquid-guides'

        print(f"   ✅ Real codebase: {result['avg_duration_s']:.2f}s, "
              f"{result['files_per_second']:.1f} files/s, "
              f"{result['avg_files_processed']:.0f} files")

        return {'real_codebase': result}

    def profile_validation_steps(self) -> Dict:
        """Profile individual validation steps"""
        print("\n🔍 Profiling Validation Steps")
        print("=" * 50)

        test_dir = self.create_test_files(5, 'complex')

        try:
            validator = UltimateShopifyValidator()

            # Profile each major step
            steps = {}

            for file_path in list(test_dir.rglob('*.liquid'))[:3]:  # Profile 3 files
                print(f"   📄 Profiling: {file_path.name}")

                # Read file
                start = time.time()
                content = file_path.read_text()
                steps['file_read'] = time.time() - start

                # File type detection
                start = time.time()
                file_type = validator.detect_file_type(file_path, content)
                steps['file_type_detection'] = time.time() - start

                # Schema extraction
                start = time.time()
                schema = validator.extract_schema(content)
                steps['schema_extraction'] = time.time() - start

                # Schema validation (if exists)
                if schema:
                    start = time.time()
                    validator.validate_schema(schema, file_path, file_type)
                    steps['schema_validation'] = time.time() - start

                # Content validation
                start = time.time()
                validator.validate_liquid_content(content, file_path)
                steps['content_validation'] = time.time() - start

                break  # Profile just one file for detailed breakdown

            return {'profiling': steps}

        finally:
            shutil.rmtree(test_dir)

    def benchmark_memory_efficiency(self) -> Dict:
        """Test memory efficiency across different scenarios"""
        print("\n💾 Running Memory Efficiency Tests")
        print("=" * 50)

        results = {}

        # Test memory usage with large files
        large_file_dir = self.create_test_files(1, 'complex')

        try:
            # Create a very large file
            large_file = large_file_dir / "sections" / "huge-section.liquid"
            content = large_file.read_text()

            # Multiply content to create large file
            large_content = content * 50  # Make it ~50x larger
            large_file.write_text(large_content)

            validator = UltimateShopifyValidator()

            def validate_large():
                validator.validate_file(large_file)
                return len(validator.issues)

            metrics = self.measure_memory_usage(validate_large)

            results['large_file'] = {
                'file_size_kb': len(large_content) / 1024,
                'duration_s': metrics['duration'],
                'memory_used_mb': metrics['memory_used_mb']
            }

            print(f"   📏 Large file ({results['large_file']['file_size_kb']:.1f}KB): "
                  f"{metrics['duration']:.2f}s, {metrics['memory_used_mb']:.1f}MB")

        finally:
            shutil.rmtree(large_file_dir)

        return results

    def generate_performance_report(self, all_results: Dict) -> str:
        """Generate a comprehensive performance report"""
        report = []
        report.append("=" * 80)
        report.append("VALIDATOR PERFORMANCE BENCHMARK REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Python: {sys.version}")
        report.append(f"Platform: {os.uname().sysname} {os.uname().release}")
        report.append("")

        # Scalability Results
        if 'scalability' in all_results:
            report.append("📊 SCALABILITY PERFORMANCE")
            report.append("-" * 40)

            scales = [k for k in all_results['scalability'].keys() if k.startswith('scale_')]
            scales.sort(key=lambda x: int(x.split('_')[1]))

            report.append(f"{'Files':<8} {'Duration(s)':<12} {'Files/sec':<12} {'Memory(MB)':<12}")
            report.append("-" * 48)

            for scale_key in scales:
                result = all_results['scalability'][scale_key]
                report.append(f"{result['scale']:<8} "
                            f"{result['avg_duration_s']:<12.2f} "
                            f"{result['files_per_second']:<12.1f} "
                            f"{result['avg_memory_mb']:<12.1f}")

            report.append("")

        # Complexity Results
        if 'complexity' in all_results:
            report.append("🧩 COMPLEXITY PERFORMANCE")
            report.append("-" * 40)

            for complexity_key, result in all_results['complexity'].items():
                complexity = result['complexity']
                report.append(f"{complexity.title()} files: "
                            f"{result['avg_duration_s']:.2f}s, "
                            f"{result['files_per_second']:.1f} files/sec, "
                            f"{result['avg_memory_mb']:.1f}MB")

            report.append("")

        # Real Codebase Results
        if 'real_codebase' in all_results and all_results['real_codebase']:
            report.append("🏭 REAL CODEBASE PERFORMANCE")
            report.append("-" * 40)

            result = all_results['real_codebase']['real_codebase']
            report.append(f"Files processed: {result['avg_files_processed']:.0f}")
            report.append(f"Total duration: {result['avg_duration_s']:.2f} seconds")
            report.append(f"Processing rate: {result['files_per_second']:.1f} files/second")
            report.append(f"Memory usage: {result['avg_memory_mb']:.1f} MB")
            report.append("")

        # Performance Assessment
        report.append("🎯 PERFORMANCE ASSESSMENT")
        report.append("-" * 40)

        # Determine performance grade
        if 'real_codebase' in all_results and all_results['real_codebase']:
            rate = all_results['real_codebase']['real_codebase']['files_per_second']
            memory = all_results['real_codebase']['real_codebase']['avg_memory_mb']

            if rate > 50 and memory < 100:
                grade = "🏆 EXCELLENT"
            elif rate > 20 and memory < 200:
                grade = "✅ GOOD"
            elif rate > 10 and memory < 300:
                grade = "⚠️  ACCEPTABLE"
            else:
                grade = "🚨 NEEDS IMPROVEMENT"

            report.append(f"Overall Performance: {grade}")
            report.append(f"Processing Rate: {rate:.1f} files/second")
            report.append(f"Memory Efficiency: {memory:.1f} MB")

        # Recommendations
        report.append("")
        report.append("💡 OPTIMIZATION RECOMMENDATIONS")
        report.append("-" * 40)

        # Add specific recommendations based on results
        if 'scalability' in all_results:
            scales = list(all_results['scalability'].keys())
            if len(scales) >= 2:
                small = all_results['scalability'][scales[0]]
                large = all_results['scalability'][scales[-1]]

                rate_ratio = small['files_per_second'] / large['files_per_second']
                if rate_ratio > 2:
                    report.append("- Performance degrades significantly with scale")
                    report.append("- Consider batch processing optimizations")

        if 'profiling' in all_results:
            steps = all_results['profiling']['profiling']
            slowest_step = max(steps.items(), key=lambda x: x[1])
            report.append(f"- Slowest validation step: {slowest_step[0]} ({slowest_step[1]*1000:.1f}ms)")
            report.append("- Focus optimization efforts on this step")

        report.append("- Consider caching for repeated validations")
        report.append("- Use parallel processing for large theme validation")

        return "\n".join(report)

    def run_all_benchmarks(self) -> Dict:
        """Run complete benchmark suite"""
        print("🚀 Validator Performance Benchmark Suite")
        print("=" * 80)

        all_results = {}

        try:
            # Run all benchmark categories
            all_results['scalability'] = self.benchmark_scalability()
            all_results['complexity'] = self.benchmark_complexity()
            all_results['real_codebase'] = self.benchmark_real_codebase()
            all_results['profiling'] = self.profile_validation_steps()
            all_results['memory'] = self.benchmark_memory_efficiency()

            # Generate and save report
            report = self.generate_performance_report(all_results)

            # Save results
            results_file = Path(__file__).parent / "benchmark-results.json"
            with open(results_file, 'w') as f:
                json.dump(all_results, f, indent=2, default=str)

            # Save report
            report_file = Path(__file__).parent / "benchmark-report.txt"
            report_file.write_text(report)

            print(f"\n📊 Results saved to: {results_file}")
            print(f"📋 Report saved to: {report_file}")

            # Print summary
            print("\n" + report)

            return all_results

        except Exception as e:
            print(f"❌ Benchmark failed: {str(e)}")
            return {}

def main():
    """Run the performance benchmark suite"""
    benchmark = ValidatorBenchmark()
    results = benchmark.run_all_benchmarks()

    # Return success based on overall performance
    if results and 'real_codebase' in results and results['real_codebase']:
        rate = results['real_codebase']['real_codebase']['files_per_second']
        success = rate > 10  # At least 10 files per second
        sys.exit(0 if success else 1)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()