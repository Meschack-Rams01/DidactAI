#!/usr/bin/env python
"""
Quick setup script to ensure the platform is ready for testing
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DidactAI_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from courses.models import Course
from uploads.models import UploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile
import io

User = get_user_model()

def quick_setup():
    print("🚀 DidactAI QUICK SETUP")
    print("=" * 40)
    
    # Check/create superuser
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("Creating admin user...")
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@DidactAI.com', 
            password='admin123'
        )
        print("✅ Admin user created (admin/admin123)")
    else:
        print(f"✅ Admin user exists: {admin_user.username}")
    
    # Check courses
    course_count = Course.objects.count()
    print(f"✅ Found {course_count} courses")
    
    # Check files
    file_count = UploadedFile.objects.count()
    print(f"✅ Found {file_count} uploaded files")
    
    if file_count == 0:
        print("Creating sample files...")
        # Create a test course if none exists
        if course_count == 0:
            course = Course.objects.create(
                title="Sample Course",
                course_code="SAMPLE101",
                instructor=admin_user,
                description="Sample course for testing"
            )
        else:
            course = Course.objects.first()
        
        # Create a sample text file
        sample_content = """
        Introduction to Machine Learning
        
        Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.
        
        Key Types:
        1. Supervised Learning - Learning with labeled data
        2. Unsupervised Learning - Finding patterns in unlabeled data  
        3. Reinforcement Learning - Learning through trial and error
        
        Applications:
        - Image recognition
        - Natural language processing
        - Recommendation systems
        - Autonomous vehicles
        """
        
        # Create uploaded file
        UploadedFile.objects.create(
            course=course,
            original_filename="sample_ml_notes.txt",
            file_size=len(sample_content),
            file_type='txt',
            extracted_text=sample_content,
            detected_language='en',
            status='ready',
            is_processed=True
        )
        print("✅ Sample file created")
    
    print("\n🎉 SETUP COMPLETE!")
    print("=" * 40)
    print("Now you can:")
    print("1. Start the server: python manage.py runserver")
    print("2. Login with admin/admin123")
    print("3. Go to AI Generator to test file browsing")
    print("4. Files are available for quiz/exam generation")

if __name__ == '__main__':
    quick_setup()
