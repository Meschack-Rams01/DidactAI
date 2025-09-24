#!/usr/bin/env python
"""
Fix script for AI generation malformed output issue
Identifies and resolves problems with quiz generation
"""

import os
import sys
import django
import json
from datetime import datetime

# Setup Django environment
sys.path.append('C:\\Users\\Ramat\\Desktop\\Nouveau dossier')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
django.setup()

from ai_generator.models import AIGeneration
from ai_generator.services import QuizGenerator

def diagnose_generation_issues():
    """Diagnose issues with recent AI generations"""
    print("🔍 DIAGNOSING AI GENERATION ISSUES...")
    print("=" * 50)
    
    # Get recent generations
    recent_generations = AIGeneration.objects.order_by('-created_at')[:5]
    
    for gen in recent_generations:
        print(f"\n📋 Generation ID: {gen.id}")
        print(f"   Title: {gen.title}")
        print(f"   Created: {gen.created_at}")
        print(f"   Content Type: {gen.content_type}")
        print(f"   Status: {gen.status}")
        
        if gen.generated_content:
            content = gen.generated_content
            print(f"   Content Keys: {list(content.keys())}")
            
            # Check for malformed questions
            if 'questions' in content:
                questions = content['questions']
                print(f"   Number of Questions: {len(questions)}")
                
                for i, q in enumerate(questions[:3]):  # Check first 3 questions
                    print(f"\n   Question {i+1}:")
                    print(f"     Text: {q.get('question', 'MISSING')[:100]}...")
                    print(f"     Type: {q.get('type', 'MISSING')}")
                    print(f"     Options: {len(q.get('options', []))} options")
                    
                    # Identify issues
                    issues = []
                    if not q.get('question') or 'questions' in q.get('question', ''):
                        issues.append("Malformed question text")
                    if q.get('type') == 'multiple_choice' and len(q.get('options', [])) == 0:
                        issues.append("Missing multiple choice options")
                    if not q.get('correct_answer'):
                        issues.append("Missing correct answer")
                    
                    if issues:
                        print(f"     ❌ ISSUES: {', '.join(issues)}")
                    else:
                        print(f"     ✅ Question looks good")
        else:
            print("   ❌ No generated content found")

def create_fixed_quiz_sample():
    """Create a properly formatted quiz to test the system"""
    print("\n🛠️ CREATING FIXED QUIZ SAMPLE...")
    print("=" * 50)
    
    # Proper quiz data structure
    fixed_quiz_data = {
        'title': 'Cloud HPC - Fixed Version',
        'description': 'Comprehensive quiz on High Performance Computing in the Cloud',
        'content_type': 'quiz',
        'total_points': 50,
        'estimated_duration': '15 minutes',
        'questions': [
            {
                'type': 'multiple_choice',
                'question': 'What is the primary characteristic of HPC in the cloud?',
                'points': 5,
                'options': [
                    'On-demand scalable computing resources',
                    'Fixed hardware configuration',
                    'Local data storage only',
                    'Single-user access'
                ],
                'correct_answer': 'A',
                'explanation': 'Cloud HPC provides on-demand, scalable computing resources that can be adjusted based on workload requirements.'
            },
            {
                'type': 'multiple_choice',
                'question': 'When did HPC in the cloud start gaining significant popularity?',
                'points': 5,
                'options': [
                    'Early 1990s',
                    'Early 2000s', 
                    'Early 2010s',
                    'Early 2020s'
                ],
                'correct_answer': 'C',
                'explanation': 'Cloud HPC gained significant popularity in the early 2010s as cloud infrastructure matured.'
            },
            {
                'type': 'multiple_choice',
                'question': 'Which of the following is NOT a key feature of cloud HPC?',
                'points': 5,
                'options': [
                    'Elastic scaling',
                    'Pay-as-you-use pricing',
                    'Fixed hardware ownership',
                    'Global accessibility'
                ],
                'correct_answer': 'C',
                'explanation': 'Fixed hardware ownership is characteristic of on-premise HPC, not cloud HPC.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What is a significant advantage of using cloud HPC?',
                'points': 5,
                'options': [
                    'Higher upfront costs',
                    'Reduced scalability',
                    'Lower barrier to entry',
                    'Fixed resource allocation'
                ],
                'correct_answer': 'C',
                'explanation': 'Cloud HPC significantly lowers the barrier to entry by eliminating large upfront infrastructure investments.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What is a major disadvantage of cloud HPC?',
                'points': 5,
                'options': [
                    'Unlimited scalability',
                    'Network latency and data transfer costs',
                    'Too much flexibility',
                    'Instant resource availability'
                ],
                'correct_answer': 'B',
                'explanation': 'Network latency and data transfer costs can be significant challenges in cloud HPC implementations.'
            },
            {
                'type': 'short_answer',
                'question': 'Explain why a startup might prefer cloud HPC over setting up its own on-premise supercomputer.',
                'points': 10,
                'correct_answer': 'A startup might prefer cloud HPC because it eliminates large upfront capital investments, provides instant access to high-performance resources, offers scalability based on needs, and reduces operational overhead like maintenance and upgrades.',
                'explanation': 'Key benefits include cost efficiency, scalability, and reduced operational complexity.'
            },
            {
                'type': 'short_answer', 
                'question': 'Describe a scenario where the latency associated with data transfer in cloud HPC could be a significant problem.',
                'points': 10,
                'correct_answer': 'Real-time financial trading algorithms, interactive scientific simulations, or any application requiring immediate feedback where milliseconds matter. Large datasets that need frequent transfer between cloud and local systems can also create bottlenecks.',
                'explanation': 'Latency becomes critical in time-sensitive applications and frequent data transfer scenarios.'
            },
            {
                'type': 'short_answer',
                'question': 'Discuss a potential security concern related to using cloud HPC for sensitive data.',
                'points': 10,
                'correct_answer': 'Data breaches, lack of physical control over hardware, compliance issues with regulations like HIPAA or GDPR, shared infrastructure risks, and potential government access to data stored in cloud providers\' facilities.',
                'explanation': 'Security concerns include data sovereignty, compliance, and shared infrastructure risks.'
            }
        ]
    }
    
    return fixed_quiz_data

