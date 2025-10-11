#!/usr/bin/env python
"""
Data migration script to fix existing question types in database
This script updates all QuizQuestion records to use the standardized question type names
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
django.setup()

from ai_generator.models import QuizQuestion
from django.db import transaction

def fix_question_types():
    """Fix all existing question types in the database"""
    
    # Mapping of old question types to new standardized ones
    question_type_mapping = {
        'mcq': 'multiple_choice',
        'mc': 'multiple_choice',
        'multiple_choice': 'multiple_choice',  # Already correct
        'true_false': 'true_false',  # Already correct
        'tf': 'true_false',
        'short_answer': 'short_answer',  # Already correct
        'short': 'short_answer',
        'sa': 'short_answer',
        'long_answer': 'essay',
        'essay': 'essay',  # Already correct
        'long': 'essay',
        'fill_blank': 'fill_blank',  # Already correct
        'fill_in_blank': 'fill_blank',
        'fill_in_the_blank': 'fill_blank',
        'fillblank': 'fill_blank',
        'matching': 'matching',  # Already correct
        'ordering': 'ordering',  # Already correct
        'order': 'ordering',
    }
    
    print("=== Fixing Question Types in Database ===\n")
    
    # Get all questions
    all_questions = QuizQuestion.objects.all()
    total_questions = all_questions.count()
    print(f"Found {total_questions} questions in database")
    
    if total_questions == 0:
        print("No questions to fix.")
        return
    
    # Count questions by type before fixing
    print("\n--- Question Types BEFORE fixing ---")
    type_counts_before = {}
    for question in all_questions:
        q_type = question.question_type
        type_counts_before[q_type] = type_counts_before.get(q_type, 0) + 1
    
    for q_type, count in type_counts_before.items():
        print(f"  {q_type}: {count}")
    
    # Fix question types
    fixed_count = 0
    
    with transaction.atomic():
        for question in all_questions:
            old_type = question.question_type
            new_type = question_type_mapping.get(old_type, old_type)
            
            if old_type != new_type:
                question.question_type = new_type
                question.save(update_fields=['question_type'])
                fixed_count += 1
                print(f"✅ Fixed question {question.id}: '{old_type}' → '{new_type}'")
    
    print(f"\n✅ Fixed {fixed_count} questions")
    
    # Count questions by type after fixing
    print("\n--- Question Types AFTER fixing ---")
    all_questions_after = QuizQuestion.objects.all()
    type_counts_after = {}
    for question in all_questions_after:
        q_type = question.question_type
        type_counts_after[q_type] = type_counts_after.get(q_type, 0) + 1
    
    for q_type, count in type_counts_after.items():
        print(f"  {q_type}: {count}")
    
    print(f"\n=== Database Fix Complete ===")
    print(f"Total questions processed: {total_questions}")
    print(f"Questions updated: {fixed_count}")
    print(f"Questions unchanged: {total_questions - fixed_count}")

if __name__ == '__main__':
    fix_question_types()