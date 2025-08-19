#!/usr/bin/env python3
"""
Main test runner for the Crypto Arbitrage Bot.
This script runs all tests and reports results.

COMPATIBILITY NOTE:
This test runner includes special handling for Python 3.12 compatibility with
python-telegram-bot v20.7. It pre-configures test environment to ensure
tests run correctly across different Python versions.
"""

import os
import sys
import glob
import importlib.util
import logging
import argparse
import time
import platform
from datetime import datetime
from unittest.mock import MagicMock

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Add mocks directory to path first so it takes precedence
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'mocks')))

def check_python_compatibility():
    """Check Python version and compatibility issues."""
    python_version = sys.version_info
    
    # Check if Python 3.12
    is_python_312 = (python_version.major == 3 and python_version.minor >= 12)
    
    if is_python_312:
        logger.info("Detected Python 3.12 or newer - applying compatibility fixes for tests")
        
        # Pre-mock telegram modules for Python 3.12 compatibility
        # This prevents issues with ConversationHandler initialization
        sys.modules['telegram'] = MagicMock()
        sys.modules['telegram.ext'] = MagicMock()
        
        # Define mock classes for telegram.ext to avoid isinstance issues
        class MockCommandHandler:
            def __init__(self, command, callback):
                self.command = command
                self.callback = callback
        
        class MockCallbackQueryHandler:
            def __init__(self, callback, pattern=None):
                self.callback = callback
                self.pattern = pattern
        
        class MockConversationHandler:
            def __init__(self, entry_points, states, fallbacks, per_message=True):
                self.entry_points = entry_points
                self.states = states
                self.fallbacks = fallbacks
                self.per_message = per_message
        
        # Add mock classes to telegram.ext
        sys.modules['telegram.ext'].CommandHandler = MockCommandHandler
        sys.modules['telegram.ext'].CallbackQueryHandler = MockCallbackQueryHandler
        sys.modules['telegram.ext'].ConversationHandler = MockConversationHandler
        
        return "Applied Python 3.12 compatibility fixes for python-telegram-bot"
    
    return "No compatibility issues detected"

def import_module_from_file(module_path):
    """Import a module from a file path."""
    module_name = os.path.basename(module_path).replace(".py", "")
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_test_module(module_path):
    """Run tests from a specific module."""
    logger.info(f"Running tests from: {module_path}")
    
    try:
        # Import module
        module = import_module_from_file(module_path)
        
        # Check if module has run_tests function
        if hasattr(module, 'run_tests'):
            start_time = time.time()
            success = module.run_tests()
            end_time = time.time()
            
            logger.info(f"Tests {'PASSED' if success else 'FAILED'} in {end_time - start_time:.2f} seconds")
            return success
        else:
            logger.warning(f"Module {module_path} does not have a run_tests function")
            return False
    except Exception as e:
        logger.error(f"Error running tests from {module_path}: {str(e)}")
        return False

def run_all_tests(test_dir="test_flows"):
    """Run all test modules in the specified directory."""
    # Get all test files
    test_files = glob.glob(os.path.join(test_dir, "test_*.py"))
    logger.info(f"Found {len(test_files)} test files in {test_dir}")
    
    # Results tracking
    results = {
        "total": len(test_files),
        "passed": 0,
        "failed": 0,
        "failed_modules": []
    }
    
    # Run each test file
    for test_file in test_files:
        logger.info(f"=" * 70)
        logger.info(f"Running tests from: {test_file}")
        logger.info(f"=" * 70)
        
        success = run_test_module(test_file)
        
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
            results["failed_modules"].append(test_file)
    
    return results

def print_results(results):
    """Print test results in a formatted way."""
    logger.info(f"\n{'=' * 70}")
    logger.info(f"TEST RESULTS SUMMARY")
    logger.info(f"{'=' * 70}")
    logger.info(f"Total Test Modules: {results['total']}")
    logger.info(f"Passed: {results['passed']}")
    logger.info(f"Failed: {results['failed']}")
    
    if results["failed"] > 0:
        logger.info(f"\nFailed Test Modules:")
        for module in results["failed_modules"]:
            logger.info(f"  - {module}")
    
    logger.info(f"{'=' * 70}")
    logger.info(f"Overall Result: {'PASSED' if results['failed'] == 0 else 'FAILED'}")
    logger.info(f"{'=' * 70}\n")