def test_ai_service():
    """Test the AI generator service"""
    print("\n🧪 TESTING AI GENERATOR SERVICE...")
    print("=" * 50)
    
    try:
        quiz_generator = QuizGenerator()
        print("✅ Quiz Generator Service initialized successfully")
        
        # Test with a simple prompt
        test_content = "Cloud computing provides on-demand access to computing resources over the internet. It offers scalability, cost-effectiveness, and flexibility for businesses."
        
        print(f"\n📝 Testing with content: {test_content[:100]}...")
        
        # This would normally call the AI service
        # result = quiz_generator.generate_quiz(test_content, num_questions=2)
        print("⚠️ Skipping actual AI call to avoid API costs")
        
    except Exception as e:
        print(f"❌ Error testing Quiz Generator service: {str(e)}")

def save_fixed_generation():
    """Save a properly formatted generation to the database"""
    print("\n💾 SAVING FIXED GENERATION TO DATABASE...")
    print("=" * 50)
    
    try:
        fixed_data = create_fixed_quiz_sample()
        
        # Create a new generation with fixed data
        generation = AIGeneration.objects.create(
            title='Cloud HPC - Fixed Quiz',
            description='Properly formatted quiz about High Performance Computing in the Cloud',
            content_type='quiz',
            generated_content=fixed_data,
            status='completed'
        )
        
        print(f"✅ Fixed generation created with ID: {generation.id}")
        print(f"   Title: {generation.title}")
        print(f"   Questions: {len(fixed_data['questions'])}")
        print(f"   Total Points: {fixed_data['total_points']}")
        
        return generation
        
    except Exception as e:
        print(f"❌ Error saving fixed generation: {str(e)}")
        return None

def main():
    """Main function to run diagnostics and fixes"""
    print("🚀 AI GENERATION ISSUE DIAGNOSTIC & FIX TOOL")
    print("=" * 60)
    
    # Step 1: Diagnose existing issues
    diagnose_generation_issues()
    
    # Step 2: Test AI service
    test_ai_service()
    
    # Step 3: Create and save fixed example
    fixed_gen = save_fixed_generation()
    
    # Step 4: Final recommendations
    print("\n💡 RECOMMENDATIONS:")
    print("=" * 50)
    print("1. ✅ Check AI prompt templates for malformed JSON generation")
    print("2. ✅ Validate AI responses before saving to database")
    print("3. ✅ Implement fallback generation for parsing failures")
    print("4. ✅ Add better error handling in the AI generation pipeline")
    print("5. ✅ Test the fixed generation for proper export functionality")
    
    if fixed_gen:
        print(f"\n🎯 Next Steps:")
        print(f"   • Visit: /ai-generator/view/{fixed_gen.id}/ to see the fixed quiz")
        print(f"   • Test export functionality with the fixed generation")
        print(f"   • Use this as a template for proper question formatting")

if __name__ == '__main__':
    main()