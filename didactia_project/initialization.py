"""
Initialization module to ensure database is ready
Runs migrations on first request if needed
"""

import os
import sys
import subprocess
from django.db import connection

_migration_done = False


def ensure_migrations_applied():
    """Ensure all migrations are applied before handling requests"""
    global _migration_done
    
    if _migration_done:
        return
    
    try:
        # Check if accounts_customuser table exists
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts_customuser';")
                table_exists = cursor.fetchone() is not None
        except Exception as e:
            print(f"[INIT] Error checking database: {e}")
            table_exists = False
        
        if not table_exists:
            print("\n" + "="*80)
            print("[INIT] DATABASE INITIALIZATION REQUIRED")
            print("="*80)
            
            try:
                print("[INIT] Running migrations...")
                result = subprocess.run(
                    [sys.executable, 'manage.py', 'migrate', '--noinput', '--run-syncdb'],
                    cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode != 0:
                    print(f"[INIT] Migration stderr: {result.stderr}")
                else:
                    print("[INIT] Migrations completed successfully")
                
                print("[INIT] Running setup_site...")
                result = subprocess.run(
                    [sys.executable, 'manage.py', 'setup_site'],
                    cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode != 0:
                    print(f"[INIT] Setup site stderr: {result.stderr}")
                else:
                    print("[INIT] Site setup completed successfully")
                
            except subprocess.TimeoutExpired:
                print("[INIT] WARNING: Migration timeout - continuing anyway")
            except Exception as e:
                print(f"[INIT] Error running migrations: {e}")
                import traceback
                traceback.print_exc()
            
            print("[INIT] Database initialization complete!")
            print("="*80 + "\n")
        else:
            print("[INIT] Database already initialized, skipping migrations")
        
        _migration_done = True
        
    except Exception as e:
        print(f"[INIT] Unexpected error during initialization: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        # Mark as done to prevent retry
        _migration_done = True
