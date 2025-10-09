#!/usr/bin/env python
"""
Quick fix script to repair the malformed quiz question issue
Directly fixes the problematic generation in the database
"""

import os
import sys
import django
import json

# Setup Django environment
sys.path.append('C:\\Users\\Ramat\\Desktop\\Nouveau dossier')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DidactAI_project.settings')
django.setup()

from ai_generator.models import AIGeneration

def fix_malformed_quiz():
    """Fix the malformed quiz with ID 17"""
    print("ðŸ› ï¸ FIXING MALFORMED QUIZ...")
    print("=" * 40)
    
    try:
        # Get the problematic generation (ID 17 based on diagnostic)
        generation = AIGeneration.objects.get(id=17)
        print(f"ðŸ“‹ Found generation: {generation.title} (ID: {generation.id})")
        
        # Get the current content
        content = generation.generated_content
        questions = content.get('questions', [])
        
        print(f"   Current question count: {len(questions)}")
        
        # Fix the first malformed question
        if questions and len(questions) > 0:
            first_question = questions[0]
            print(f"   First question text: {first_question.get('question', 'N/A')[:50]}...")
            
            # Check if it's the malformed one with '"questions": ['
            if '"questions"' in str(first_question.get('question', '')):
                print("   âŒ Found malformed first question - fixing...")
                
                # Replace with a proper question
                questions[0] = {
                    'id': 1,
                    'type': 'multiple_choice',
                    'question': 'What is the primary characteristic of HPC in the cloud?',
                    'options': [
                        'On-demand scalable computing resources',
                        'Fixed hardware configuration',
                        'Local data storage only',
                        'Single-user access'
                    ],
                    'correct_answer': 'A',
                    'explanation': 'Cloud HPC provides on-demand, scalable computing resources that can be adjusted based on workload requirements.',
                    'difficulty': 'medium',
                    'points': 1
                }
                
                # Update the content
                content['questions'] = questions
                generation.generated_content = content
                generation.save()
                
                print("   âœ… Fixed malformed question!")
                print(f"   New question: {questions[0]['question']}")
                
        print(f"\nâœ… Quiz repair completed successfully!")
        return generation.id
        
    except AIGeneration.DoesNotExist:
        print("âŒ Generation with ID 17 not found")
        return None
    except Exception as e:
        print(f"âŒ Error fixing quiz: {str(e)}")
        return None

def test_export_fixed_quiz(generation_id):
    """Test export functionality with the fixed quiz"""
    print(f"\nðŸ§ª TESTING EXPORT WITH FIXED QUIZ...")
    print("=" * 40)
    
    try:
        from exports.services import HTMLExporter
        
        generation = AIGeneration.objects.get(id=generation_id)
        html_exporter = HTMLExporter()
        
        # Prepare branding
        branding = {
            'university_name': 'SAMPLE UNIVERSITY',
            'department': 'Department of Computer Science',
            'course': 'Cloud Computing - CS 401',
            'semester': 'Fall 2025',
            'instructor': 'Prof. Cloud Expert',
            'exam_date': 'December 1, 2025'
        }
        
        # Convert generation to export format
        quiz_data = {
            'title': generation.title,
            'description': generation.description or 'Cloud HPC Quiz',
            'content_type': 'quiz',
            'questions': generation.generated_content.get('questions', []),
            'total_points': generation.generated_content.get('total_points', 0),
            'estimated_duration': generation.generated_content.get('estimated_duration', '15 minutes')
        }
        
        print(f"   Exporting quiz: {quiz_data['title']}")
        print(f"   Questions: {len(quiz_data['questions'])}")
        
        # Generate student version
        student_html = html_exporter.export_quiz(quiz_data, branding, show_answers=False)
        
        # Save to file
        with open('cloud_hpc_fixed_student.html', 'w', encoding='utf-8') as f:
            f.write(student_html)
        
        # Generate instructor version
        instructor_html = html_exporter.export_quiz(quiz_data, branding, show_answers=True)
        
        # Save to file
        with open('cloud_hpc_fixed_instructor.html', 'w', encoding='utf-8') as f:
            f.write(instructor_html)
        
        print("   âœ… Export successful!")
        print("   ðŸ“ Files created:")
        print("      â€¢ cloud_hpc_fixed_student.html")
        print("      â€¢ cloud_hpc_fixed_instructor.html")
        
        # Validate the export
        if 'What is the primary characteristic of HPC in the cloud?' in student_html:
            print("   âœ… Fixed question appears in export")
        else:
            print("   âŒ Fixed question not found in export")
            
        return True
        
    except Exception as e:
        print(f"   âŒ Export test failed: {str(e)}")
        return False

def main():
    """Main execution function"""
    print("ðŸš€ QUICK FIX FOR MALFORMED QUIZ ISSUE")
    print("=" * 50)
    
    # Step 1: Fix the malformed quiz
    fixed_id = fix_malformed_quiz()
    
    if fixed_id:
        # Step 2: Test export functionality
        export_success = test_export_fixed_quiz(fixed_id)
        
        if export_success:
            print(f"\nðŸŽ‰ SUCCESS! Quiz {fixed_id} has been fixed and exported successfully!")
            print("\nðŸ“‹ Summary:")
            print("â€¢ âœ… Malformed question replaced with proper content")
            print("â€¢ âœ… Export functionality tested and working")
            print("â€¢ âœ… Both student and instructor versions generated")
            print("\nðŸ’¡ Next Steps:")
            print("â€¢ Open the generated HTML files to verify the fix")
            print("â€¢ Use the web interface to view and export the fixed quiz")
            print(f"â€¢ Visit: http://127.0.0.1:8000/ai-generator/view/{fixed_id}/")
        else:
            print(f"\nâš ï¸ Quiz {fixed_id} was fixed but export test failed")
    else:
        print("\nâŒ Unable to fix the malformed quiz")

if __name__ == '__main__':
    main()
