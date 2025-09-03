#!/usr/bin/env python3
"""
Simple test runner script for Qantas flight booking tests
"""

import subprocess
import sys
import os


def create_directories():
    """Create necessary directories"""
    directories = ["screenshots", "reports"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")


def run_all_tests():
    """Run all test cases"""
    print("Running all test cases...")
    cmd = [
        "python", "-m", "pytest",
        "-v",
        "--html=reports/report.html",
        "--self-contained-html"
    ]
    return subprocess.run(cmd)


def run_smoke_tests():
    """Run only smoke tests"""
    print("Running smoke tests...")
    cmd = [
        "python", "-m", "pytest",
        "-m", "smoke",
        "-v",
        "--html=reports/smoke_report.html",
        "--self-contained-html"
    ]
    return subprocess.run(cmd)


def run_regression_tests():
    """Run only regression tests"""
    print("Running regression tests...")
    cmd = [
        "python", "-m", "pytest",
        "-m", "regression",
        "-v",
        "--html=reports/regression_report.html",
        "--self-contained-html"
    ]
    return subprocess.run(cmd)


def run_specific_test(test_file):
    """Run specific test case"""
    print(f"Running {test_file}...")
    cmd = [
        "python", "-m", "pytest",
        test_file,
        "-v",
        "--html=reports/single_test_report.html",
        "--self-contained-html"
    ]
    return subprocess.run(cmd)


if __name__ == "__main__":
    create_directories()

    if len(sys.argv) > 1:
        option = sys.argv[1].lower()

        if option == "smoke":
            run_smoke_tests()
        elif option == "regression":
            run_regression_tests()
        elif option.startswith("test_"):
            run_specific_test(sys.argv[1])
        else:
            print("Usage:")
            print("  python run_tests.py                 # Run all tests")
            print("  python run_tests.py smoke          # Run smoke tests")
            print("  python run_tests.py regression     # Run regression tests")
            print("  python run_tests.py testcase1_successful_oneway_flight.py # Run specific test")
    else:
        run_all_tests()