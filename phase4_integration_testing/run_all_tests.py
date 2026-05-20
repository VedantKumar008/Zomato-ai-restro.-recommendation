"""
Master Test Runner
Runs all test suites and generates a comprehensive report
"""

import subprocess
import sys
import os
from datetime import datetime


def run_command(command, cwd):
    """Run a command and return the result"""
    print(f"\n{'='*80}")
    print(f"Running: {command}")
    print(f"Directory: {cwd}")
    print('='*80)
    
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result


def main():
    """Run all test suites"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(base_dir, "reports")
    
    # Create reports directory if it doesn't exist
    os.makedirs(reports_dir, exist_ok=True)
    
    # Initialize report
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("COMPREHENSIVE TEST REPORT")
    report_lines.append("=" * 80)
    report_lines.append(f"Test Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # Track overall status
    all_passed = True
    
    # 1. Run E2E Tests
    print("\n" + "="*80)
    print("PHASE 1: End-to-End Tests")
    print("="*80)
    e2e_dir = os.path.join(base_dir, "e2e_tests")
    e2e_result = run_command("pytest test_e2e.py -v -s --tb=short", e2e_dir)
    
    report_lines.append("## End-to-End Tests")
    report_lines.append(f"Exit Code: {e2e_result.returncode}")
    report_lines.append(f"Status: {'PASSED' if e2e_result.returncode == 0 else 'FAILED'}")
    report_lines.append("")
    
    if e2e_result.returncode != 0:
        all_passed = False
    
    # 2. Run Performance Tests
    print("\n" + "="*80)
    print("PHASE 2: Performance Tests")
    print("="*80)
    perf_dir = os.path.join(base_dir, "performance_tests")
    perf_result = run_command("python load_test.py", perf_dir)
    
    report_lines.append("## Performance Tests")
    report_lines.append(f"Exit Code: {perf_result.returncode}")
    report_lines.append(f"Status: {'PASSED' if perf_result.returncode == 0 else 'FAILED'}")
    report_lines.append("")
    
    if perf_result.returncode != 0:
        all_passed = False
    
    # 3. Run Error Handling Tests
    print("\n" + "="*80)
    print("PHASE 3: Error Handling Tests")
    print("="*80)
    error_dir = os.path.join(base_dir, "error_handling_tests")
    error_result = run_command("pytest test_errors.py -v -s --tb=short", error_dir)
    
    report_lines.append("## Error Handling Tests")
    report_lines.append(f"Exit Code: {error_result.returncode}")
    report_lines.append(f"Status: {'PASSED' if error_result.returncode == 0 else 'FAILED'}")
    report_lines.append("")
    
    if error_result.returncode != 0:
        all_passed = False
    
    # 4. Generate Summary
    report_lines.append("=" * 80)
    report_lines.append("SUMMARY")
    report_lines.append("=" * 80)
    report_lines.append(f"Overall Status: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    report_lines.append("")
    
    report_lines.append("Test Suite Results:")
    report_lines.append(f"  - E2E Tests: {'PASSED' if e2e_result.returncode == 0 else 'FAILED'}")
    report_lines.append(f"  - Performance Tests: {'PASSED' if perf_result.returncode == 0 else 'FAILED'}")
    report_lines.append(f"  - Error Handling Tests: {'PASSED' if error_result.returncode == 0 else 'FAILED'}")
    report_lines.append("")
    
    # 5. Write comprehensive report
    report_path = os.path.join(reports_dir, "comprehensive_test_report.txt")
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))
    
    print("\n" + "="*80)
    print("COMPREHENSIVE TEST REPORT GENERATED")
    print("="*80)
    print(f"Report saved to: {report_path}")
    print(f"\nOverall Status: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    
    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
