#!/usr/bin/env python3
"""
Simple test to verify Docker setup works correctly.
This script checks for required environment variables and dependencies.
"""

import os
import sys
import importlib


def check_environment_variables():
    """Check required environment variables are set."""
    required_vars = [
        "DB_HOST",
        "DB_USER",
        "DB_PASS",
        "DB_NAME",
        "GCP_PROJECT_ID",
        "GCP_LOCATION",
        "GCP_CORPUS_NAME",
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False

    print("✅ All required environment variables are set")
    return True


def check_dependencies():
    """Check if required Python packages are installed."""
    required_packages = [
        "dotenv",
        "google.auth",
        "google.cloud.aiplatform",
        "gspread",
        "pandas",
        "psycopg2",
        "yaml",
        "tenacity",
        "vertexai",
    ]

    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        return False

    print("✅ All required packages are installed")
    return True


def check_config_files():
    """Check if required configuration files exist."""
    required_files = ["config/config.py", "config/plugin_config.yml", "pyproject.toml"]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False

    print("✅ All required configuration files exist")
    return True


def main():
    """Run all checks."""
    print("🔍 Running Docker setup checks...\n")

    checks = [
        ("Environment Variables", check_environment_variables),
        ("Dependencies", check_dependencies),
        ("Configuration Files", check_config_files),
    ]

    all_passed = True
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        if not check_func():
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All checks passed! Docker setup is ready.")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
