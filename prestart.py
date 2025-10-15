#!/usr/bin/env python
"""
Pre-start script for DidactAI deployment
This ensures migrations and static files are ready before starting the server
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings

print("=" * 60)
print("🚀 DidactAI Pre-Start Setup")
print("=" * 60)

# Run migrations
print("\n📊 Running database migrations...")
try:
    call_command('migrate', '--noinput', verbosity=1)
    print("✅ Migrations completed successfully")
except Exception as e:
    print(f"❌ Migration failed: {e}")
    sys.exit(1)

# Collect static files
print("\n📁 Collecting static files...")
try:
    call_command('collectstatic', '--noinput', '--clear', verbosity=1)
    print("✅ Static files collected successfully")
except Exception as e:
    print(f"❌ Static collection failed: {e}")
    sys.exit(1)

# Verify logo exists
print("\n🔍 Verifying static files...")
static_root = settings.STATIC_ROOT
logo_path = os.path.join(static_root, 'images', 'logo-professional.svg')

if os.path.exists(logo_path):
    print(f"✅ Logo found: {logo_path}")
else:
    print(f"⚠️  Logo not found: {logo_path}")
    images_dir = os.path.join(static_root, 'images')
    if os.path.exists(images_dir):
        files = os.listdir(images_dir)
        print(f"📂 Images directory contains {len(files)} files:")
        for f in files[:10]:  # Show first 10 files
            print(f"   - {f}")
    else:
        print("❌ Images directory does not exist!")

print("\n" + "=" * 60)
print("🎉 Pre-start setup completed successfully!")
print("=" * 60)
print("")