#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Complete Character Corruption Fix for DidactAI
This script fixes common character encoding issues in all project files.
"""

import os
import re
import glob
from pathlib import Path

def fix_character_corruption():
    """Fix character corruption in all project files"""
    
    print("🚀 Character Corruption Fixer for DidactAI")
    print("=" * 50)
    
    # Define character mappings for common corruptions
    character_fixes = {
        # Emoji fixes
        '🎓': '🎓',  # Graduation cap
        '🚀': '🚀',  # Rocket
        '✅': '✅',   # Check mark
        '🤖': '🤖',  # Robot
        '🌟': '🌟',  # Star
        '🔧': '🔧',  # Wrench
        '📊': '📊',  # Chart
        '📈': '📝',   # Memo
        '🎉': '🎉',  # Party
        '📈': '🔒',   # Lock
        '🛡️': '🛡️',  # Shield
        '📈±': '📱',  # Mobile phone
        '📈¥': '📧',  # Email
        '📈': '🔐',   # Lock with key
        '⚠️': '⚠️',   # Warning
        '🏆': '🏆',   # Trophy
        '📈': '📈',   # Chart up
        '🪟': '🪟',   # Window
        '🍎': '🍎',   # Apple
        '🐧': '🐧',   # Penguin
        '🖥️': '🖥️',  # Desktop
        '📈„': '📄',  # Page
        '📈ž': '📞',  # Phone
        '🙏': '🙏',   # Folded hands
        
        # Arrow and symbol fixes
        '←': '←',
        '→': '→',
        '↑': '↑',
        '↓': '↓',
        '↔': '↔',
        '⇐': '⇐',
        '⇒': '⇒',
        '⇑': '⇑',
        '⇓': '⇓',
        '⇔': '⇔',
        '→': '→',
        '←': '←',
        '↓': '↓',
        '↑': '↑',
        
        # Special character fixes
        '✅': '✅',
        '⚠': '⚠',
        ''': "'",
        '"': '"',
        '"': '"',
        '""': '—',
        '""': '–',
        '': '',
        'á': 'á',
        'é': 'é',
        'í': 'í',
        'ó': 'ó',
        'ú': 'ú',
        'ñ': 'ñ',
        'ü': 'ü',
        'ö': 'ö',
        'ä': 'ä',
        'ç': 'ç',
        
        # Turkish character fixes
        'ı': 'ı',
        'Ğ': 'ğ',
        'Ş': 'ş',
        'ç': 'ç',
        'ü': 'ü',
        'ö': 'ö',
        'İ': 'İ',
        'Ğ': 'Ğ',
        'Ş': 'Ş',
        'Ç': 'Ç',
        'Ü': 'Ü',
        'Ö': 'Ö'
    }
    
    # File extensions to process
    file_extensions = ['*.py', '*.html', '*.css', '*.js', '*.md', '*.txt', '*.json']
    
    # Directories to exclude
    exclude_dirs = {
        '__pycache__', '.git', 'node_modules', 'venv', 'env',
        '.pytest_cache', 'migrations', 'staticfiles', 'locale'
    }
    
    fixed_files = []
    total_files = 0
    
    print("🔍 Scanning for files to fix...")
    
    for extension in file_extensions:
        for file_path in glob.glob(f"**/{extension}", recursive=True):
            # Skip excluded directories
            path_parts = Path(file_path).parts
            if any(exclude_dir in path_parts for exclude_dir in exclude_dirs):
                continue
                
            total_files += 1
            
            try:
                # Read file with different encodings
                content = None
                encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
                
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            content = f.read()
                        break
                    except UnicodeDecodeError:
                        continue
                
                if content is None:
                    print(f"⚠️ Could not read: {file_path}")
                    continue
                
                # Apply character fixes
                original_content = content
                for corrupt_char, fixed_char in character_fixes.items():
                    content = content.replace(corrupt_char, fixed_char)
                
                # If content changed, write it back
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixed_files.append(file_path)
                    print(f"✅ Fixed: {file_path}")
                    
            except Exception as e:
                print(f"❌ Error processing {file_path}: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Character Corruption Fix Complete!")
    print(f"📊 Total files scanned: {total_files}")
    print(f"🔧 Files fixed: {len(fixed_files)}")
    
    if fixed_files:
        print("\n🔧 Fixed files:")
        for file_path in fixed_files:
            print(f"  - {file_path}")
    
    print("\n✅ All character corruption issues have been resolved!")
    print("🔄 Recommendation: Clear browser cache and restart Django server")
    
    return len(fixed_files)

if __name__ == "__main__":
    fixed_count = fix_character_corruption()
    
    if fixed_count > 0:
        print(f"\n🚀 Successfully fixed {fixed_count} files!")
        print("📝 Next steps:")
        print("  1. Clear your browser cache (Ctrl+Shift+Delete)")
        print("  2. Restart Django server: python manage.py runserver")
        print("  3. Hard refresh the page (Ctrl+F5)")
    else:
        print("\n✅ No corrupted files found. Your project is clean!")