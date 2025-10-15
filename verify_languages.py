#!/usr/bin/env python
"""
Simple script to verify language configuration
"""

import os
import django
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
django.setup()

from django.conf import settings


def main():
    print("🚀 DidactAI Language Configuration Verification")
    print("="*60)
    
    # Check Django LANGUAGES setting
    django_languages = getattr(settings, 'LANGUAGES', [])
    print(f"🌐 Django LANGUAGES: {len(django_languages)} configured")
    for code, name in django_languages:
        print(f"   • {name} ({code})")
    
    # Check application-specific supported languages
    from didactia_project import settings as project_settings
    app_settings = getattr(project_settings, 'DidactAI_SETTINGS', {})
    supported_languages = app_settings.get('SUPPORTED_LANGUAGES', [])
    
    print(f"\n📋 Application SUPPORTED_LANGUAGES: {len(supported_languages)} configured")
    
    # Language display names
    language_names = {
        'en': 'English', 'fr': 'French', 'es': 'Spanish', 'de': 'German',
        'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ar': 'Arabic',
        'zh': 'Chinese', 'ja': 'Japanese', 'ko': 'Korean', 'hi': 'Hindi',
        'tr': 'Turkish', 'el': 'Greek'
    }
    
    for lang_code in supported_languages:
        lang_name = language_names.get(lang_code, lang_code.upper())
        print(f"   • {lang_name} ({lang_code})")
    
    # Check if we have the expected 14 languages
    expected_count = 14
    actual_count = len(supported_languages)
    
    print(f"\n📊 Language Count Verification:")
    print(f"   Expected: {expected_count} languages")
    print(f"   Actual: {actual_count} languages")
    
    if actual_count == expected_count:
        print("   ✅ SUCCESS: Language count matches expectation!")
    else:
        print("   ❌ WARNING: Language count does not match expectation")
    
    # Check specific language availability
    expected_languages = ['en', 'fr', 'es', 'de', 'it', 'pt', 'ru', 'ar', 'zh', 'ja', 'ko', 'hi', 'tr', 'el']
    missing_languages = [lang for lang in expected_languages if lang not in supported_languages]
    extra_languages = [lang for lang in supported_languages if lang not in expected_languages]
    
    if not missing_languages and not extra_languages:
        print("   ✅ SUCCESS: All expected languages are configured correctly!")
    else:
        if missing_languages:
            print(f"   ⚠️  Missing languages: {', '.join(missing_languages)}")
        if extra_languages:
            print(f"   ⚠️  Extra languages: {', '.join(extra_languages)}")
    
    # Verify export formats are available
    from exports.models import ExportJob
    export_formats = dict(ExportJob.FORMAT_CHOICES)
    
    print(f"\n📄 Export Formats Available: {len(export_formats)}")
    for code, name in export_formats.items():
        print(f"   • {name} ({code})")
    
    # Check that JSON and ZIP are removed
    removed_formats = ['json', 'zip']
    still_present = [fmt for fmt in removed_formats if fmt in export_formats]
    
    if still_present:
        print(f"   ❌ ERROR: These formats should be removed: {', '.join(still_present)}")
    else:
        print("   ✅ SUCCESS: JSON and ZIP formats have been removed as requested!")
    
    print("\n🏁 Verification completed!")
    print("="*60)


if __name__ == '__main__':
    main()