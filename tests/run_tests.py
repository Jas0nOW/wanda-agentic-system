"""Test runner script for WANDA Voice Core.

This script runs all tests and generates a comprehensive report.
"""

import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime


def run_tests(test_type="all", verbose=True, coverage=False):
    """Run WANDA test suite.

    Args:
        test_type: Type of tests to run (unit, integration, e2e, regression, performance, all)
        verbose: Show detailed output
        coverage: Generate coverage report
    """
    test_dir = Path(__file__).parent.parent / "tests"

    # Build pytest command
    cmd = ["pytest"]

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(["--cov=wanda_voice_core", "--cov-report=html", "--cov-report=term"])

    # Select tests based on type
    if test_type == "unit":
        cmd.append(str(test_dir / "unit"))
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.append(str(test_dir / "integration"))
        cmd.extend(["-m", "integration"])
    elif test_type == "e2e":
        cmd.append(str(test_dir / "e2e"))
        cmd.extend(["-m", "e2e"])
    elif test_type == "regression":
        cmd.append(str(test_dir / "regression"))
        cmd.extend(["-m", "regression"])
    elif test_type == "performance":
        cmd.append(str(test_dir / "performance"))
        cmd.extend(["-m", "performance"])
    elif test_type == "fast":
        # Run only fast tests (exclude slow, e2e, performance)
        cmd.append(str(test_dir))
        cmd.extend(["-m", "not slow and not e2e and not performance"])
    else:  # all
        cmd.append(str(test_dir))

    # Run tests
    print(f"🧪 Running {test_type} tests...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)

    start_time = time.time()
    result = subprocess.run(cmd, capture_output=False)
    elapsed = time.time() - start_time

    print("-" * 60)
    print(f"⏱️  Test run completed in {elapsed:.2f}s")

    if result.returncode == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ Tests failed with exit code {result.returncode}")

    return result.returncode


def run_specific_test(test_file):
    """Run a specific test file."""
    cmd = ["pytest", test_file, "-v"]
    print(f"🧪 Running {test_file}...")
    result = subprocess.run(cmd)
    return result.returncode


def generate_report():
    """Generate comprehensive test report."""
    report_dir = Path(__file__).parent.parent / "tests" / "reports"
    report_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"test_report_{timestamp}.txt"

    # Run tests with output capture
    cmd = [
        "pytest",
        str(Path(__file__).parent.parent / "tests"),
        "-v",
        "--tb=short",
        "--cov=wanda_voice_core",
        "--cov-report=term",
    ]

    with open(report_file, "w") as f:
        f.write(f"WANDA Test Report - {datetime.now()}\n")
        f.write("=" * 60 + "\n\n")

        result = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)

    print(f"📊 Report saved to: {report_file}")
    return report_file


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run WANDA tests")
    parser.add_argument(
        "type",
        nargs="?",
        default="fast",
        choices=[
            "unit",
            "integration",
            "e2e",
            "regression",
            "performance",
            "fast",
            "all",
        ],
        help="Type of tests to run",
    )
    parser.add_argument(
        "--coverage", "-c", action="store_true", help="Generate coverage report"
    )
    parser.add_argument(
        "--report", "-r", action="store_true", help="Generate detailed report"
    )
    parser.add_argument("--file", "-f", help="Run specific test file")

    args = parser.parse_args()

    if args.file:
        exit_code = run_specific_test(args.file)
    elif args.report:
        report_path = generate_report()
        exit_code = 0
    else:
        exit_code = run_tests(args.type, coverage=args.coverage)

    sys.exit(exit_code)
