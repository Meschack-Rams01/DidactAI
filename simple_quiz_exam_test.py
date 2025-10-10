#!/usr/bin/env python
"""
Simple Quiz and Exam Generation and Export Test

This script tests the core functionality without complex logging or emojis
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DidactAI_project.settings')
django.setup()

from django.conf import settings
from accounts.models import CustomUser
from courses.models import Course
from ai_generator.models import AIGeneration, QuizQuestion
from ai_generator.services import QuizGenerator, ExamGenerator
from uploads.models import UploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile

def test_quiz_and_exam_functionality():
    """Test the quiz and exam generation functionality"""
    print("DidactAI Quiz and Exam Functionality Test")
    print("=" * 45)
    
    results = {
        'tests_run': 0,
        'tests_passed': 0,
        'tests_failed': 0
    }
    
    def run_test(test_name, test_func):
        """Run a test function and record results"""
        print(f"Testing {test_name}... ", end="")
        results['tests_run'] += 1
        try:
            result = test_func()
            if result:
                print("PASS")
                results['tests_passed'] += 1
                return True
            else:
                print("FAIL")
                results['tests_failed'] += 1
                return False
        except Exception as e:
            print(f"ERROR: {e}")
            results['tests_failed'] += 1
            return False
    
    # Test 1: Database Models
    def test_database_models():
        """Test that all models are working"""
        try:
            # Check if models are accessible
            user_count = CustomUser.objects.count()
            course_count = Course.objects.count()
            generation_count = AIGeneration.objects.count()
            question_count = QuizQuestion.objects.count()
            file_count = UploadedFile.objects.count()
            
            print(f"\n    Database Status:")
            print(f"    - Users: {user_count}")
            print(f"    - Courses: {course_count}")  
            print(f"    - Generations: {generation_count}")
            print(f"    - Questions: {question_count}")
            print(f"    - Files: {file_count}")
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    # Test 2: AI Services
    def test_ai_services():
        """Test AI service initialization"""
        try:
            quiz_generator = QuizGenerator()
            exam_generator = ExamGenerator()
            
            # Check if services have required attributes
            has_gemini = hasattr(quiz_generator, 'gemini')
            has_methods = (hasattr(quiz_generator, 'generate_quiz') and 
                          hasattr(exam_generator, 'generate_exam'))
            
            print(f"\n    AI Services:")
            print(f"    - Quiz Generator: {'OK' if has_gemini else 'NO GEMINI'}")
            print(f"    - Exam Generator: {'OK' if has_methods else 'MISSING METHODS'}")
            print(f"    - Gemini API Key: {'SET' if settings.GEMINI_API_KEY else 'NOT SET'}")
            
            return has_gemini and has_methods
        except Exception as e:
            print(f"AI services error: {e}")
            return False
    
    # Test 3: Export Services
    def test_export_services():
        """Test export service availability"""
        try:
            from exports.services import PDFExporter, DOCXExporter, HTMLExporter
            from exports.services import REPORTLAB_AVAILABLE, DOCX_AVAILABLE
            
            pdf_available = REPORTLAB_AVAILABLE
            docx_available = DOCX_AVAILABLE
            html_available = True  # HTML is always available
            
            print(f"\n    Export Services:")
            print(f"    - PDF Export: {'AVAILABLE' if pdf_available else 'NOT AVAILABLE'}")
            print(f"    - DOCX Export: {'AVAILABLE' if docx_available else 'NOT AVAILABLE'}")
            print(f"    - HTML Export: {'AVAILABLE' if html_available else 'NOT AVAILABLE'}")
            
            return html_available  # At least HTML should be available
        except Exception as e:
            print(f"Export services error: {e}")
            return False
    
    # Test 4: File Processing
    def test_file_processing():
        """Test file upload and processing"""
        try:
            # Get or create a test user
            test_user, created = CustomUser.objects.get_or_create(
                username='testuser',
                defaults={'email': 'test@example.com'}
            )
            
            # Get or create a test course
            test_course, created = Course.objects.get_or_create(
                title='Test Course',
                defaults={'instructor': test_user}
            )
            
            # Create test content
            test_content = "Cloud computing is a model for enabling convenient network access to computing resources."
            
            # Create test file
            test_file = SimpleUploadedFile(
                "test.txt",
                test_content.encode('utf-8'),
                content_type="text/plain"
            )
            
            # Create uploaded file record
            uploaded_file = UploadedFile.objects.create(
                course=test_course,
                original_filename='test.txt',
                file_type='text/plain',
                file_size=len(test_content),
                uploaded_file=test_file,
                is_processed=True,
                extracted_text=test_content
            )
            
            print(f"\n    File Processing:")
            print(f"    - Test file created: {uploaded_file.original_filename}")
            print(f"    - Content length: {len(test_content)} chars")
            print(f"    - Processing status: {'PROCESSED' if uploaded_file.is_processed else 'PENDING'}")
            
            return True
        except Exception as e:
            print(f"File processing error: {e}")
            return False
    
    # Test 5: Quiz Generation (Basic)
    def test_quiz_generation():
        """Test basic quiz generation"""
        try:
            # Get test file
            test_file = UploadedFile.objects.filter(original_filename='test.txt').first()
            if not test_file:
                print("\n    No test file available for quiz generation")
                return False
            
            quiz_generator = QuizGenerator()
            
            # Try to generate a simple quiz (may use fallback if API not available)
            result = quiz_generator.generate_quiz(
                content=test_file.extracted_text,
                language='en',
                num_questions=3,
                difficulty='easy',
                question_types=['multiple_choice']
            )
            
            success = result.get('success', False)
            questions = result.get('questions', [])
            is_fallback = result.get('fallback', False)
            
            print(f"\n    Quiz Generation:")
            print(f"    - Generation successful: {'YES' if success else 'NO'}")
            print(f"    - Questions generated: {len(questions)}")
            print(f"    - Used fallback: {'YES' if is_fallback else 'NO'}")
            
            return success
        except Exception as e:
            print(f"Quiz generation error: {e}")
            return False
    
    # Test 6: Export Functionality (Basic)
    def test_export_functionality():
        """Test basic export functionality"""
        try:
            from exports.services import HTMLExporter
            
            # Test HTML export (most reliable)
            html_exporter = HTMLExporter()
            
            # Sample quiz data
            test_quiz_data = {
                'title': 'Test Quiz',
                'description': 'A simple test quiz',
                'questions': [
                    {
                        'id': 1,
                        'type': 'multiple_choice',
                        'question': 'What is cloud computing?',
                        'options': ['A service model', 'A hardware type', 'A software license', 'A network protocol'],
                        'correct_answer': 'A',
                        'points': 1
                    }
                ]
            }
            
            # Test branding
            test_branding = {
                'university_name': 'Test University',
                'department': 'Computer Science',
                'course': 'CS 101'
            }
            
            # Generate HTML export
            html_content = html_exporter.export_quiz(test_quiz_data, test_branding, show_answers=False)
            
            html_size = len(html_content)
            has_content = 'Test Quiz' in html_content and 'cloud computing' in html_content
            
            print(f"\n    Export Functionality:")
            print(f"    - HTML export size: {html_size} chars")
            print(f"    - Content validation: {'PASS' if has_content else 'FAIL'}")
            
            return has_content and html_size > 1000
        except Exception as e:
            print(f"Export functionality error: {e}")
            return False
    
    # Test 7: Turkish Content Support
    def test_turkish_support():
        """Test Turkish character support"""
        try:
            # Test Turkish content
            turkish_text = "Bilgisayar bilimi, algoritmaları ve veri yapılarını içerir."
            
            # Test if we can handle Turkish characters in database
            test_user = CustomUser.objects.filter(username='testuser').first()
            if test_user:
                test_course = Course.objects.filter(instructor=test_user).first()
                if test_course:
                    # Update course title with Turkish characters
                    test_course.title = "Türkçe Test Kursu"
                    test_course.save()
                    
                    # Retrieve and verify
                    updated_course = Course.objects.get(id=test_course.id)
                    turkish_saved = updated_course.title == "Türkçe Test Kursu"
                    
                    print(f"\n    Turkish Support:")
                    print(f"    - Turkish text: {turkish_text[:30]}...")
                    print(f"    - Database storage: {'OK' if turkish_saved else 'FAILED'}")
                    print(f"    - Character encoding: UTF-8")
                    
                    return turkish_saved
            
            return False
        except Exception as e:
            print(f"Turkish support error: {e}")
            return False
    
    # Run all tests
    print("\nRunning functionality tests...\n")
    
    run_test("Database Models", test_database_models)
    run_test("AI Services", test_ai_services)
    run_test("Export Services", test_export_services)
    run_test("File Processing", test_file_processing)
    run_test("Quiz Generation", test_quiz_generation)
    run_test("Export Functionality", test_export_functionality)
    run_test("Turkish Support", test_turkish_support)
    
    # Summary
    print("\n" + "=" * 45)
    print("TEST SUMMARY:")
    print(f"Total Tests: {results['tests_run']}")
    print(f"Passed: {results['tests_passed']}")
    print(f"Failed: {results['tests_failed']}")
    
    success_rate = (results['tests_passed'] / results['tests_run']) * 100 if results['tests_run'] > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("Status: GOOD - Core functionality working")
    elif success_rate >= 60:
        print("Status: FAIR - Most functionality working")
    else:
        print("Status: NEEDS ATTENTION - Several issues found")
    
    return success_rate

if __name__ == '__main__':
    success_rate = test_quiz_and_exam_functionality()
    
    # Exit with appropriate code
    if success_rate >= 80:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Issues found
