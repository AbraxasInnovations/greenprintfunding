#!/usr/bin/env python3
"""
Test script that checks for basic syntax errors in Python files without importing them.
"""

import ast
import os
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def check_syntax(file_path):
    """Check Python file for syntax errors without importing/executing."""
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False

        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse the file to check for syntax errors
        try:
            ast.parse(source)
            logger.info(f"Syntax check passed for {file_path}")
            return True
        except SyntaxError as e:
            logger.error(f"Syntax error in {file_path} at line {e.lineno}, column {e.offset}: {e.msg}")
            return False
            
    except Exception as e:
        logger.error(f"Error checking {file_path}: {str(e)}")
        return False

def main():
    """Run syntax checks on critical files."""
    logger.info("Starting syntax checks...")
    
    # Define files to test
    files_to_test = [
        "telegram_bot.py",
        "arb_bot.py",
        "bot_service.py"
    ]
    
    # Test each file
    success_count = 0
    for file_path in files_to_test:
        try:
            if check_syntax(file_path):
                success_count += 1
        except Exception as e:
            logger.error(f"Unexpected error testing {file_path}: {str(e)}")
    
    # Report results
    logger.info(f"Tests completed. {success_count}/{len(files_to_test)} files passed.")
    
    if success_count == len(files_to_test):
        logger.info("✅ All files passed syntax checking!")
    else:
        logger.warning(f"⚠️ {len(files_to_test) - success_count} files failed syntax checking.")

if __name__ == "__main__":
    main() 