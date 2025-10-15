#!/usr/bin/env python
"""
DidactAI Production Deployment Script
Automates the deployment preparation process
"""

import os
import sys
import subprocess
import secrets
import string
from pathlib import Path

def generate_secret_key(length=50):
    """Generate a secure secret key for Django"""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_directories():
    """Create necessary directories for production"""
    dirs = ['logs', 'staticfiles', 'media', 'backup']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ Created directory: {dir_name}")

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def main():
    print("🚀 DidactAI Production Deployment Preparation")
    print("=" * 50)
    
    # 1. Create necessary directories
    print("\n1. Creating directories...")
    create_directories()
    
    # 2. Generate secret key
    print("\n2. Generating secure secret key...")
    secret_key = generate_secret_key()
    print("✓ New secret key generated (save this securely!)")
    print(f"SECRET_KEY={secret_key}")
    
    # 3. Install production requirements
    print("\n3. Installing production requirements...")
    run_command("pip install -r requirements-production.txt", "Installing production dependencies")
    
    # 4. Collect static files
    print("\n4. Collecting static files...")
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # 5. Run migrations
    print("\n5. Running database migrations...")
    run_command("python manage.py makemigrations", "Creating migrations")
    run_command("python manage.py migrate", "Applying migrations")
    
    # 6. Create superuser prompt
    print("\n6. Create superuser (optional)...")
    create_super = input("Do you want to create a superuser account? (y/N): ")
    if create_super.lower() == 'y':
        run_command("python manage.py createsuperuser", "Creating superuser")
    
    # 7. Run security check
    print("\n7. Running security checks...")
    run_command("python manage.py check --deploy", "Security deployment check")
    
    # 8. Test imports
    print("\n8. Testing critical imports...")
    try:
        import django
        print(f"✓ Django {django.VERSION} imported successfully")
        
        import reportlab
        print("✓ ReportLab imported successfully")
        
        import google.generativeai
        print("✓ Google Generative AI imported successfully")
        
        print("✓ All critical imports working")
    except ImportError as e:
        print(f"✗ Import error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Production deployment preparation completed!")
    print("\nNext steps:")
    print("1. Set your environment variables (see production.env)")
    print("2. Configure your database URL")
    print("3. Set up your web server (Nginx/Apache)")
    print("4. Configure SSL certificate")
    print("5. Set up monitoring and backups")
    print(f"6. Use this SECRET_KEY in production: {secret_key}")

if __name__ == '__main__':
    main()