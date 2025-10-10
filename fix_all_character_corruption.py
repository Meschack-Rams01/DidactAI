#!/usr/bin/env python3
"""
Comprehensive character corruption fixer for DidactAI.

This script fixes all types of character corruption issues including:
1. Left arrow (←) corruption in navigation links
2. Bullet points (•) corruption in lists
3. Special icon corruption () in buttons and UI elements
4. Other common UTF-8 double encoding issues
"""

import os
import sys
import re
from pathlib import Path
import codecs

def fix_corrupted_characters(content):
    """Fix corrupted Unicode characters in content."""
    
    # First apply specific replacements for known issues
    replacements = {
        # Left arrow corruptions
        '&larr;': '&larr;',         # Common left arrow corruption
        '&larr;': '&larr;',         # Another left arrow variant
        
        # Button text corruptions ( Enhanced Export)
        '': '',              # Remove corruption before "Enhanced Export"
        '': '',              # Another variant
        
        # Bullet point corruptions
        '&bull;': '&bull;',        # Bullet point corruption
        
        # Double encoding issues
        '': '',             # UTF-8 double encoding
        '': '',               # Common double encoding
        '': '',                # Non-breaking space corruption
        
        # Quote and punctuation corruptions
        ''': "'",             # Right single quotation mark
        '"': '"',             # Left double quotation mark
        '"': '"',              # Right double quotation mark variant
        '""': '-',             # En dash
        '""': '—',             # Em dash
        '"¦': '...',           # Horizontal ellipsis
    }
    
    fixed_content = content
    changes_made = []
    
    # Apply specific replacements
    for corrupted, fixed in replacements.items():
        if corrupted in fixed_content:
            count = fixed_content.count(corrupted)
            fixed_content = fixed_content.replace(corrupted, fixed)
            changes_made.append(f"Replaced '{corrupted}' with '{fixed}' ({count} occurrences)")
    
    # Apply general regex patterns for "" type corruptions in buttons/labels
    patterns = [
        # Pattern for " Enhanced Export" and similar button texts
        (r'(ö|Ã¶|o)[\u0080-\u00FF][ZT"\']?\s*(Enhanced|Export)', r' \2'),
        
        # Pattern for other common corruption sequences (3+ non-ASCII chars together)
        (r'[\u0080-\u00FF]{3,}', ''),
        
        # Pattern for common UTF-8 double encoding patterns
        (r'‚¬[Å¾\'"""]', ''),
    ]
    
    # Apply regex patterns
    for pattern, replacement in patterns:
        original = fixed_content
        fixed_content = re.sub(pattern, replacement, fixed_content)
        if original != fixed_content:
            changes_made.append(f"Applied pattern '{pattern}' → '{replacement}'")
    
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

def fix_all_files(base_dir):
    """Fix character corruption in all files."""
    base_path = Path(base_dir)
    
    # File patterns to check
    patterns = [
        '**/*.html', '**/*.htm', '**/*.css', '**/*.js',
        '**/*.txt', '**/*.md', '**/*.py', '**/*.json'
    ]
    
    fixed_files = []
    total_files = 0
    
    print("🔍 Scanning for character corruption issues...")
    
    for pattern in patterns:
        for file_path in base_path.rglob(pattern):
            # Skip certain directories
            if any(skip in str(file_path) for skip in ['.git', 'node_modules', '.venv', 'venv', '__pycache__']):
                continue
                
            total_files += 1
            
            if total_files % 50 == 0:
                print(f"  Processed {total_files} files...")
                
            changes_made = process_file(file_path)
            
            if changes_made:
                print(f"\n✅ Fixed {file_path}:")
                for change in changes_made[:5]:  # Show up to 5 changes per file
                    print(f"   - {change}")
                if len(changes_made) > 5:
                    print(f"   - and {len(changes_made) - 5} more changes...")
                fixed_files.append((str(file_path), changes_made))
    
    return fixed_files, total_files

def clear_django_cache():
    """Clear Django template cache and compiled Python files."""
    cache_cleared = []
    
    # Clear __pycache__ directories
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                for file in os.listdir(pycache_path):
                    file_path = os.path.join(pycache_path, file)
                    os.remove(file_path)
                cache_cleared.append(pycache_path)
                print(f"Cleared cache: {pycache_path}")
            except Exception as e:
                print(f"Warning: Could not fully clear {pycache_path}: {e}")
    
    return cache_cleared

def main():
    """Main function."""
    print("🔧 Comprehensive Character Corruption Fixer for DidactAI")
    print("=" * 60)
    
    # Get the current directory (should be the Django project root)
    project_root = Path(__file__).parent
    
    print(f"Scanning directory: {project_root}")
    print()
    
    # Step 1: Clear Django cache
    print(f"\n📋 Step 1: Clearing Django cache")
    print("-" * 40)
    cache_cleared = clear_django_cache()
    print(f"Cache directories cleared: {len(cache_cleared)}")
    
    # Step 2: Fix character corruption
    print(f"\n📋 Step 2: Fixing character corruption")
    print("-" * 40)
    fixed_files, total_files = fix_all_files(project_root)
    
    print(f"\n📊 Summary:")
    print(f"Total files checked: {total_files}")
    print(f"Files with corruption fixed: {len(fixed_files)}")
    
    if fixed_files:
        print(f"\n🎉 Successfully fixed character corruption in {len(fixed_files)} files!")
        print("\n🔧 Top 10 fixed files:")
        for file_path, changes in fixed_files[:10]:
            print(f"  - {file_path} ({len(changes)} changes)")
        
        if len(fixed_files) > 10:
            print(f"  - And {len(fixed_files) - 10} more files...")
        
        print("\n💡 Next steps:")
        print("1. Restart the Django server: python manage.py runserver")
        print("2. Clear browser cache completely (Ctrl+Shift+Delete)")
        print("3. Hard refresh the browser (Ctrl+F5)")
        
    else:
        print("\n✅ No character corruption found!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())