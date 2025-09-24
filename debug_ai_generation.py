#!/usr/bin/env python
"""
Debug script to examine what the AI is actually generating
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')
django.setup()

from ai_generator.services import QuizGenerator
import json

def debug_ai_response():
    """Debug the raw AI response to see parsing issues"""
    print("🔍 Debug AI Generation Response")
    print("=" * 50)
    
    generator = QuizGenerator()
    
    # Create a simple test case
    content = '''Object-Oriented Programming is a programming paradigm based on the concept of objects. 
    Key principles include encapsulation, inheritance, and polymorphism. 
    Encapsulation bundles data and methods together.
    Inheritance allows classes to inherit properties from parent classes.
    Polymorphism enables objects of different types to be treated uniformly.'''
    
    # Test by calling the Gemini API directly to see raw response
    prompt = generator._create_quiz_prompt(
        content=content,
        language='en',
        num_questions=3,
        difficulty='medium',
        question_types=['multiple_choice', 'true_false']
    )
    
    print("📝 Generated Prompt (first 500 chars):")
    print("-" * 30)
    print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
    print("\n" + "=" * 50)
    
    # Get raw response from Gemini
    print("🤖 Getting raw AI response...")
    result = generator.gemini.generate_content(prompt)
    
    if result['success']:
        print("✅ AI Response received successfully")
        print(f"📊 Processing time: {result['processing_time']:.2f}s")
        print(f"🔢 Estimated tokens: {result['tokens_used']}")
        print("\n📄 Raw AI Response:")
        print("-" * 30)
        print(result['content'])
        print("\n" + "=" * 50)
        
        # Try to parse it manually
        print("🔧 Attempting to parse response...")
        try:
            parsed_result = generator._parse_quiz_response(result['content'])
            print("✅ Parsing successful!")
            print(f"📊 Quiz title: {parsed_result.get('title', 'N/A')}")
            print(f"📝 Questions found: {len(parsed_result.get('questions', []))}")
            
            if parsed_result.get('questions'):
                first_q = parsed_result['questions'][0]
                print(f"\n🎯 Sample question:")
                print(f"   Text: {first_q.get('question', 'N/A')[:100]}...")
                print(f"   Type: {first_q.get('type', 'N/A')}")
                if first_q.get('options'):
                    print(f"   Options: {len(first_q.get('options', []))} choices")
        except Exception as e:
            print(f"❌ Parsing failed: {str(e)}")
            print("🔧 This explains why fallback questions are being used.")
            
    else:
        print(f"❌ AI request failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    debug_ai_response()