def check_dependencies():
    """Check for required dependencies and return a report."""
    dependency_report = []
    
    # Check for python-telegram-bot
    try:
        import telegram
        dependency_report.append(f"python-telegram-bot: v{telegram.__version__}")
    except (ImportError, AttributeError):
        dependency_report.append("python-telegram-bot: Not installed or version unknown")
    
    # Check for SQLAlchemy
    try:
        import sqlalchemy
        dependency_report.append(f"SQLAlchemy: v{sqlalchemy.__version__}")
    except (ImportError, AttributeError):
        dependency_report.append("SQLAlchemy: Not installed or version unknown")
    
    # Check for pycryptodome
    try:
        import Crypto
        dependency_report.append(f"pycryptodome: Found")
    except ImportError:
        dependency_report.append("pycryptodome: Not installed (optional)")
    
    # Check for hyperliquid (not required for tests but noted)
    try:
        import hyperliquid
        dependency_report.append("hyperliquid: Installed (not required for tests)")
    except ImportError:
        dependency_report.append("hyperliquid: Not installed (mocked in tests)")
    
    # Check for kraken (not required for tests but noted)
    try:
        import kraken
        dependency_report.append("kraken: Installed (not required for tests)")
    except ImportError:
        dependency_report.append("kraken: Not installed (mocked in tests)")
    
    return dependency_report

def generate_report(results, compatibility_note, dependency_report, report_file="test_report.md"):
    """Generate a markdown report of test results."""
    with open(report_file, "w") as f:
        f.write(f"# Crypto Arbitrage Bot Test Report\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"## Summary\n\n")
        f.write(f"- **Total Test Modules:** {results['total']}\n")
        f.write(f"- **Passed:** {results['passed']}\n")
        f.write(f"- **Failed:** {results['failed']}\n")
        f.write(f"- **Overall Result:** {'PASSED' if results['failed'] == 0 else 'FAILED'}\n\n")
        
        if results["failed"] > 0:
            f.write(f"## Failed Test Modules\n\n")
            for module in results["failed_modules"]:
                f.write(f"- {module}\n")
            f.write("\n")
        
        f.write(f"## Environment\n\n")
        f.write(f"- Python Version: {platform.python_version()}\n")
        f.write(f"- Platform: {platform.platform()}\n")
        f.write(f"- Working Directory: {os.getcwd()}\n\n")
        
        f.write(f"## Compatibility\n\n")
        f.write(f"- {compatibility_note}\n\n")
        
        f.write(f"## Dependencies\n\n")
        for dep in dependency_report:
            f.write(f"- {dep}\n")
        f.write("\n")
        
        f.write(f"## Notes\n\n")
        f.write("- Tests use extensive mocking to avoid external dependencies\n")
        f.write("- Python 3.12 compatibility fixes are applied automatically when needed\n")
        f.write("- Warnings about missing packages are expected and handled by mocks\n")
    
    logger.info(f"Test report generated: {report_file}")

def main():
    """Main function to run tests."""
    parser = argparse.ArgumentParser(description="Run tests for the Crypto Arbitrage Bot")
    parser.add_argument("--test-dir", default="test_flows", help="Directory containing test modules")
    parser.add_argument("--module", help="Specific test module to run")
    parser.add_argument("--report", default="test_report.md", help="Output report file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--skip-compatibility", action="store_true", help="Skip compatibility fixes")
    
    args = parser.parse_args()
    
    # Set log level based on verbosity
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Check compatibility
    if not args.skip_compatibility:
        compatibility_note = check_python_compatibility()
    else:
        compatibility_note = "Compatibility checks skipped"
    
    # Check dependencies
    dependency_report = check_dependencies()
    
    start_time = time.time()
    
    if args.module:
        # Run specific module
        success = run_test_module(args.module)
        results = {
            "total": 1,
            "passed": 1 if success else 0,
            "failed": 0 if success else 1,
            "failed_modules": [] if success else [args.module]
        }
    else:
        # Run all tests
        results = run_all_tests(args.test_dir)
    
    end_time = time.time()
    logger.info(f"Total test time: {end_time - start_time:.2f} seconds")
    
    # Print results
    print_results(results)
    
    # Generate report
    if args.report:
        generate_report(results, compatibility_note, dependency_report, args.report)
    
    # Return success if all tests passed
    return results["failed"] == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 