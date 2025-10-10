#!/usr/bin/env python3
"""
Fix character corruption issues in Django templates.

This script finds and fixes common Unicode character corruption issues
like corrupted arrows, bullet points, and other symbols.
"""

import os
import sys
import re
from pathlib import Path

def fix_corrupted_characters(content):
    """Fix corrupted Unicode characters in content."""
    replacements = {
        # Corrupted left arrow variations
        '←': '←',      # ←
        '←': '←',              # ← (different encoding)
        '←': '←',             # ← (what user sees)
        
        # Corrupted bullet points
        '&bull;': '&bull;',            # &bull; 
        
        # Common question mark corruptions (fallback)
        '???': '←',            # Sometimes shows as ???
    }
    
    fixed_content = content
    changes_made = []
    
    for corrupted, fixed in replacements.items():
        if corrupted in fixed_content:
            fixed_content = fixed_content.replace(corrupted, fixed)
            changes_made.append(f"'{corrupted}' → '{fixed}'")
    
    return fixed_content, changes_made

def process_file(file_path):
    """Process a single file for character corruption."""
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Fix corrupted characters
        fixed_content, changes_made = fix_corrupted_characters(original_content)
        
        # Write back if changes were made
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return changes_made
        
        return []
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []

def fix_all_templates(base_dir):
    """Fix character corruption in all template files."""
    base_path = Path(base_dir)
    
    # File patterns to check
    patterns = ['**/*.html', '**/*.htm', '**/*.txt', '**/*.md']
    
    fixed_files = []
    total_files = 0
    
    print("🔍 Scanning for character corruption issues...")
    
    for pattern in patterns:
        for file_path in base_path.rglob(pattern):
            # Skip certain directories
            if any(skip in str(file_path) for skip in ['.git', 'node_modules', '.venv', 'venv', '__pycache__']):
                continue
                
            total_files += 1
            changes_made = process_file(file_path)
            
            if changes_made:
                print(f"\n✅ Fixed {file_path}:")
                for change in changes_made:
                    print(f"   {change}")
                fixed_files.append((str(file_path), changes_made))
    
    return fixed_files, total_files

def main():
    """Main function."""
    print("🔧 Character Corruption Fixer for DidactAI")
    print("=" * 50)
    
    # Get the current directory (should be the Django project root)
    project_root = Path(__file__).parent
    
    print(f"Scanning directory: {project_root}")
    print()
    
    # Fix character corruption
    fixed_files, total_files = fix_all_templates(project_root)
    
    print(f"\n📊 Summary:")
    print(f"Total files checked: {total_files}")
    print(f"Files with corruption fixed: {len(fixed_files)}")
    
    if fixed_files:
        print(f"\n🎉 Successfully fixed character corruption in {len(fixed_files)} files!")
        print("\n🔧 Files fixed:")
        for file_path, changes in fixed_files:
            print(f"  - {file_path} ({len(changes)} corrections)")
        
        print("\n💡 Next steps:")
        print("1. Refresh your browser (Ctrl+F5)")
        print("2. The characters should now display correctly")
        print("3. If issues persist, clear browser cache completely")
        
    else:
        print("\n✅ No character corruption found!")
        print("💡 If you still see strange characters:")
        print("   - Clear browser cache completely")
        print("   - Restart Django server")
        print("   - Check for JavaScript-generated content")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())