"""
Initialization module to ensure database is ready
Runs migrations on first request if needed
"""

import os
import sys
import django
from django.db import connection
from django.core.management import execute_from_command_line

_migration_done = False


def ensure_migrations_applied():
    """Ensure all migrations are applied before handling requests"""
    global _migration_done
    
    if _migration_done:
        return
    
    try:
        # Check if accounts_customuser table exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts_customuser';")
            table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            print("\n" + "="*80)
            print("DATABASE INITIALIZATION REQUIRED")
            print("="*80)
            print("Running migrations...")
            
            # Run migrations
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
            execute_from_command_line(['manage.py', 'migrate', '--noinput', '--run-syncdb'])
            
            print("Running setup_site...")
            execute_from_command_line(['manage.py', 'setup_site'])
            
            print("Database initialization complete!")
            print("="*80 + "\n")
        
        _migration_done = True
        
    except Exception as e:
        print(f"Error during database initialization: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        # Don't crash, let Django handle the error
