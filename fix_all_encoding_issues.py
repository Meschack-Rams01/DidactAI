#!/usr/bin/env python3
"""
Complete encoding issue fixer for DidactAI.

This script:
1. Removes BOM from all HTML files
2. Checks Django template cache
3. Provides browser cache clearing instructions
"""

import os
import sys
import shutil
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

def clear_django_cache():
    """Clear Django template cache and compiled Python files."""
    cache_cleared = []
    
    # Clear __pycache__ directories
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(pycache_path)
                cache_cleared.append(pycache_path)
            except Exception as e:
                print(f"Warning: Could not remove {pycache_path}: {e}")
    
    return cache_cleared

def fix_all_html_files(base_dir):
    """Fix all HTML files in all directories."""
    base_path = Path(base_dir)
    
    # File patterns to check
    patterns = ['**/*.html', '**/*.htm']
    
    fixed_files = []
    total_files = 0
    
    print("🔍 Scanning all directories for HTML files...")
    
    for pattern in patterns:
        for file_path in base_path.rglob(pattern):
            # Skip certain directories
            if any(skip in str(file_path) for skip in ['.git', 'node_modules', '.venv', 'venv']):
                continue
                
            total_files += 1
            
            if has_bom(file_path):
                print(f"Found BOM in: {file_path}")
                if remove_bom_from_file(file_path):
                    fixed_files.append(str(file_path))
                    print(f"✅ Fixed: {file_path}")
                else:
                    print(f"❌ Failed to fix: {file_path}")
    
    return fixed_files, total_files

def main():
    """Main function."""
    print("🚀 Complete Encoding Issue Fixer for DidactAI")
    print("=" * 60)
    
    # Get the current directory (should be the Django project root)
    project_root = Path(__file__).parent
    
    print(f"Scanning directory: {project_root}")
    print()
    
    # Step 1: Fix HTML files
    print("📋 Step 1: Fixing BOM in HTML files")
    print("-" * 40)
    fixed_files, total_files = fix_all_html_files(project_root)
    
    print(f"\n📊 HTML Files Summary:")
    print(f"Total HTML files checked: {total_files}")
    print(f"Files with BOM found and fixed: {len(fixed_files)}")
    
    # Step 2: Clear Django cache
    print(f"\n📋 Step 2: Clearing Django cache")
    print("-" * 40)
    cache_cleared = clear_django_cache()
    print(f"Cache directories cleared: {len(cache_cleared)}")
    
    # Step 3: Browser cache instructions
    print(f"\n📋 Step 3: Clear Browser Cache")
    print("-" * 40)
    print("To completely resolve encoding issues, clear your browser cache:")
    print("\n🌐 Chrome/Edge:")
    print("   - Press Ctrl+Shift+Delete")
    print("   - Select 'All time' and check all boxes")
    print("   - Click 'Clear data'")
    print("\n🦊 Firefox:")
    print("   - Press Ctrl+Shift+Delete")
    print("   - Select 'Everything' and check all boxes")
    print("   - Click 'Clear Now'")
    print("\n🔄 Alternative: Hard refresh")
    print("   - Press Ctrl+F5 while on the page")
    print("   - Or Ctrl+Shift+R")
    
    # Step 4: Django server restart instructions
    print(f"\n📋 Step 4: Restart Django Server")
    print("-" * 40)
    print("After fixing encoding issues:")
    print("1. Stop the Django development server (Ctrl+C)")
    print("2. Restart it with: python manage.py runserver")
    print("3. Clear browser cache or hard refresh (Ctrl+F5)")
    
    # Final summary
    print(f"\n🎉 Summary:")
    if fixed_files:
        print(f"✅ Fixed {len(fixed_files)} files with BOM issues")
        print(f"✅ Cleared {len(cache_cleared)} cache directories")
        print("⚠️  Browser cache clearing required for full fix")
        print("⚠️  Django server restart recommended")
        
        print(f"\n🔧 Fixed files:")
        for file_path in fixed_files[:10]:  # Show first 10
            print(f"  - {file_path}")
        if len(fixed_files) > 10:
            print(f"  ... and {len(fixed_files) - 10} more files")
    else:
        print("✅ No BOM issues found in HTML files")
        print(f"✅ Cleared {len(cache_cleared)} cache directories")
        print("💡 If you still see encoding issues:")
        print("   - Clear browser cache (Step 3)")
        print("   - Restart Django server (Step 4)")
        print("   - Check for issues in JavaScript/CSS files")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())