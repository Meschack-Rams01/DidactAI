#!/usr/bin/env python
"""
Manual test for AI Generator - simulate form submission
"""

import os
import django
import requests

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from ai_generator.models import AIGeneration

User = get_user_model()

def test_quiz_generation():
    """Test quiz generation via form submission"""
    print("🧪 Testing Quiz Generation Form Submission...")
    
    # Create Django test client
    client = Client()
    
    # Create or get test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    # Login the test user
    client.force_login(user)
    
    # Get the quiz form page
    response = client.get('/ai-generator/quiz/')
    print(f"✅ Quiz form GET request: Status {response.status_code}")
    
    # Submit quiz generation form
    form_data = {
        'topic': 'Machine Learning',
        'difficulty': 'medium',
        'num_questions': 5,
        'question_types': ['multiple_choice', 'short_answer']
    }
    
    response = client.post('/ai-generator/quiz/', form_data)
    print(f"✅ Quiz form POST request: Status {response.status_code}")
    
    if response.status_code == 302:  # Redirect after successful creation
        print("✅ Quiz generation successful - redirected to view page")
        
        # Check if generation was created
        latest_generation = AIGeneration.objects.filter(content_type='quiz').last()
        if latest_generation:
            print(f"✅ Generated quiz: {latest_generation.title}")
            print(f"   Questions: {len(latest_generation.generated_content.get('questions', []))}")
            
            # Test viewing the generation
            view_response = client.get(f'/ai-generator/view/{latest_generation.id}/')
            print(f"✅ View generation: Status {view_response.status_code}")
            
            return True
    elif response.status_code == 200:
        print("⚠️  Form returned to same page - check for validation errors")
        return False
    else:
        print(f"❌ Unexpected status code: {response.status_code}")
        return False

def test_exam_generation():
    """Test exam generation via form submission"""
    print("\n🧪 Testing Exam Generation Form Submission...")
    
    client = Client()
    
    # Get test user
    user = User.objects.get(username='testuser')
    client.force_login(user)
    
    # Get the exam form page
    response = client.get('/ai-generator/exam/')
    print(f"✅ Exam form GET request: Status {response.status_code}")
    
    # Submit exam generation form
    form_data = {
        'topic': 'Data Structures',
        'difficulty': 'hard',
        'num_questions': 10,
        'duration': 90,
        'question_types': ['multiple_choice', 'essay'],
        'create_versions': False
    }
    
    response = client.post('/ai-generator/exam/', form_data)
    print(f"✅ Exam form POST request: Status {response.status_code}")
    
    if response.status_code == 302:  # Redirect after successful creation
        print("✅ Exam generation successful - redirected to view page")
        
        # Check if generation was created
        latest_generation = AIGeneration.objects.filter(content_type='exam').last()
        if latest_generation:
            print(f"✅ Generated exam: {latest_generation.title}")
            sections = latest_generation.generated_content.get('sections', [])
            total_questions = sum(len(section.get('questions', [])) for section in sections)
            print(f"   Sections: {len(sections)}")
            print(f"   Total questions: {total_questions}")
            
            return True
    elif response.status_code == 200:
        print("⚠️  Form returned to same page - check for validation errors")
        return False
    else:
        print(f"❌ Unexpected status code: {response.status_code}")
        return False

def test_generation_history():
    """Test generation history page"""
    print("\n🧪 Testing Generation History...")
    
    client = Client()
    user = User.objects.get(username='testuser')
    client.force_login(user)
    
    response = client.get('/ai-generator/history/')
    print(f"✅ History page: Status {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Generation history page loads successfully")
        return True
    return False

def main():
    """Run manual tests"""
    print("🚀 Starting Manual AI Generator Tests")
    print("=" * 50)
    
    # Count initial generations
    initial_count = AIGeneration.objects.count()
    print(f"Initial generations in database: {initial_count}")
    
    results = []
    
    # Run tests
    results.append(("Quiz Generation", test_quiz_generation()))
    results.append(("Exam Generation", test_exam_generation()))
    results.append(("Generation History", test_generation_history()))
    
    # Final count
    final_count = AIGeneration.objects.count()
    print(f"\nFinal generations in database: {final_count}")
    print(f"New generations created: {final_count - initial_count}")
    
    # Print results
    print("\n" + "=" * 50)
    print("📊 MANUAL TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All AI Generator features are working correctly!")
        print("\n📝 Ready for Browser Testing:")
        print("1. Open http://127.0.0.1:8000/")
        print("2. Login with testuser / testpass123")
        print("3. Navigate to AI Generator in the sidebar")
        print("4. Try generating quizzes and exams")
        print("5. Check generation history")
        
        # Show recent generations
        print("\n📋 Recent Generations:")
        for gen in AIGeneration.objects.all().order_by('-created_at')[:5]:
            print(f"   - {gen.title} ({gen.content_type}) - {gen.status}")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed")

if __name__ == '__main__':
    main()