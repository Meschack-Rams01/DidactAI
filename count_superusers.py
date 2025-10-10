#!/usr/bin/env python
"""
Script to count and list all superusers in DidactAI
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
django.setup()

from accounts.models import CustomUser

def count_and_list_superusers():
    print("👑 SUPERUSER ANALYSIS - DidactAI System")
    print("=" * 50)
    
    # Count total users
    total_users = CustomUser.objects.count()
    
    # Count superusers
    superusers = CustomUser.objects.filter(is_superuser=True)
    superuser_count = superusers.count()
    
    # Count regular users
    regular_users = CustomUser.objects.filter(is_superuser=False)
    regular_user_count = regular_users.count()
    
    print(f"📊 **SYSTEM OVERVIEW**:")
    print(f"  🧑‍🤝‍🧑 Total Users: {total_users}")
    print(f"  👑 Superusers: {superuser_count}")
    print(f"  👤 Regular Users: {regular_user_count}")
    print()
    
    if superuser_count > 0:
        print(f"🎉 **YOU HAVE {superuser_count} SUPERUSER(S)**:")
        print()
        
        for i, user in enumerate(superusers, 1):
            print(f"🔹 **Superuser #{i}**:")
            print(f"    📧 Email: {user.email}")
            print(f"    👤 Username: {user.username}")
            print(f"    📝 Name: {user.first_name} {user.last_name}".strip())
            print(f"    🏢 Institution: {getattr(user, 'institution', 'N/A') or 'N/A'}")
            print(f"    📅 Created: {user.date_joined.strftime('%Y-%m-%d %H:%M')}")
            print(f"    📅 Last Login: {user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Never'}")
            print(f"    ✅ Is Active: {'Yes' if user.is_active else 'No'}")
            print(f"    🔧 Is Staff: {'Yes' if user.is_staff else 'No'}")
            print()
    else:
        print("❌ **NO SUPERUSERS FOUND!**")
        print("   You need to create at least one superuser.")
        print("   Run: python manage.py createsuperuser")
        print()
    
    # Show breakdown by role if available
    print("📈 **USER BREAKDOWN BY TYPE**:")
    roles = CustomUser.objects.values_list('role', flat=True).distinct()
    for role in roles:
        if role:
            role_count = CustomUser.objects.filter(role=role).count()
            role_superusers = CustomUser.objects.filter(role=role, is_superuser=True).count()
            print(f"  {role.title()}: {role_count} users ({role_superusers} superusers)")
    
    print()
    print("🔍 **ALL USERS IN SYSTEM** (sorted by permissions):")
    all_users = CustomUser.objects.all().order_by('-is_superuser', '-is_staff', 'email')
    
    for user in all_users:
        if user.is_superuser:
            icon = "👑"
            status = "SUPERUSER"
        elif user.is_staff:
            icon = "🔧"
            status = "STAFF"
        else:
            icon = "👤"
            status = "USER"
        
        active_status = "🟢" if user.is_active else "🔴"
        last_login = user.last_login.strftime('%Y-%m-%d') if user.last_login else "Never"
        
        print(f"  {icon} {active_status} {status}: {user.email} ({user.username}) - Last: {last_login}")
    
    print()
    print("🔑 **QUICK ACCESS COMMANDS**:")
    if superuser_count > 0:
        print("  Reset superuser password:")
        for user in superusers:
            print(f"    python manage.py changepassword {user.username}")
    else:
        print("    python manage.py createsuperuser")
    
    print()
    print("🌐 **Admin Panel**: http://localhost:8000/admin/")
    
    return superuser_count

if __name__ == "__main__":
    try:
        count = count_and_list_superusers()
        print()
        print(f"✅ **RESULT: You have {count} superuser(s) in your system.**")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you've run migrations: python manage.py migrate")