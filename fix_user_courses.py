#!/usr/bin/env python
"""
Script to fix user courses issue - create courses for the current user
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DidactAI_project.settings')
django.setup()

def fix_user_courses():
    print("ðŸ”§ Fixing user courses issue...")
    
    try:
        from courses.models import Course
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        # Show all users and their courses
        users = User.objects.all()
        print("ðŸ‘¥ All users and their courses:")
        for i, user in enumerate(users, 1):
            user_courses = Course.objects.filter(instructor=user)
            print(f"   {i}. {user.get_full_name() or user.username} ({user.email}) - {user_courses.count()} courses")
            for course in user_courses:
                print(f"      - {course.title}")
        
        if not users.exists():
            print("âŒ No users found!")
            return False
        
        # Find users without courses
        users_without_courses = []
        for user in users:
            if Course.objects.filter(instructor=user).count() == 0:
                users_without_courses.append(user)
        
        if users_without_courses:
            print(f"\nðŸ‘¤ Users without courses ({len(users_without_courses)}):")
            for i, user in enumerate(users_without_courses, 1):
                print(f"   {i}. {user.get_full_name() or user.username} ({user.email})")
            
            # Ask which user to create courses for
            print(f"\nðŸ“ Which user needs courses? (1-{len(users_without_courses)}, or 0 to skip): ", end="")
            choice = input()
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(users_without_courses):
                    selected_user = users_without_courses[choice_num - 1]
                    
                    # Create sample courses for the selected user
                    sample_courses = [
                        {
                            'title': 'Introduction to Computer Science',
                            'code': 'CS101',
                            'description': 'Basic concepts of computer science and programming',
                            'credits': 3
                        },
                        {
                            'title': 'Advanced Quantum Physics',
                            'code': 'PHYS301', 
                            'description': 'Advanced topics in quantum mechanics and physics',
                            'credits': 4
                        },
                        {
                            'title': 'Mathematics for Engineers',
                            'code': 'MATH201',
                            'description': 'Mathematical concepts essential for engineering',
                            'credits': 3
                        }
                    ]
                    
                    created_courses = []
                    for course_data in sample_courses:
                        course = Course.objects.create(
                            instructor=selected_user,
                            **course_data
                        )
                        created_courses.append(course)
                        print(f"âœ… Created course: {course.title} ({course.code})")
                    
                    print(f"\nðŸŽ‰ Successfully created {len(created_courses)} courses for {selected_user.get_full_name() or selected_user.username}!")
                    print("   The courses should now appear in the AI Exam Generator dropdown.")
                    
                elif choice_num == 0:
                    print("  Skipping course creation.")
                else:
                    print("âŒ Invalid choice.")
            except ValueError:
                print("âŒ Invalid input. Please enter a number.")
        else:
            print("âœ… All users have courses!")
            
        # Show final state
        print(f"\nðŸ“Š Final course summary:")
        all_courses = Course.objects.all()
        print(f"   Total courses: {all_courses.count()}")
        for user in users:
            user_courses = Course.objects.filter(instructor=user)
            if user_courses.count() > 0:
                print(f"   {user.get_full_name() or user.username}: {user_courses.count()} courses")
        
    except Exception as e:
        print(f"âŒ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    fix_user_courses()
