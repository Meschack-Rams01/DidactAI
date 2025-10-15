#!/usr/bin/env python
"""
Startup script for DidactAI on Render
Alternative to start.sh for better compatibility
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and print status"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    """Main startup function"""
    print("🚀 Starting DidactAI application...")
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
    
    # Run migrations
    if not run_command('python manage.py migrate --noinput', 'Running database migrations'):
        print("⚠️ Warning: Database migrations failed, continuing...")
    
    # Collect static files
    print("🗂️ Collecting static files for production...")
    if not run_command('python manage.py collectstatic --noinput --clear', 'Collecting static files'):
        print("⚠️ Warning: Static files collection failed, continuing...")
    
    # Create missing static directories if needed
    import os
    static_dirs = ['staticfiles/images', 'staticfiles/css', 'staticfiles/js']
    for static_dir in static_dirs:
        os.makedirs(static_dir, exist_ok=True)
        print(f"📁 Ensured directory: {static_dir}")
    
    # Get port from environment
    port = os.getenv('PORT', '8000')
    
    # Start Gunicorn
    gunicorn_cmd = [
        'gunicorn',
        'didactia_project.wsgi:application',
        f'--bind=0.0.0.0:{port}',
        '--workers=2',
        '--timeout=120',
        '--access-logfile=-',
        '--error-logfile=-',
        '--log-level=info'
    ]
    
    print(f"🚀 Starting Gunicorn server on port {port}...")
    print(f"Command: {' '.join(gunicorn_cmd)}")
    
    # Execute Gunicorn
    os.execvp('gunicorn', gunicorn_cmd)

if __name__ == '__main__':
    main()