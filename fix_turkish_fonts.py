#!/usr/bin/env python
"""
Fix Turkish character support in PDF export by updating font references
"""

import re

def fix_font_references():
    file_path = r'C:\Users\Ramat\Desktop\DidactAI_Template\exports\services.py'
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace Times font references with Unicode-compatible fonts
    replacements = [
        (r"fontName='Times-Roman'", "fontName=getattr(self, 'unicode_font_normal', 'Helvetica')"),
        (r"fontName='Times-Bold'", "fontName=getattr(self, 'unicode_font_bold', 'Helvetica-Bold')"),
    ]
    
    for old, new in replacements:
        content = re.sub(old, new, content)
        print(f"Replaced: {old} -> {new}")
    
    # Write back the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Font references updated for Turkish character support")

if __name__ == "__main__":
    fix_font_references()
