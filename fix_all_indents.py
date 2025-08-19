#!/usr/bin/env python3
"""
Script to fix Python indentation issues.
This is more thorough than fix_indentation.sh as it uses Python's AST parsing.
"""

import ast
import sys
import os
import argparse
import autopep8
import shutil
from pathlib import Path

def fix_file_indentation(file_path):
    """
    Fix indentation in a Python file using AST parsing and autopep8.
    This is a two-step process:
    1. Check if the file is syntactically valid Python
    2. If valid, use autopep8 to fix style issues
    3. If not valid, make a backup and attempt to fix common indentation issues
    """
    print(f"Processing {file_path}...")
    
    # Create backup
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    print(f"Created backup at {backup_path}")
    
    # Try to parse the file with AST to check for syntax errors
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
        print(f"File is valid Python. Using autopep8 for style fixes...")
        
        # File is valid Python, use autopep8 to fix style
        result = autopep8.fix_file(
            file_path,
            options={
                'aggressive': 2,
                'indent_size': 4,
                'max_line_length': 100
            }
        )
        
        # Write the result back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result)
            
        print(f"Successfully fixed indentation in {file_path}")
        return True
        
    except SyntaxError as e:
        print(f"SyntaxError in {file_path}: {e}")
        print("Attempting manual fixes for common issues...")
        
        # File has syntax errors, try a more manual approach
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Convert tabs to spaces
            for i in range(len(lines)):
                lines[i] = lines[i].replace('\t', '    ')
            
            # Write the changes back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
                
            print(f"Manual fixes applied. Running autopep8 for further corrections...")
            
            # Try autopep8 again
            result = autopep8.fix_file(
                file_path,
                options={
                    'aggressive': 2,
                    'indent_size': 4,
                    'max_line_length': 100
                }
            )
            
            # Write the result back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result)
                
            print(f"Successfully applied corrections to {file_path}")
            
            # Verify the file is now valid
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                ast.parse(source)
                print(f"File is now valid Python! Indentation appears fixed.")
                return True
            except SyntaxError as e2:
                print(f"File still has syntax errors after corrections: {e2}")
                print(f"Manual inspection and fixes may be needed.")
                return False
                
        except Exception as e:
            print(f"Error during manual fixes: {e}")
            return False
    
    except Exception as e:
        print(f"Unexpected error processing {file_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Fix Python indentation issues')
    parser.add_argument('files', nargs='+', help='Python files to process')
    args = parser.parse_args()
    
    success_count = 0
    fail_count = 0
    
    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found")
            fail_count += 1
            continue
            
        if not file_path.endswith('.py'):
            print(f"Warning: {file_path} does not appear to be a Python file")
            
        if fix_file_indentation(file_path):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\nSummary: {success_count} files fixed successfully, {fail_count} files with errors")
    
if __name__ == "__main__":
    main() 