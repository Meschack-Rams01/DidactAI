#!/usr/bin/env python
"""
Script to promote a user to superuser in DidactAI
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
django.setup()

from accounts.models import CustomUser

def promote_user_to_superuser(email):
    print(f"🚀 Promoting user to superuser: {email}")
    print("=" * 50)
    
    try:
        # Find the user
        user = CustomUser.objects.get(email=email)
        
        print(f"✅ User found: {user.email} ({user.username})")
        print()
        
        # Check current status
        print("📋 **CURRENT STATUS**:")
        print(f"  👑 Is Superuser: {'✅ YES' if user.is_superuser else '❌ NO'}")
        print(f"  🔧 Is Staff: {'✅ YES' if user.is_staff else '❌ NO'}")
        print(f"  ✅ Is Active: {'✅ YES' if user.is_active else '❌ NO'}")
        
        if user.is_superuser:
            print()
            print("ℹ️  **USER IS ALREADY A SUPERUSER!**")
            print("   No changes needed.")
            return True
        
        # Confirm promotion
        print()
        print("⚠️  **CONFIRMATION REQUIRED**")
        print(f"   Are you sure you want to promote '{user.email}' to superuser?")
        print("   This will give them full admin access to the system.")
        print()
        
        confirm = input("   Type 'YES' to confirm: ").strip()
        
        if confirm.upper() != 'YES':
            print("❌ Operation cancelled.")
            return False
        
        # Promote the user
        user.is_superuser = True
        user.is_staff = True  # Superusers should also be staff
        user.save()
        
        print()
        print("🎉 **SUCCESS!**")
        print(f"✅ User '{user.email}' has been promoted to superuser!")
        print()
        print("📋 **NEW STATUS**:")
        print(f"  👑 Is Superuser: ✅ YES")
        print(f"  🔧 Is Staff: ✅ YES")
        print(f"  ✅ Is Active: ✅ YES")
        print()
        print("🌐 **ADMIN ACCESS**:")
        print(f"   Email: {user.email}")
        print(f"   Username: {user.username}")
        print("   Password: [Current password - may need reset]")
        print()
        print("🔗 **Admin Panel**: http://localhost:8000/admin/")
        
        return True
        
    except CustomUser.DoesNotExist:
        print(f"❌ User with email '{email}' not found!")
        print()
        print("🔍 Available users:")
        all_users = CustomUser.objects.all().order_by('-is_superuser', 'email')
        for user in all_users:
            status = "👑 SUPERUSER" if user.is_superuser else "👤 Regular User"
            print(f"  {status}: {user.email} ({user.username})")
        
        return False

def main():
    if len(sys.argv) > 1:
        email = sys.argv[1]
        promote_user_to_superuser(email)
    else:
        # Interactive mode
        print("🚀 User Promotion Tool")
        print("=" * 30)
        print()
        
        # Show available users
        print("🔍 Available users:")
        all_users = CustomUser.objects.all().order_by('-is_superuser', 'email')
        for i, user in enumerate(all_users, 1):
            status = "👑 SUPERUSER" if user.is_superuser else "👤 Regular User"
            print(f"  {i}. {status}: {user.email} ({user.username})")
        
        print()
        email = input("📧 Enter email to promote: ").strip()
        if email:
            promote_user_to_superuser(email)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled.")
    except Exception as e:
        print(f"❌ Error: {e}")