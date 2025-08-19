#!/usr/bin/env python3
"""
Test script that validates imports and syntax of critical files without needing a real bot token.
"""

import importlib.util
import sys
import os
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def test_import_file(file_path, module_name):
    """Test importing a file to check for syntax errors."""
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False

        # Create a module spec
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            logger.error(f"Failed to create module spec for {file_path}")
            return False

        # Create a module from the spec
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module

        # Execute the module
        try:
            spec.loader.exec_module(module)
            logger.info(f"Successfully imported {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error during import of {file_path}: {str(e)}")
            return False

    except Exception as e:
        logger.error(f"Failed to import {file_path}: {str(e)}")
        return False

def main():
    """Run tests on critical files."""
    logger.info("Starting syntax tests...")
    
    # Define files to test
    files_to_test = [
        ("telegram_bot.py", "telegram_bot_test"),
        ("arb_bot.py", "arb_bot_test"),
        ("bot_service.py", "bot_service_test")
    ]
    
    # Test each file
    success_count = 0
    for file_path, module_name in files_to_test:
        try:
            if test_import_file(file_path, module_name):
                success_count += 1
        except Exception as e:
            logger.error(f"Unexpected error testing {file_path}: {str(e)}")
    
    # Report results
    logger.info(f"Tests completed. {success_count}/{len(files_to_test)} files passed.")
    
    if success_count == len(files_to_test):
        logger.info("✅ All files passed syntax testing!")
    else:
        logger.warning(f"⚠️ {len(files_to_test) - success_count} files failed testing.")

if __name__ == "__main__":
    main() 