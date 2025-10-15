#!/usr/bin/env python3
"""
Ultimate character corruption fixer for all Django templates.

This script fixes ALL types of character corruption issues in one go:
- BOM (Byte Order Mark) issues
- Left/right arrow corruptions  
- Bullet point corruptions
- Emoji corruptions (document, clipboard, etc.)
- Double encoding issues
- Question mark sequences
- Special character corruptions
"""

import os
import sys
import re
from pathlib import Path
import codecs

def remove_bom(content):
    """Remove BOM from content if present."""
    if content.startswith(codecs.BOM_UTF8.decode('utf-8')):
        return content[1:]
    return content

def fix_all_corruptions(content):
    """Fix all types of character corruptions in content."""
    
    # Remove BOM first
    content = remove_bom(content)
    
    changes_made = []
    
    # Dictionary of specific character replacements
    replacements = {
        # Arrow corruptions
        '✓†': '←',           # Left arrow corruption
        'à¤': '←',           # Another left arrow variant
        '✓†'': '→',          # Right arrow corruption
        
        # Bullet point corruptions  
        '"¢': '•',          # Bullet point corruption
        '&bull;': '•',       # HTML entity to actual bullet
        
        # Emoji corruptions - document/file icons
        '📈„': '📄',        # Document emoji
        '📈‹': '📋',        # Clipboard emoji
        'Ã°Å¸""ž': '📄',   # Complex document corruption
        'Ã°Å¸""‹': '📋',   # Complex clipboard corruption
        
        # Enhanced Export button corruptions
        'öŸZ': '',           # Remove "öŸZ" corruption
        'öŸ"': '',           # Remove "öŸ"" corruption
        'öŸZ Enhanced': 'Enhanced',  # Clean Enhanced text
        'öŸ" Enhanced': 'Enhanced',  # Clean Enhanced text
        
        # Quote corruptions
        '"': '"',          # Left double quote
        '"\x9d': '"',       # Right double quote
        ''': "'",          # Right single quote
        '"˜': "'",          # Left single quote
        
        # Dash corruptions
        '""': '—',          # Em dash
        '""': '–',          # En dash
        
        # Other common corruptions
        '"¦': '…',          # Ellipsis
        '': '',             # Non-breaking space corruption
        'ö': 'ö',          # o with umlaut
        'Ã¢': '✓',          # a with circumflex
        'é': 'é',          # e with acute
        'Ã ': 'à',          # a with grave
        'ü': 'ü',          # u with umlaut
        
        # Remove corrupted sequences before common words
        'Ã': '',            # Double encoding corruption
        'Ã¢✓‚¬': '',         # Complex corruption pattern
        '✓‚¬': '',           # Euro symbol corruption
    }
    
    # Apply specific replacements
    original_content = content
    for corrupted, fixed in replacements.items():
        if corrupted in content:
            count = content.count(corrupted)
            content = content.replace(corrupted, fixed)
            changes_made.append(f"'{corrupted}' → '{fixed}' ({count}x)")
    
    # Regex patterns for complex corruptions
    patterns = [
        # Fix question mark sequences before Export/Enhanced/Quick
        (r'\?{2,}\s*(Export|Enhanced|Quick)', r'📄 \1'),
        
        # Fix corrupted sequences before Export buttons
        (r'[^\w\s]{3,}\s*(Export to PDF)', r'📄 \1'),
        (r'[^\w\s]{3,}\s*(Quick Export)', r'📋 \1'),
        (r'[^\w\s]{3,}\s*(Enhanced Export)', r'📄 \1'),
        
        # Remove standalone non-ASCII sequences (3+ chars)
        (r'[\x80-\xFF]{3,}', ''),
        
        # Clean up corrupted Unicode sequences
        (r'[Ã][^\w\s][^\w\s]', ''),
        
        # Fix corrupted arrows in "Back to Home"
        (r'[^\w\s]{2,}\s*Back to Home', r'← Back to Home'),
        
        # Remove corruption before common button text
        (r'[^\w\s<>="\'\-]{2,}\s*(Enhanced|Export|Quick|Back)', r'\1'),
    ]
    
    # Apply regex patterns
    for pattern, replacement in patterns:
        original = content
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        if original != content:
            changes_made.append(f"Pattern '{pattern[:20]}...' applied")
    
    return content, changes_made

def process_file(file_path):
    """Process a single file to fix corruption."""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Fix all corruptions
        fixed_content, changes_made = fix_all_corruptions(original_content)
        
        # Write back if changes were made
        if changes_made:
            with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(fixed_content)
            return changes_made
        
        return []
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return []

def fix_all_template_files(base_dir):
    """Fix corruption in all template files."""
    base_path = Path(base_dir)
    
    # File patterns to check
    patterns = ['**/*.html', '**/*.htm']
    
    fixed_files = []
    total_files = 0
    
    print("🔍 Scanning all HTML template files...")
    
    for pattern in patterns:
        for file_path in base_path.rglob(pattern):
            # Skip certain directories
            skip_dirs = ['.git', 'node_modules', '.venv', 'venv', '__pycache__', 'staticfiles']
            if any(skip in str(file_path) for skip in skip_dirs):
                continue
                
            total_files += 1
            
            if total_files % 25 == 0:
                print(f"  Processed {total_files} files...")
                
            changes_made = process_file(file_path)
            
            if changes_made:
                print(f"\n✅ Fixed {file_path.name}:")
                for change in changes_made[:3]:  # Show first 3 changes
                    print(f"   - {change}")
                if len(changes_made) > 3:
                    print(f"   - and {len(changes_made) - 3} more fixes...")
                fixed_files.append((str(file_path), changes_made))
    
    return fixed_files, total_files

def clear_cache():
    """Clear Django cache directories."""
    cache_cleared = 0
    
    # Clear __pycache__ directories
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                import shutil
                shutil.rmtree(pycache_path)
                cache_cleared += 1
            except Exception as e:
                print(f"⚠️  Could not clear {pycache_path}: {e}")
    
    return cache_cleared

def main():
    """Main function."""
    print("🚀 ULTIMATE Template Corruption Fixer for DidactAI")
    print("=" * 60)
    print("Fixing ALL character corruption issues in templates...")
    print()
    
    # Get the project root
    project_root = Path(__file__).parent
    
    # Step 1: Clear cache
    print("📋 Step 1: Clearing Django cache")
    print("-" * 30)
    cache_cleared = clear_cache()
    print(f"Cleared {cache_cleared} cache directories")
    
    # Step 2: Fix template files
    print(f"\n📋 Step 2: Fixing template corruption")
    print("-" * 30)
    fixed_files, total_files = fix_all_template_files(project_root)
    
    # Summary
    print(f"\n🎯 FINAL RESULTS:")
    print("=" * 40)
    print(f"📊 Total HTML files checked: {total_files}")
    print(f"🔧 Files with corruption fixed: {len(fixed_files)}")
    print(f"🗂️  Cache directories cleared: {cache_cleared}")
    
    if fixed_files:
        print(f"\n🎉 SUCCESS! Fixed corruption in {len(fixed_files)} files!")
        print("\n📁 Fixed files:")
        for file_path, changes in fixed_files[:10]:  # Show first 10
            filename = Path(file_path).name
            print(f"  ✓ {filename} ({len(changes)} fixes)")
        
        if len(fixed_files) > 10:
            print(f"  ... and {len(fixed_files) - 10} more files")
        
        print(f"\n🚀 NEXT STEPS:")
        print("1. Restart Django server: python manage.py runserver")
        print("2. Clear browser cache: Ctrl+Shift+Delete")
        print("3. Hard refresh pages: Ctrl+F5")
        print("4. All character corruption should be FIXED! ✅")
        
    else:
        print(f"\n✅ No corruption found - templates are clean!")
        
    print(f"\n🎊 Character corruption fix COMPLETE!")
    return 0

if __name__ == "__main__":
    sys.exit(main())