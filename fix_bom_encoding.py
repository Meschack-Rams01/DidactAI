#!/usr/bin/env python3
"""
Fix BOM (Byte Order Mark) encoding issues in Django template files.

This script removes the BOM from HTML template files that are causing
character encoding issues in the browser.
"""

import os
import sys
from pathlib import Path
import codecs

def remove_bom_from_file(file_path):
    """Remove BOM from a single file."""
    try:
        # Read the file with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        # Write back without BOM
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def has_bom(file_path):
    """Check if a file has BOM."""
    try:
        with open(file_path, 'rb') as f:
            first_bytes = f.read(3)
            return first_bytes == codecs.BOM_UTF8
    except:
        return False

def fix_template_files(base_dir):
    """Fix all template files in the project."""
    base_path = Path(base_dir)
    
    # File patterns to check
    patterns = ['**/*.html', '**/*.htm']
    
    fixed_files = []
    total_files = 0
    
    for pattern in patterns:
        for file_path in base_path.rglob(pattern):
            total_files += 1
            
            if has_bom(file_path):
                print(f"Found BOM in: {file_path}")
                if remove_bom_from_file(file_path):
                    fixed_files.append(str(file_path))
                    print(f"✅ Fixed: {file_path}")
                else:
                    print(f"❌ Failed to fix: {file_path}")
    
    print(f"\n📊 Summary:")
    print(f"Total HTML files checked: {total_files}")
    print(f"Files with BOM found and fixed: {len(fixed_files)}")
    
    if fixed_files:
        print(f"\n🔧 Fixed files:")
        for file_path in fixed_files:
            print(f"  - {file_path}")
    else:
        print(f"\n✅ No BOM issues found!")
    
    return fixed_files

def main():
    """Main function."""
    print("🔍 Django Template BOM Fixer")
    print("=" * 50)
    
    # Get the current directory (should be the Django project root)
    project_root = Path(__file__).parent
    
    print(f"Scanning directory: {project_root}")
    print()
    
    # Fix template files
    fixed_files = fix_template_files(project_root)
    
    if fixed_files:
        print(f"\n🎉 Successfully fixed {len(fixed_files)} files!")
        print("You should now see proper characters in your web pages.")
        print("\nRecommendation: Restart your Django development server.")
    else:
        print("\n✅ No BOM encoding issues found in your template files.")

if __name__ == "__main__":
    main()