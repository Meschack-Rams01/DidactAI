#!/usr/bin/env python3
"""
Create default AI generation templates for DidactAI.

This script creates system-level templates that will be available to all users.
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
django.setup()

from ai_generator.models import GenerationTemplate
from accounts.models import CustomUser

def create_default_templates():
    """Create default generation templates."""
    
    # Get or create a system user
    system_user, created = CustomUser.objects.get_or_create(
        username='system',
        defaults={
            'email': 'system@didactai.com',
            'first_name': 'System',
            'last_name': 'Admin',
            'is_active': True,
            'role': 'admin'
        }
    )
    
    templates = [
        {
            'name': 'Basic Quiz Template',
            'template_type': 'quiz',
            'description': 'Generate a basic multiple-choice quiz from course content.',
            'prompt_template': '''Create a {num_questions} question multiple-choice quiz based on the following content. 
Make the questions {difficulty} difficulty level.

Content:
{content}

Requirements:
- Each question should have 4 options (A, B, C, D)
- Only one correct answer per question
- Include explanations for correct answers
- Questions should test understanding, not just memorization
- Vary question types (factual, analytical, application-based)

Language: {language}

Format the response as JSON with this structure:
{
    "quiz": {
        "title": "Quiz Title",
        "questions": [
            {
                "question": "Question text",
                "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                "correct_answer": "A",
                "explanation": "Why this answer is correct"
            }
        ]
    }
}''',
            'parameters': {
                'num_questions': 10,
                'difficulty': 'medium',
                'language': 'English'
            }
        },
        
        {
            'name': 'Comprehensive Exam Template',
            'template_type': 'exam',
            'description': 'Generate a comprehensive exam with mixed question types.',
            'prompt_template': '''Create a comprehensive exam with {num_questions} questions based on the following content.
Include a mix of question types: multiple choice, true/false, and short answer questions.
Difficulty level: {difficulty}

Content:
{content}

Requirements:
- 60% multiple choice (4 options each)
- 25% true/false questions
- 15% short answer questions
- Include point values for each question
- Provide detailed answer keys
- Questions should comprehensively cover the material

Language: {language}
Duration: {duration} minutes

Format the response as JSON with this structure:
{
    "exam": {
        "title": "Exam Title",
        "duration": "{duration}",
        "total_points": 100,
        "sections": [
            {
                "section_name": "Multiple Choice",
                "questions": [...],
                "instructions": "Choose the best answer"
            }
        ]
    }
}''',
            'parameters': {
                'num_questions': 25,
                'difficulty': 'medium',
                'language': 'English',
                'duration': 90
            }
        },
        
        {
            'name': 'Course Syllabus Template',
            'template_type': 'syllabus',
            'description': 'Generate a structured course syllabus.',
            'prompt_template': '''Create a detailed course syllabus based on the provided course content and information.

Course Information:
{content}

Requirements:
- Course title, code, and credits
- Course description and objectives
- Weekly schedule breakdown
- Assessment methods and grading rubric
- Required materials and resources
- Course policies and expectations
- Learning outcomes

Duration: {duration} weeks
Language: {language}

Format the response as JSON with this structure:
{
    "syllabus": {
        "course_info": {...},
        "description": "...",
        "objectives": [...],
        "schedule": {...},
        "assessment": {...},
        "policies": {...}
    }
}''',
            'parameters': {
                'duration': 16,
                'language': 'English'
            }
        },
        
        {
            'name': 'Flashcards Template',
            'template_type': 'flashcards',
            'description': 'Generate study flashcards for key concepts.',
            'prompt_template': '''Create {num_cards} flashcards based on the following content.
Focus on key concepts, definitions, and important facts.

Content:
{content}

Requirements:
- Clear, concise questions on the front
- Detailed answers on the back
- Cover the most important concepts
- Vary difficulty levels
- Include both factual and conceptual cards

Language: {language}

Format the response as JSON with this structure:
{
    "flashcards": {
        "title": "Flashcard Set Title",
        "cards": [
            {
                "front": "Question or concept",
                "back": "Answer or explanation",
                "category": "concept_category"
            }
        ]
    }
}''',
            'parameters': {
                'num_cards': 20,
                'language': 'English'
            }
        },
        
        {
            'name': 'Content Summary Template',
            'template_type': 'summary',
            'description': 'Generate concise summaries of course content.',
            'prompt_template': '''Create a comprehensive summary of the following content.
Length: {length} ({summary_type})

Content:
{content}

Requirements:
- Organize by main topics and subtopics
- Include key points and important details
- Use clear, readable formatting
- Maintain academic tone
- Highlight critical concepts
- Include relevant examples where applicable

Language: {language}

Format the response as JSON with this structure:
{
    "summary": {
        "title": "Summary Title",
        "main_topics": [
            {
                "topic": "Topic Name",
                "key_points": [...],
                "details": "...",
                "examples": [...]
            }
        ],
        "conclusion": "..."
    }
}''',
            'parameters': {
                'length': 'medium',
                'summary_type': '2-3 pages',
                'language': 'English'
            }
        }
    ]
    
    created_templates = []
    
    for template_data in templates:
        template, created = GenerationTemplate.objects.get_or_create(
            name=template_data['name'],
            template_type=template_data['template_type'],
            defaults={
                'description': template_data['description'],
                'prompt_template': template_data['prompt_template'],
                'parameters': template_data['parameters'],
                'is_system_template': True,
                'is_active': True,
                'created_by': system_user
            }
        )
        
        if created:
            created_templates.append(template.name)
            print(f"✅ Created template: {template.name}")
        else:
            print(f"⚠️  Template already exists: {template.name}")
    
    return created_templates

def main():
    """Main function."""
    print("🎯 Creating Default Generation Templates")
    print("=" * 50)
    
    try:
        created_templates = create_default_templates()
        
        print(f"\n📊 Summary:")
        print(f"Templates created: {len(created_templates)}")
        
        if created_templates:
            print(f"\n✅ Successfully created default templates!")
            print("These templates are now available in the Django admin:")
            print("http://127.0.0.1:8000/admin/ai_generator/generationtemplate/")
        else:
            print(f"\n✅ All default templates already exist!")
            
    except Exception as e:
        print(f"❌ Error creating templates: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())