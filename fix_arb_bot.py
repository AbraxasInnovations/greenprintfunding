#!/usr/bin/env python3
"""
Script to fix indentation issues in arb_bot.py file
Specifically targeting the problem around line 1178
"""

import re
import sys
import shutil

def fix_indentation_issues(file_path):
    """Fix indentation issues in a Python file."""
    print(f"Processing {file_path}...")
    
    # Create backup
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    print(f"Created backup at {backup_path}")
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Fix indentation issues
    fixed_lines = []
    in_check_exit_conditions = False
    problem_fixed = False
    
    for i, line in enumerate(lines):
        # Check if we're entering the check_exit_conditions method
        if 'def check_exit_conditions' in line:
            in_check_exit_conditions = True
            fixed_lines.append(line)
            continue
        
        # Check if we're exiting the method
        if in_check_exit_conditions and re.match(r'^    def ', line):
            in_check_exit_conditions = False
            fixed_lines.append(line)
            continue
        
        # Fix the specific problematic line at around 1178
        if in_check_exit_conditions and 'asset_data = self.assets[asset]' in line:
            # Check if it has extra indentation
            indent = len(line) - len(line.lstrip())
            if indent > 8:  # Should have 8 spaces (2 indentation levels)
                fixed_line = ' ' * 8 + line.lstrip()
                fixed_lines.append(fixed_line)
                problem_fixed = True
                print(f"Fixed indentation on line {i+1}: {line.strip()}")
                continue
        
        fixed_lines.append(line)
    
    # Write the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    if problem_fixed:
        print(f"Successfully fixed indentation issues in {file_path}")
    else:
        print(f"No specific indentation issues were found or fixed in {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_arb_bot.py <file_path>")
        sys.exit(1)
    
    fix_indentation_issues(sys.argv[1]) 