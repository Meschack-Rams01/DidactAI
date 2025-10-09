#!/usr/bin/env python
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
    print("ðŸ§¹ Cleaning up old files...")
    
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
    
    print("âœ… Maintenance completed!")
