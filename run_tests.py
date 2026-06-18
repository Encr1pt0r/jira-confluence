#!/usr/bin/env python3
"""
Test runner for JC CLI tool
Provides easy commands to run different types of tests
"""

import subprocess
import sys


def run_all_tests():
    """Run all tests with coverage"""
    print("Running all tests with coverage...\n")
    result = subprocess.run([
        sys.executable, '-m', 'pytest',
        'test_jc.py',
        '-v',
        '--tb=short',
        '--cov=jc',
        '--cov-report=term-missing',
        '--cov-report=html'
    ])
    return result.returncode


def run_quick_tests():
    """Run tests without coverage for quick feedback"""
    print("Running quick tests...\n")
    result = subprocess.run([
        sys.executable, '-m', 'pytest',
        'test_jc.py',
        '-v',
        '--tb=short'
    ])
    return result.returncode


def run_specific_test(test_name):
    """Run a specific test or test class"""
    print(f"Running test: {test_name}\n")
    result = subprocess.run([
        sys.executable, '-m', 'pytest',
        'test_jc.py',
        '-v',
        '--tb=short',
        '-k', test_name
    ])
    return result.returncode


def run_adf_tests():
    """Run only ADF text extraction tests"""
    print("Running ADF text extraction tests...\n")
    result = subprocess.run([
        sys.executable, '-m', 'pytest',
        'test_jc.py::TestADFTextExtraction',
        '-v',
        '--tb=short'
    ])
    return result.returncode


def run_command_tests():
    """Run only CLI command tests"""
    print("Running CLI command tests...\n")
    result = subprocess.run([
        sys.executable, '-m', 'pytest',
        'test_jc.py',
        '-v',
        '--tb=short',
        '-k', 'Command'
    ])
    return result.returncode


def show_usage():
    """Show usage information"""
    print("""
JC CLI Test Runner
==================

Usage: python run_tests.py [command]

Commands:
  all       - Run all tests with coverage report (default)
  quick     - Run all tests without coverage (faster)
  adf       - Run only ADF text extraction tests
  commands  - Run only CLI command tests
  <name>    - Run specific test matching <name>

Examples:
  python run_tests.py              # Run all tests with coverage
  python run_tests.py quick        # Quick test run
  python run_tests.py adf          # Test ADF parsing only
  python run_tests.py ticket       # Test all ticket-related tests
  python run_tests.py test_emoji   # Run specific emoji test

After running with coverage, open htmlcov/index.html to see detailed coverage report.
""")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # Default: run all tests with coverage
        sys.exit(run_all_tests())

    command = sys.argv[1].lower()

    if command == 'all':
        sys.exit(run_all_tests())
    elif command == 'quick':
        sys.exit(run_quick_tests())
    elif command == 'adf':
        sys.exit(run_adf_tests())
    elif command == 'commands':
        sys.exit(run_command_tests())
    elif command in ['help', '-h', '--help']:
        show_usage()
        sys.exit(0)
    else:
        # Treat as specific test name
        sys.exit(run_specific_test(command))
