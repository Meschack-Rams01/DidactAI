#!/usr/bin/env python
"""
Script to diagnose admin dashboard login issues in DidactAI
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
django.setup()

from accounts.models import CustomUser
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import authenticate

def diagnose_admin_dashboard():
    print("🔍 ADMIN DASHBOARD DIAGNOSIS")
    print("=" * 50)
    
    # 1. Check superuser status
    print("1️⃣ **CHECKING SUPERUSER STATUS**:")
    try:
        admin_user = CustomUser.objects.get(email='admin@didactia.com')
        print(f"   ✅ Admin user found: {admin_user.email}")
        print(f"   👑 Is Superuser: {'✅ YES' if admin_user.is_superuser else '❌ NO'}")
        print(f"   🔧 Is Staff: {'✅ YES' if admin_user.is_staff else '❌ NO'}")
        print(f"   ✅ Is Active: {'✅ YES' if admin_user.is_active else '❌ NO'}")
        
        if not admin_user.is_superuser:
            print("   ⚠️ WARNING: User is not a superuser!")
        if not admin_user.is_staff:
            print("   ⚠️ WARNING: User is not staff!")
        if not admin_user.is_active:
            print("   ⚠️ WARNING: User is not active!")
    except CustomUser.DoesNotExist:
        print("   ❌ Admin user not found!")
        return
    
    print()
    
    # 2. Check Django settings
    print("2️⃣ **CHECKING DJANGO SETTINGS**:")
    print(f"   🐛 DEBUG: {settings.DEBUG}")
    print(f"   🔐 LOGIN_URL: {getattr(settings, 'LOGIN_URL', 'Not set')}")
    print(f"   🏠 LOGIN_REDIRECT_URL: {getattr(settings, 'LOGIN_REDIRECT_URL', 'Not set')}")
    print(f"   🚪 LOGOUT_REDIRECT_URL: {getattr(settings, 'LOGOUT_REDIRECT_URL', 'Not set')}")
    print()
    
    # 3. Check URL patterns
    print("3️⃣ **CHECKING URL PATTERNS**:")
    try:
        admin_url = reverse('admin:index')
        print(f"   🔗 Admin URL: {admin_url}")
    except:
        print("   ❌ Admin URL not found!")
    
    try:
        dashboard_url = reverse('accounts:dashboard')
        print(f"   🏠 Dashboard URL: {dashboard_url}")
    except:
        print("   ❌ Dashboard URL not found!")
        try:
            dashboard_url = reverse('dashboard')
            print(f"   🏠 Dashboard URL (alt): {dashboard_url}")
        except:
            print("   ❌ No dashboard URL found!")
    
    print()
    
    # 4. Check installed apps
    print("4️⃣ **CHECKING INSTALLED APPS**:")
    required_apps = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.sessions',
        'accounts',
    ]
    
    for app in required_apps:
        if app in settings.INSTALLED_APPS:
            print(f"   ✅ {app}")
        else:
            print(f"   ❌ {app} - MISSING!")
    
    print()
    
    # 5. Check middleware
    print("5️⃣ **CHECKING MIDDLEWARE**:")
    required_middleware = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ]
    
    for middleware in required_middleware:
        if middleware in settings.MIDDLEWARE:
            print(f"   ✅ {middleware}")
        else:
            print(f"   ❌ {middleware} - MISSING!")
    
    print()
    
    # 6. Test authentication
    print("6️⃣ **TESTING AUTHENTICATION**:")
    print("   ℹ️ Testing with username 'admin'...")
    
    # Check if we can authenticate (without password)
    admin_by_username = CustomUser.objects.filter(username='admin').first()
    if admin_by_username:
        print(f"   ✅ User found by username: {admin_by_username.email}")
        print(f"   🔑 Can login to admin: {'✅ YES' if admin_by_username.is_staff and admin_by_username.is_superuser else '❌ NO'}")
    else:
        print("   ❌ No user with username 'admin' found!")
    
    print()
    
    # 7. Check common URLs
    print("7️⃣ **AVAILABLE URLS TO TRY**:")
    urls_to_try = [
        ("Admin Panel", "http://localhost:8000/admin/"),
        ("Main Dashboard", "http://localhost:8000/dashboard/"),
        ("Accounts Dashboard", "http://localhost:8000/accounts/dashboard/"),
        ("Home Page", "http://localhost:8000/"),
        ("Login Page", "http://localhost:8000/accounts/login/"),
    ]
    
    for name, url in urls_to_try:
        print(f"   🔗 {name}: {url}")
    
    print()
    
    # 8. Provide solutions
    print("8️⃣ **POTENTIAL SOLUTIONS**:")
    print("   1. Try these URLs after login:")
    print("      • http://localhost:8000/admin/ (Django Admin)")
    print("      • http://localhost:8000/dashboard/ (Main Dashboard)")
    print()
    
    print("   2. If admin panel doesn't work:")
    print("      • Check if user is both superuser AND staff")
    print("      • Run: python manage.py collectstatic")
    print()
    
    print("   3. If dashboard doesn't work:")
    print("      • Check URL patterns in your urls.py")
    print("      • Check if templates exist")
    print()
    
    print("   4. Reset password if needed:")
    print("      • python manage.py changepassword admin")

if __name__ == "__main__":
    try:
        diagnose_admin_dashboard()
    except Exception as e:
        print(f"❌ Error during diagnosis: {e}")
        import traceback
        traceback.print_exc()