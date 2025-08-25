#!/usr/bin/env python3
"""
Test runner script for the modular system test suite.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n❌ Command not found: {cmd[0]}")
        print("Please ensure pytest is installed: pip install pytest pytest-asyncio")
        return False


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run the modular system test suite")
    parser.add_argument(
        "--type", 
        choices=["unit", "integration", "all", "quick"], 
        default="quick",
        help="Type of tests to run (default: quick)"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true",
        help="Run with coverage reporting"
    )
    parser.add_argument(
        "--parallel", "-n", 
        type=int,
        help="Run tests in parallel (requires pytest-xdist)"
    )
    parser.add_argument(
        "--stop", "-x", 
        action="store_true",
        help="Stop on first failure"
    )
    
    args = parser.parse_args()
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Base pytest command
    base_cmd = ["python3", "-m", "pytest"]
    
    if args.verbose:
        base_cmd.append("-v")
    
    if args.stop:
        base_cmd.append("-x")
    
    if args.parallel:
        base_cmd.extend(["-n", str(args.parallel)])
    
    if args.coverage:
        base_cmd.extend([
            "--cov=src",
            "--cov-report=term-missing",
            "--cov-report=html",
            "--cov-report=xml"
        ])
    
    # Test selection based on type
    if args.type == "unit":
        print("🧪 Running UNIT TESTS only...")
        cmd = base_cmd + ["-m", "unit", "tests/tools", "tests/agent_core"]
        success = run_command(cmd, "Unit Tests")
        
    elif args.type == "integration":
        print("🔗 Running INTEGRATION TESTS only...")
        cmd = base_cmd + ["-m", "integration", "tests/integration"]
        success = run_command(cmd, "Integration Tests")
        
    elif args.type == "all":
        print("🚀 Running ALL TESTS...")
        cmd = base_cmd + ["tests/"]
        success = run_command(cmd, "All Tests")
        
    else:  # quick
        print("⚡ Running QUICK TESTS (unit tests only)...")
        cmd = base_cmd + ["-m", "unit", "tests/tools", "tests/agent_core", "--tb=line"]
        success = run_command(cmd, "Quick Tests")
    
    # Summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 Test suite completed successfully!")
        print("📊 To run specific test types:")
        print("   python run_tests.py --type unit      # Unit tests only")
        print("   python run_tests.py --type integration  # Integration tests only")
        print("   python run_tests.py --type all       # All tests")
        print("   python run_tests.py --type quick     # Quick tests (default)")
        print("\n🔧 Additional options:")
        print("   python run_tests.py --verbose        # Verbose output")
        print("   python run_tests.py --coverage       # With coverage")
        print("   python run_tests.py --parallel 4     # Parallel execution")
        print("   python run_tests.py --stop           # Stop on first failure")
    else:
        print("💥 Test suite failed!")
        print("🔍 Check the output above for details")
        sys.exit(1)
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
