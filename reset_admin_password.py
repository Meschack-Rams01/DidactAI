#!/usr/bin/env python
"""
Script to reset superuser password for DidactAI
"""
import os
import sys
import django
from getpass import getpass

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
django.setup()

from accounts.models import CustomUser

def reset_superuser_password():
    print("🔐 Reset Superuser Password")
    print("=" * 40)
    
    # Get the superuser
    try:
        superuser = CustomUser.objects.get(email='admin@didactia.com')
        print(f"✅ Found superuser: {superuser.email} ({superuser.username})")
        
        # Get new password
        print("\n💡 Enter new password for the superuser:")
        new_password = getpass("New password: ")
        confirm_password = getpass("Confirm password: ")
        
        if new_password != confirm_password:
            print("❌ Passwords don't match!")
            return False
        
        if len(new_password) < 8:
            print("❌ Password too short! Must be at least 8 characters.")
            return False
        
        # Set the new password
        superuser.set_password(new_password)
        superuser.save()
        
        print("✅ Password successfully updated!")
        print(f"🎉 You can now login with:")
        print(f"   Email: {superuser.email}")
        print(f"   Username: {superuser.username}")
        print(f"   Password: [the password you just set]")
        
        return True
        
    except CustomUser.DoesNotExist:
        print("❌ Superuser admin@didactia.com not found!")
        return False

if __name__ == "__main__":
    try:
        reset_superuser_password()
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled.")
    except Exception as e:
        print(f"❌ Error: {e}")