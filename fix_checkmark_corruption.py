#!/usr/bin/env python
"""
Fix corrupted checkmarks throughout DidactAI project
Replaces corrupted "✓ with clean "✓
"""
import os
import re

def fix_checkmarks_in_file(file_path):
    """Fix corrupted checkmarks in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace corrupted checkmarks
        corrupted_patterns = [
            '✓',  # Most common corruption
            '✓',   # Another variant
            '✓',   # Without the quote
        ]
        
        original_content = content
        for pattern in corrupted_patterns:
            content = content.replace(pattern, '✓')
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def fix_checkmarks_in_directory(directory):
    """Fix corrupted checkmarks in all files in directory"""
    fixed_files = []
    
    # File extensions to check
    extensions = ['.html', '.py', '.js', '.css', '.md', '.txt']
    
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        skip_dirs = ['__pycache__', '.git', 'node_modules', 'venv', 'env', '.vscode']
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                if fix_checkmarks_in_file(file_path):
                    fixed_files.append(file_path)
    
    return fixed_files

def main():
    """Main function to fix checkmarks"""
    print("=== Fixing Corrupted Checkmarks in DidactAI ===\n")
    
    current_dir = os.getcwd()
    print(f"Scanning directory: {current_dir}")
    
    fixed_files = fix_checkmarks_in_directory(current_dir)
    
    if fixed_files:
        print(f"\n✅ Fixed corrupted checkmarks in {len(fixed_files)} files:")
        for file_path in fixed_files:
            relative_path = os.path.relpath(file_path, current_dir)
            print(f"  - {relative_path}")
    else:
        print("\n✅ No corrupted checkmarks found or all already fixed!")
    
    print(f"\n=== Checkmark Fix Complete ===")

if __name__ == '__main__':
    main()