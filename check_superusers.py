#!/usr/bin/env python
"""
Script to check existing superusers in DidactAI
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
django.setup()

from accounts.models import CustomUser

def check_superusers():
    print("🔍 Checking for existing superusers...")
    print("=" * 50)
    
    # Get all superusers
    superusers = CustomUser.objects.filter(is_superuser=True)
    
    if superusers.exists():
        print(f"✅ Found {superusers.count()} superuser(s):")
        print()
        
        for i, user in enumerate(superusers, 1):
            print(f"Superuser #{i}:")
            print(f"  📧 Email: {user.email}")
            print(f"  👤 Username: {user.username}")
            print(f"  📝 First Name: {user.first_name}")
            print(f"  📝 Last Name: {user.last_name}")
            print(f"  📅 Date Joined: {user.date_joined}")
            print(f"  📅 Last Login: {user.last_login}")
            print(f"  ✅ Is Active: {user.is_active}")
            print(f"  🔧 Is Staff: {user.is_staff}")
            print("-" * 30)
    else:
        print("❌ No superusers found in the database.")
        print("💡 You'll need to create a new superuser.")
    
    print()
    print("🔍 All users in system:")
    all_users = CustomUser.objects.all()
    if all_users.exists():
        for user in all_users:
            status = "👑 SUPERUSER" if user.is_superuser else "👤 Regular User"
            print(f"  {status}: {user.email} ({user.username})")
    else:
        print("  No users found in the system.")

if __name__ == "__main__":
    try:
        check_superusers()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you've run migrations: python manage.py migrate")