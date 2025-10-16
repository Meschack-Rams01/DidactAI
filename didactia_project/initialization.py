"""
Initialization module to ensure database is ready
Runs migrations on first request if needed
"""

import os
import sys
import subprocess
from decouple import config

_migration_done = False


def setup_admin_user():
    """Create or update admin user from environment variables"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        admin_email = config('ADMIN_EMAIL', default='admin@didactia.com')
        admin_password = config('ADMIN_PASSWORD', default='')
        admin_username = config('ADMIN_USERNAME', default='admin')
        
        if admin_password:  # Only create/update if password is set
            print(f"[INIT] Setting up admin user: {admin_email}")
            
            user, created = User.objects.get_or_create(
                email=admin_email,
                defaults={
                    'username': admin_username,
                    'is_staff': True,
                    'is_superuser': True,
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'role': 'admin'
                }
            )
            
            # Always update password and ensure superuser status
            user.set_password(admin_password)
            user.is_staff = True
            user.is_superuser = True
            user.username = admin_username
            user.save()
            
            status = 'created' if created else 'updated'
            print(f"[INIT] Admin user {status} successfully")
        else:
            print("[INIT] No ADMIN_PASSWORD set, skipping admin user setup")
            
    except Exception as e:
        print(f"[INIT] Error setting up admin user: {e}")
        import traceback
        traceback.print_exc()


def ensure_migrations_applied():
    """Ensure all migrations are applied before handling requests"""
    global _migration_done
    
    if _migration_done:
        return
    
    try:
        # Try to run migrations - this is idempotent
        # If already applied, Django will skip them
        print("\n" + "="*80)
        print("[INIT] Running database migrations...")
        print("="*80)
        
        try:
            result = subprocess.run(
                [sys.executable, 'manage.py', 'migrate', '--noinput', '--run-syncdb'],
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.stdout:
                print(f"[INIT] Migration output:\n{result.stdout}")
            
            if result.returncode != 0:
                print(f"[INIT] Migration completed with warnings/errors:")
                if result.stderr:
                    print(f"[INIT] {result.stderr}")
            else:
                print("[INIT] Migrations applied successfully")
            
            # Always try to setup site after migrations
            print("[INIT] Ensuring site record exists...")
            result = subprocess.run(
                [sys.executable, 'manage.py', 'setup_site'],
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.stdout:
                print(f"[INIT] {result.stdout.strip()}")
            
            if result.returncode != 0 and result.stderr:
                print(f"[INIT] Setup site note: {result.stderr}")
            
            # Setup admin user if needed
            setup_admin_user()
            
            print("[INIT] Database initialization complete!")
            print("="*80 + "\n")
            
        except subprocess.TimeoutExpired:
            print("[INIT] WARNING: Database initialization timeout - continuing anyway")
        except Exception as e:
            print(f"[INIT] Error running database setup: {e}")
            import traceback
            traceback.print_exc()
        
        _migration_done = True
        
    except Exception as e:
        print(f"[INIT] Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        _migration_done = True
