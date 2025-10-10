#!/usr/bin/env python
"""
Script to check user bergermeschack@gmail.com in DidactAI
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
django.setup()

from accounts.models import CustomUser

def check_user_bergermeschack():
    print("🔍 Checking user: bergermeschack@gmail.com")
    print("=" * 50)
    
    target_email = "bergermeschack@gmail.com"
    
    try:
        # Try to find the user
        user = CustomUser.objects.get(email=target_email)
        
        print(f"✅ User found!")
        print()
        print("📋 **USER DETAILS**:")
        print(f"  📧 Email: {user.email}")
        print(f"  👤 Username: {user.username}")
        print(f"  📝 First Name: {user.first_name}")
        print(f"  📝 Last Name: {user.last_name}")
        print(f"  🏢 Institution: {getattr(user, 'institution', 'N/A')}")
        print(f"  🏫 Department: {getattr(user, 'department', 'N/A')}")
        print(f"  🌐 Role: {getattr(user, 'role', 'N/A')}")
        print()
        print("🔐 **PERMISSIONS & STATUS**:")
        print(f"  👑 Is Superuser: {'✅ YES' if user.is_superuser else '❌ NO'}")
        print(f"  🔧 Is Staff: {'✅ YES' if user.is_staff else '❌ NO'}")
        print(f"  ✅ Is Active: {'✅ YES' if user.is_active else '❌ NO'}")
        print()
        print("📅 **ACTIVITY INFO**:")
        print(f"  📅 Date Joined: {user.date_joined}")
        print(f"  📅 Last Login: {user.last_login if user.last_login else 'Never logged in'}")
        
        # Check if this user is a superuser
        if user.is_superuser:
            print()
            print("🎉 **THIS USER IS A SUPERUSER!**")
            print("   You can use this account to access the admin panel:")
            print(f"   - Email: {user.email}")
            print(f"   - Username: {user.username}")
            print("   - Password: [You may need to reset it]")
        else:
            print()
            print("ℹ️  **THIS USER IS NOT A SUPERUSER**")
            print("   This is a regular user account.")
            
            # Option to make them superuser
            print()
            print("💡 Would you like to make this user a superuser?")
            print("   Run this command to promote them:")
            print(f"   python promote_user.py {user.email}")
        
    except CustomUser.DoesNotExist:
        print(f"❌ User with email '{target_email}' not found!")
        print()
        print("🔍 Let me check for similar emails...")
        
        # Look for similar emails
        similar_users = CustomUser.objects.filter(email__icontains="bergermeschack")
        if similar_users.exists():
            print("📧 Found similar emails:")
            for user in similar_users:
                status = "👑 SUPERUSER" if user.is_superuser else "👤 Regular User"
                print(f"  {status}: {user.email} ({user.username})")
        else:
            print("❌ No similar emails found.")
        
        print()
        print("🔍 All users in the system:")
        all_users = CustomUser.objects.all().order_by('-is_superuser', 'email')
        for user in all_users:
            status = "👑 SUPERUSER" if user.is_superuser else "👤 Regular User"
            print(f"  {status}: {user.email} ({user.username})")

if __name__ == "__main__":
    try:
        check_user_bergermeschack()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you've run migrations: python manage.py migrate")