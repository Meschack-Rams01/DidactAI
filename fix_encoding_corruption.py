#!/usr/bin/env python3
"""
Fix UTF-8 encoding corruption in DidactAI project files.
This script fixes common corrupted character sequences that appear when UTF-8 
text is incorrectly decoded/encoded.
"""

import os
import re
import shutil
from pathlib import Path

# Common UTF-8 corruption patterns and their fixes
CORRUPTION_FIXES = {
    # Checkmarks and X marks
    '✓': '✓',
    '✗': '✗', 
    '✓': '✓',
    '✓—': '✗',
    
    # Quotes and apostrophes  
    '✓€œ': '"',
    '✓€': '"', 
    '✓€™': "'",
    '✓€˜': "'",
    
    # Dashes
    '✓€"': '–',
    '✓€"': '—',
    
    # Other common symbols
    '✓€¢': '•',
    '✓€¦': '…',
    '': '',  # Often unwanted non-breaking space
    
    # Currency and symbols
    '✓‚¬': '€',
    '£': '£',
    '©': '©',
    '®': '®',
}

def should_skip_file(file_path):
    """Check if file should be skipped (binary files, etc.)"""
    skip_extensions = {
        '.pyc', '.pyo', '.jpg', '.jpeg', '.png', '.gif', '.pdf', '.docx', 
        '.xlsx', '.zip', '.tar', '.gz', '.exe', '.dll', '.so', '.db', '.sqlite3'
    }
    
    skip_dirs = {
        '__pycache__', '.git', 'node_modules', '.venv', 'venv', 'staticfiles',
        '.pytest_cache', 'migrations'
    }
    
    # Check extension
    if file_path.suffix.lower() in skip_extensions:
        return True
        
    # Check if in skip directory
    for part in file_path.parts:
        if part in skip_dirs:
            return True
            
    return False

def fix_file_encoding(file_path):
    """Fix encoding corruption in a single file"""
    try:
        # Read file with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Check if file needs fixing
        original_content = content
        
        # Apply all corruption fixes
        for corrupted, fixed in CORRUPTION_FIXES.items():
            content = content.replace(corrupted, fixed)
        
        # Only write if changes were made
        if content != original_content:
            # Create backup
            backup_path = str(file_path) + '.backup'
            shutil.copy2(file_path, backup_path)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                f.write(content)
            
            print(f"✓ Fixed: {file_path}")
            
            # Count changes
            changes = 0
            for corrupted, fixed in CORRUPTION_FIXES.items():
                changes += original_content.count(corrupted)
            
            print(f"  → Applied {changes} fixes")
            return True
        
        return False
        
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix encoding corruption"""
    print("🔧 DidactAI Encoding Corruption Fix")
    print("=" * 50)
    
    project_root = Path.cwd()
    print(f"Scanning project: {project_root}")
    
    files_processed = 0
    files_fixed = 0
    
    # Walk through all files in project
    for file_path in project_root.rglob('*'):
        if file_path.is_file() and not should_skip_file(file_path):
            files_processed += 1
            
            if fix_file_encoding(file_path):
                files_fixed += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Encoding fix complete!")
    print(f"📁 Files processed: {files_processed}")
    print(f"🔧 Files fixed: {files_fixed}")
    
    if files_fixed > 0:
        print("\n⚠️  Backup files created with .backup extension")
        print("💡 Test the application and remove backups if everything works correctly:")
        print("   find . -name '*.backup' -delete")

if __name__ == "__main__":
    main()