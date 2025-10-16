"""
Initialization module to ensure database is ready
Runs migrations on first request if needed
"""

import os
import sys
import subprocess

_migration_done = False


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
