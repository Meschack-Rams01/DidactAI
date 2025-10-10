#!/usr/bin/env python
"""
Comprehensive Fix Script for DidactAI Project
Addresses all identified issues and optimizes the system
"""

import os
import sys
import django
import secrets
import string

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DidactAI_project.settings')
django.setup()

def fix_security_issues():
    """Fix security configuration issues"""
    print("ðŸ”’ Fixing Security Issues")
    print("=" * 40)
    
    # Generate a proper SECRET_KEY
    def generate_secret_key(length=50):
        """Generate a cryptographically strong secret key"""
        alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    # Read current .env file
    env_file_path = '.env'
    
    try:
        with open(env_file_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
        
        # Generate new secret key
        new_secret_key = generate_secret_key()
        
        # Update SECRET_KEY
        import re
        env_content = re.sub(
            r'^SECRET_KEY=.*$',
            f'SECRET_KEY={new_secret_key}',
            env_content,
            flags=re.MULTILINE
        )
        
        # Add production security settings if not present
        security_settings = """
# Production Security Settings
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True

# Note: SSL settings are disabled for development
# Enable these in production with proper SSL certificate:
# SECURE_SSL_REDIRECT=True
# SESSION_COOKIE_SECURE=True
# CSRF_COOKIE_SECURE=True
"""
        
        if 'SECURE_HSTS_SECONDS' not in env_content:
            env_content += security_settings
        
        # Write back the updated .env file
        with open(env_file_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ Generated new SECRET_KEY")
        print("✅ Added production security settings")
        return True
        
    except Exception as e:
        print(f"âŒ Error fixing security issues: {e}")
        return False

def fix_dependency_issues():
    """Fix dependency version conflicts"""
    print("\nðŸ“¦ Fixing Dependency Issues")
    print("=" * 40)
    
    try:
        # Create a requirements-fixed.txt with compatible versions
        fixed_requirements = """
# Core Django and Framework
Django==4.2.24
djangorestframework==3.15.2
django-cors-headers==4.8.0
django-environ==0.11.2
python-decouple==3.8

# Database
psycopg2-binary==2.9.7
dj-database-url==2.1.0

# Authentication & Security  
django-allauth==0.65.2
django-crispy-forms==2.4
crispy-tailwind==0.5.0

# File Handling & Storage
Pillow==11.3.0
django-storages==1.14.6
boto3==1.35.9
supabase==2.6.0

# Document Processing
PyPDF2==3.0.1
python-docx==1.2.0
python-pptx==0.6.22
pytesseract==0.3.10
opencv-python==4.12.0.88

# AI & NLP Libraries  
langchain==0.3.12
langchain-google-genai==2.1.0
google-generativeai==0.8.5
transformers==4.43.3
torch==2.4.0
sentence-transformers==3.2.1
langdetect==1.0.9

# Export & PDF Generation
reportlab==4.4.1
python-docx==1.2.0

# Utilities
celery==5.3.6
redis==5.1.1
requests==2.32.3
python-magic==0.4.27

# Development
django-debug-toolbar==4.4.6
black==24.10.0
flake8==7.0.0
pytest-django==4.8.0

# Production Server
gunicorn==22.0.0

# Search and Elasticsearch (Compatible versions)
elasticsearch==7.17.12
django-elasticsearch-dsl==7.4.2

# Social Auth (Compatible version)
social-auth-app-django==5.4.1
"""
        
        with open('requirements-fixed.txt', 'w', encoding='utf-8') as f:
            f.write(fixed_requirements.strip())
        
        print("✅ Created requirements-fixed.txt with compatible versions")
        print("ðŸ’¡ Run: pip install -r requirements-fixed.txt --upgrade")
        return True
        
    except Exception as e:
        print(f"âŒ Error fixing dependencies: {e}")
        return False

def fix_missing_services():
    """Fix missing services and add fallback implementations"""
    print("\nðŸ”§ Fixing Missing Services")
    print("=" * 40)
    
    try:
        # Create missing services in uploads app
        uploads_services_path = 'uploads/services.py'
        
        if not os.path.exists(uploads_services_path):
            uploads_services_content = '''"""
File Processing Services for DidactAI
"""

import os
import logging
from typing import Dict, Any, Optional
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings

logger = logging.getLogger(__name__)


class FileProcessor:
    """Service for processing uploaded files"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.pptx', '.txt', '.png', '.jpg', '.jpeg']
    
    def process_file(self, uploaded_file: InMemoryUploadedFile) -> Dict[str, Any]:
        """Process an uploaded file and extract text content"""
        try:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_extension == '.txt':
                return self._process_text_file(uploaded_file)
            elif file_extension == '.pdf':
                return self._process_pdf_file(uploaded_file)
            elif file_extension == '.docx':
                return self._process_docx_file(uploaded_file)
            elif file_extension in ['.png', '.jpg', '.jpeg']:
                return self._process_image_file(uploaded_file)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported file format: {file_extension}'
                }
        
        except Exception as e:
            logger.error(f"Error processing file {uploaded_file.name}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _process_text_file(self, file) -> Dict[str, Any]:
        """Process plain text file"""
        try:
            content = file.read().decode('utf-8')
            return {
                'success': True,
                'text_content': content,
                'word_count': len(content.split()),
                'character_count': len(content)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _process_pdf_file(self, file) -> Dict[str, Any]:
        """Process PDF file"""
        try:
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ""
            
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\\n"
            
            return {
                'success': True,
                'text_content': text_content,
                'page_count': len(pdf_reader.pages),
                'word_count': len(text_content.split())
            }
        except ImportError:
            return {
                'success': False,
                'error': 'PyPDF2 not available. Please install: pip install PyPDF2'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _process_docx_file(self, file) -> Dict[str, Any]:
        """Process DOCX file"""
        try:
            from docx import Document
            doc = Document(file)
            text_content = ""
            
            for paragraph in doc.paragraphs:
                text_content += paragraph.text + "\\n"
            
            return {
                'success': True,
                'text_content': text_content,
                'paragraph_count': len(doc.paragraphs),
                'word_count': len(text_content.split())
            }
        except ImportError:
            return {
                'success': False,
                'error': 'python-docx not available. Please install: pip install python-docx'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _process_image_file(self, file) -> Dict[str, Any]:
        """Process image file with OCR"""
        try:
            import pytesseract
            from PIL import Image
            
            image = Image.open(file)
            text_content = pytesseract.image_to_string(image)
            
            return {
                'success': True,
                'text_content': text_content,
                'image_format': image.format,
                'image_size': image.size,
                'word_count': len(text_content.split())
            }
        except ImportError:
            return {
                'success': False,
                'error': 'OCR dependencies not available. Please install pytesseract and Pillow'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def detect_language(self, text: str) -> Optional[str]:
        """Detect language of text content"""
        try:
            from langdetect import detect
            return detect(text)
        except ImportError:
            logger.warning("langdetect not available")
            return 'en'  # Default to English
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            return 'en'
'''
            
            with open(uploads_services_path, 'w', encoding='utf-8') as f:
                f.write(uploads_services_content)
            
            print("✅ Created uploads/services.py")
        
        # Create missing HTMLExporter in exports
        html_exporter_exists = False
        
        try:
            from exports.services import HTMLExporter
            html_exporter_exists = True
        except ImportError:
            pass
        
        if not html_exporter_exists:
            # Add HTMLExporter to exports/services.py
            exports_services_path = 'exports/services.py'
            
            # Read existing content
            with open(exports_services_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add HTMLExporter class
            html_exporter_code = '''

class HTMLExporter:
    """Service for exporting content to HTML format"""
    
    def export_quiz(self, quiz_data: Dict[str, Any], branding: Dict[str, Any] = None) -> str:
        """Export quiz to HTML format"""
        
        # Simple HTML template
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }}
        .question {{ margin: 20px 0; padding: 15px; border-left: 4px solid #007bff; }}
        .options {{ margin-left: 20px; }}
        .option {{ margin: 5px 0; }}
        .instructions {{ background: #f8f9fa; padding: 15px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        {branding_info}
        <p>Duration: {duration} | Total Points: {points}</p>
    </div>
    
    <div class="instructions">
        <h3>Instructions:</h3>
        <ul>
            <li>Read each question carefully</li>
            <li>Choose the best answer for each question</li>
            <li>Write clearly and legibly</li>
        </ul>
    </div>
    
    {questions_html}
</body>
</html>
        """
        
        # Build branding info
        branding_info = ""
        if branding:
            branding_parts = []
            if branding.get('university_name'):
                branding_parts.append(f"<h2>{branding['university_name']}</h2>")
            if branding.get('department'):
                branding_parts.append(f"<p>{branding['department']}</p>")
            if branding.get('instructor'):
                branding_parts.append(f"<p>Instructor: {branding['instructor']}</p>")
            branding_info = ''.join(branding_parts)
        
        # Build questions HTML
        questions_html = ""
        for i, question in enumerate(quiz_data.get('questions', []), 1):
            question_html = f'<div class="question"><h3>Question {i}</h3>'
            question_html += f'<p><strong>{question.get("question", "")}</strong></p>'
            
            if question.get('question_type') == 'multiple_choice' and question.get('options'):
                question_html += '<div class="options">'
                for j, option in enumerate(question['options']):
                    option_letter = chr(65 + j)
                    question_html += f'<div class="option">{option_letter}. {option}</div>'
                question_html += '</div>'
            
            question_html += '</div>'
            questions_html += question_html
        
        # Fill template
        html_content = html_template.format(
            title=quiz_data.get('title', 'Quiz'),
            branding_info=branding_info,
            duration=quiz_data.get('estimated_duration', '30 minutes'),
            points=quiz_data.get('total_points', len(quiz_data.get('questions', []))),
            questions_html=questions_html
        )
        
        return html_content
'''
            
            content += html_exporter_code
            
            with open(exports_services_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Added HTMLExporter to exports/services.py")
        
        return True
        
    except Exception as e:
        print(f"âŒ Error fixing missing services: {e}")
        return False

def create_production_settings():
    """Create production-ready settings file"""
    print("\nâš™ Creating Production Settings")
    print("=" * 40)
    
    try:
        production_settings = '''"""
Production settings for DidactAI

Copy this to DidactAI_project/production_settings.py for deployment
"""

from .settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Production hosts - update with your domain
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database - Use PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'DidactAI_prod'),
        'USER': os.environ.get('DB_USER', 'DidactAI_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Security Settings
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Email configuration for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'DidactAI <noreply@yourdomain.com>')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/DidactAI/DidactAI.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'DidactAI': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Celery Configuration for production
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
    }
}
'''
        
        production_settings_path = 'DidactAI_project/production_settings.py'
        with open(production_settings_path, 'w', encoding='utf-8') as f:
            f.write(production_settings.strip())
        
        print("✅ Created production_settings.py")
        return True
        
    except Exception as e:
        print(f"âŒ Error creating production settings: {e}")
        return False

def create_deployment_scripts():
    """Create deployment and maintenance scripts"""
    print("\n🚀 Creating Deployment Scripts")
    print("=" * 40)
    
    try:
        # Create deployment script
        deploy_script = '''#!/bin/bash
# DidactAI Deployment Script

echo "🚀 Starting DidactAI Deployment..."

# Update code
git pull origin main

# Install/update dependencies
pip install -r requirements-fixed.txt --upgrade

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

# Create superuser if it doesn't exist
python manage.py shell -c "
from accounts.models import CustomUser
if not CustomUser.objects.filter(is_superuser=True).exists():
    print('Creating superuser...')
    CustomUser.objects.create_superuser(
        email='admin@yourdomain.com',
        username='admin',
        password='change-this-password'
    )
    print('Superuser created!')
else:
    print('Superuser already exists')
"

# Restart services
sudo systemctl restart DidactAI
sudo systemctl restart nginx

echo "✅ Deployment completed!"
'''
        
        with open('deploy.sh', 'w', encoding='utf-8') as f:
            f.write(deploy_script.strip())
        
        # Create maintenance script
        maintenance_script = '''#!/usr/bin/env python
"""
DidactAI Maintenance Script
Run regular maintenance tasks
"""

import os
import sys
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DidactAI_project.settings')
django.setup()

from django.core.management import call_command
from exports.models import ExportJob
from uploads.models import UploadedFile
from analytics.models import ErrorLog

def cleanup_old_files():
    """Clean up old export files and uploads"""
    print("🐧¹ Cleaning up old files...")
    
    # Delete old export jobs (older than 30 days)
    cutoff_date = datetime.now() - timedelta(days=30)
    old_exports = ExportJob.objects.filter(created_at__lt=cutoff_date)
    deleted_exports = old_exports.count()
    old_exports.delete()
    
    print(f"   Deleted {deleted_exports} old export jobs")
    
    # Clean up error logs (older than 90 days)
    error_cutoff = datetime.now() - timedelta(days=90)
    old_errors = ErrorLog.objects.filter(first_occurred__lt=error_cutoff)
    deleted_errors = old_errors.count()
    old_errors.delete()
    
    print(f"   Deleted {deleted_errors} old error logs")

def backup_database():
    """Create database backup"""
    print("ðŸ’¾ Creating database backup...")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"DidactAI_backup_{timestamp}.json"
    
    call_command('dumpdata', '--natural-foreign', '--natural-primary', 
                 '--exclude=contenttypes', '--exclude=auth.permission',
                 output=backup_file)
    
    print(f"   Database backed up to {backup_file}")

def generate_usage_report():
    """Generate usage statistics report"""
    print("ðŸ“Š Generating usage report...")
    
    from accounts.models import CustomUser
    from courses.models import Course
    from ai_generator.models import AIGeneration
    
    total_users = CustomUser.objects.count()
    total_courses = Course.objects.count()
    total_generations = AIGeneration.objects.count()
    
    print(f"   Total Users: {total_users}")
    print(f"   Total Courses: {total_courses}")
    print(f"   Total AI Generations: {total_generations}")

if __name__ == "__main__":
    print(f"ðŸ”§ DidactAI Maintenance - {datetime.now()}")
    print("=" * 50)
    
    cleanup_old_files()
    backup_database()
    generate_usage_report()
    
    print("✅ Maintenance completed!")
'''
        
        with open('maintenance.py', 'w', encoding='utf-8') as f:
            f.write(maintenance_script.strip())
        
        print("✅ Created deploy.sh")
        print("✅ Created maintenance.py")
        return True
        
    except Exception as e:
        print(f"âŒ Error creating deployment scripts: {e}")
        return False

def run_comprehensive_fixes():
    """Run all fixes"""
    print("ðŸ”§ DidactAI Comprehensive Fix Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    fixes_results = {}
    
    # Run all fixes
    fixes_results['security'] = fix_security_issues()
    fixes_results['dependencies'] = fix_dependency_issues()
    fixes_results['services'] = fix_missing_services()
    fixes_results['production'] = create_production_settings()
    fixes_results['deployment'] = create_deployment_scripts()
    
    # Summary
    print("\n" + "=" * 60)
    print("ðŸ FIX RESULTS SUMMARY")
    print("=" * 60)
    
    total_fixes = len(fixes_results)
    successful_fixes = sum(1 for result in fixes_results.values() if result)
    
    for fix_name, success in fixes_results.items():
        status = "✅" if success else "âŒ"
        print(f"{status} {fix_name.title()}: {'FIXED' if success else 'FAILED'}")
    
    success_rate = (successful_fixes / total_fixes) * 100
    print(f"\nðŸ“Š Fix Success Rate: {success_rate:.1f}% ({successful_fixes}/{total_fixes} fixes applied)")
    
    if success_rate == 100:
        print("🎉 All fixes applied successfully!")
    elif success_rate >= 75:
        print("ðŸ‘ Most fixes applied successfully")
    else:
        print("⚠Some fixes failed - manual intervention may be required")
    
    print("\nðŸ“ NEXT STEPS:")
    print("-" * 20)
    print("1. Restart Django server to apply changes")
    print("2. Install fixed dependencies: pip install -r requirements-fixed.txt --upgrade")
    print("3. Run tests again: python comprehensive_test.py")
    print("4. Configure production settings when ready")
    print("5. Use deploy.sh for production deployment")

if __name__ == "__main__":
    from datetime import datetime
    run_comprehensive_fixes()
