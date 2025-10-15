#!/usr/bin/env python3
"""
Fix emoji and special character corruption in templates.

This script specifically targets corrupted emoji and special characters
that appear as question marks or other corrupted symbols.
"""

import os
import sys
import re
from pathlib import Path

def fix_emoji_corruption(content):
    """Fix corrupted emoji and special characters in content."""
    
    # Specific fixes for known corrupted patterns
    replacements = {
        # PDF/Document emoji corruption
        '📈„': '📄',       # Document emoji
        '📈‹': '📋',       # Clipboard emoji  
        '????': '📄',      # Multiple question marks to document emoji
        '????????': '📄',  # Many question marks to document emoji
        '?????????': '📄', # Even more question marks
        '??????????': '📄', # Excessive question marks
        
        # Common emoji corruptions
        '🚀': '🚀',       # Rocket emoji
        '🍎¯': '🎯',       # Target emoji
        '✅': '✅',       # Check mark
        'â¤ï¸': '❤️',      # Heart
        '📈¥': '🔥',       # Fire emoji
        'ðŸ'¡': '💡',       # Light bulb
        'â›½': '⛽',       # Fuel emoji
        '📈': '🔧',        # Wrench
        'ðŸ› ï¸': '🛠️',      # Hammer and wrench
        
        # Arrow corruptions (additional patterns)
        '←': '←',         # Left arrow (in case it's still corrupted)
        '→': '→',         # Right arrow
        '↑': '↑',         # Up arrow
        '↓': '↓',         # Down arrow
        
        # Special character corruptions in button text
        '• Enhanced': ' Enhanced',     # Remove bullet before Enhanced
        '•Enhanced': ' Enhanced',      # Remove bullet before Enhanced (no space)
        '⭐ Enhanced': ' Enhanced',    # Remove star before Enhanced
    }
    
    fixed_content = content
    changes_made = []
    
    # Apply specific replacements
    for corrupted, fixed in replacements.items():
        if corrupted in fixed_content:
            count = fixed_content.count(corrupted)
            fixed_content = fixed_content.replace(corrupted, fixed)
            changes_made.append(f"'{corrupted}' → '{fixed}' ({count} times)")
    
    # Fix patterns with regex
    patterns = [
        # Fix sequences of 3+ question marks followed by export text
        (r'\?{3,}\s*(Export|Enhanced)', r'📄 \1'),
        
        # Fix random question mark sequences in button text
        (r'\?+\s*(Export to PDF)', r'📄 \1'),
        (r'\?+\s*(Quick Export)', r'📋 \1'),
        
        # Remove standalone question marks before known button text
        (r'\?\s*(Export|Enhanced|Quick)', r'\1'),
        
        # Fix corrupted unicode patterns (non-printable chars before text)
        (r'[\x00-\x1F\x80-\xFF]{2,}\s*(Export|Enhanced)', r'📄 \1'),
    ]
    
    # Apply regex patterns
    for pattern, replacement in patterns:
        original = fixed_content
        fixed_content = re.sub(pattern, replacement, fixed_content, flags=re.MULTILINE)
        if original != fixed_content:
            changes_made.append(f"Pattern '{pattern}' → '{replacement}'")
    
    return fixed_content, changes_made

def process_file(file_path):
    """Process a single file for emoji corruption."""
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Fix corrupted characters
        fixed_content, changes_made = fix_emoji_corruption(original_content)
        
        # Write back if changes were made
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return changes_made
        
        return []
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []

def main():
    """Main function."""
    print("🔧 Emoji and Special Character Corruption Fixer")
    print("=" * 50)
    
    # Focus on template files
    base_path = Path(__file__).parent / "templates"
    
    fixed_files = []
    total_files = 0
    
    print(f"Scanning templates directory: {base_path}")
    
    # Process all HTML files in templates
    for file_path in base_path.rglob("*.html"):
        total_files += 1
        changes_made = process_file(file_path)
        
        if changes_made:
            print(f"\n✅ Fixed {file_path}:")
            for change in changes_made:
                print(f"   - {change}")
            fixed_files.append((str(file_path), changes_made))
    
    print(f"\n📊 Summary:")
    print(f"Total template files checked: {total_files}")
    print(f"Files with emoji corruption fixed: {len(fixed_files)}")
    
    if fixed_files:
        print(f"\n🎉 Successfully fixed emoji corruption in {len(fixed_files)} files!")
        print("\n💡 Next steps:")
        print("1. Hard refresh browser (Ctrl+F5)")
        print("2. Check the Enhanced Export buttons should show proper icons")
    else:
        print(f"\n✅ No emoji corruption found!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())