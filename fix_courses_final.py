#!/usr/bin/env python
"""
Fixed script to create courses for users (using correct field names)
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DidactAI_project.settings')
django.setup()

def fix_courses_final():
    print("ðŸ”§ Creating courses for users...")
    
    try:
        from courses.models import Course
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        # Show all users and their courses
        users = User.objects.all()
        print("ðŸ‘¥ Current users and their courses:")
        for i, user in enumerate(users, 1):
            user_courses = Course.objects.filter(instructor=user)
            print(f"   {i}. {user.get_full_name() or user.username} ({user.email}) - {user_courses.count()} courses")
        
        # Find users without courses
        users_without_courses = []
        for user in users:
            if Course.objects.filter(instructor=user).count() == 0:
                users_without_courses.append(user)
        
        if users_without_courses:
            print(f"\nðŸ‘¤ Users without courses:")
            for i, user in enumerate(users_without_courses, 1):
                print(f"   {i}. {user.get_full_name() or user.username} ({user.email})")
            
            # Create courses for the first user without courses (likely the current user)
            user_to_fix = users_without_courses[0]  # Usually the current logged-in user
            print(f"\nðŸ“ Creating courses for: {user_to_fix.get_full_name() or user_to_fix.username}")
            
            # Create sample courses using correct field names from the model
            sample_courses = [
                {
                    'instructor': user_to_fix,
                    'title': 'Introduction to Computer Science',
                    'course_code': 'CS101',
                    'description': 'Basic concepts of computer science and programming',
                    'department': 'Computer Science',
                    'credits': 3,
                    'status': 'active'
                },
                {
                    'instructor': user_to_fix,
                    'title': 'Advanced Mathematics',
                    'course_code': 'MATH301', 
                    'description': 'Advanced mathematical concepts and applications',
                    'department': 'Mathematics',
                    'credits': 4,
                    'status': 'active'
                },
                {
                    'instructor': user_to_fix,
                    'title': 'Physics Fundamentals',
                    'course_code': 'PHYS201',
                    'description': 'Core principles of physics and their applications',
                    'department': 'Physics',
                    'credits': 3,
                    'status': 'active'
                }
            ]
            
            created_courses = []
            for course_data in sample_courses:
                try:
                    course = Course.objects.create(**course_data)
                    created_courses.append(course)
                    print(f"✅ Created: {course.title} ({course.course_code})")
                except Exception as e:
                    print(f"âŒ Error creating {course_data['title']}: {e}")
            
            print(f"\n🎉 Successfully created {len(created_courses)} courses!")
            print(f"   User {user_to_fix.get_full_name() or user_to_fix.username} now has {Course.objects.filter(instructor=user_to_fix).count()} courses")
            
        else:
            print("✅ All users already have courses!")
        
        # Test the view logic
        print(f"\n🐧ª Testing exam generator view logic...")
        for user in users:
            user_courses = Course.objects.filter(instructor=user)
            if user_courses.count() > 0:
                print(f"✅ {user.get_full_name() or user.username}: {user_courses.count()} courses available")
                for course in user_courses:
                    print(f"    - {course.full_course_name}")
        
        # Show final summary
        all_courses = Course.objects.all()
        print(f"\nðŸ“Š Final Summary:")
        print(f"   Total users: {users.count()}")
        print(f"   Total courses: {all_courses.count()}")
        print(f"   Users with courses: {users.filter(courses__isnull=False).distinct().count()}")
        
        print(f"\n✅ Fix applied! The courses should now appear in the AI Exam Generator dropdown.")
        print(f"   Please refresh the page: http://127.0.0.1:8000/ai-generator/exam/")
        
    except Exception as e:
        print(f"âŒ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    fix_courses_final()
