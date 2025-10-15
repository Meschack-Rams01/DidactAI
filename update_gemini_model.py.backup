#!/usr/bin/env python
"""
Script to update Gemini model references and create new migrations
"""
import os
import django
from django.core.management import execute_from_command_line

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DidactAI_project.settings')
django.setup()

def main():
    print("ðŸ”„ Updating Gemini model references...")
    
    # Create migrations for the model changes
    print("ðŸ“ Creating new migrations...")
    
    try:
        # Create migrations for ai_generator app
        print("   - Creating ai_generator migration...")
        execute_from_command_line(['manage.py', 'makemigrations', 'ai_generator', '--name=update_gemini_model'])
        
        # Create migrations for core app  
        print("   - Creating core migration...")
        execute_from_command_line(['manage.py', 'makemigrations', 'core', '--name=update_gemini_model'])
        
        print("\n✅ Migrations created successfully!")
        print("\nNext steps:")
        print("1. Run: python manage.py migrate")
        print("2. Update existing records if needed")
        
        # Option to run migrations immediately
        response = input("\nDo you want to run migrations now? (y/N): ")
        if response.lower() in ['y', 'yes']:
            print("\nðŸ”„ Running migrations...")
            execute_from_command_line(['manage.py', 'migrate'])
            print("✅ Migrations applied successfully!")
            
            # Update existing records
            print("\nðŸ”„ Updating existing records...")
            update_existing_records()
            print("✅ Existing records updated!")
        
    except Exception as e:
        print(f"âŒ Error: {e}")
        print("You may need to run migrations manually:")
        print("   python manage.py makemigrations")
        print("   python manage.py migrate")

def update_existing_records():
    """Update existing records that still have the old model name"""
    from ai_generator.models import AIGeneration
    from core.models import GlobalSettings
    
    # Update AIGeneration records
    updated_count = AIGeneration.objects.filter(ai_model='gemini-pro').update(ai_model='gemini-1.5-flash')
    if updated_count > 0:
        print(f"   - Updated {updated_count} AIGeneration records")
    
    # Update GlobalSettings
    settings = GlobalSettings.get_settings()
    if settings.default_ai_model == 'gemini-pro':
        settings.default_ai_model = 'gemini-1.5-flash'
        settings.save()
        print("   - Updated GlobalSettings")

if __name__ == '__main__':
    main()
