#!/usr/bin/env python
"""
Demonstration of Enhanced Export Features

This script creates a sample export using all the new enhanced features:
- Complete university branding hierarchy
- Student information fields
- Professional formatting
- Multiple question types
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DidactAI_project.settings')
django.setup()

from exports.services import ExportService, PDFExporter, HTMLExporter
from datetime import datetime

def create_enhanced_demo_export():
    """Create a demonstration export with all enhanced features"""
    
    print("🍎“ Creating Enhanced University Export Demo")
    print("=" * 50)
    
    # Complete university branding configuration
    enhanced_branding = {
        # University hierarchy
        'university_name': 'Harvard University',
        'faculty': 'Faculty of Arts and Sciences',
        'department': 'Department of Computer Science',
        'course': 'CS 171 - Visualization',
        
        # Academic information
        'academic_year': '2024-2025',
        'semester': 'Fall Semester',
        'instructor': 'Prof. Hanspeter Pfister',
        'exam_date': '2024-12-15',
        
        # Additional customization
        'additional_notes': 'Please ensure all visualizations are clearly labeled and include proper citations for data sources.',
        'watermark': 'CONFIDENTIAL - Harvard University',
        
        # Student information configuration
        'student_info': {
            'include_student_name': True,
            'include_student_id': True, 
            'include_signature': True,
            'include_date_field': True
        },
        
        # Logo configuration
        'has_logo': True,
        'logo_filename': 'harvard_logo.png'
    }
    
    # Comprehensive exam content
    enhanced_quiz_data = {
        'title': 'Final Examination - Data Visualization and Interactive Systems',
        'description': 'This examination covers fundamental concepts in data visualization, interaction design, and visual analytics systems.',
        'content_type': 'exam',
        'estimated_duration': '3 hours',
        'total_points': 100,
        'questions': [
            {
                'type': 'multiple_choice',
                'question': 'Which of the following best describes the purpose of data visualization in exploratory data analysis?',
                'options': [
                    'To create aesthetically pleasing graphics for presentations',
                    'To reveal patterns, trends, and relationships that might not be apparent in raw data',
                    'To reduce the amount of data that needs to be processed',
                    'To replace statistical analysis entirely'
                ],
                'correct_answer': 'B',
                'points': 5,
                'difficulty': 'medium',
                'explanation': 'Data visualization in EDA helps reveal patterns and relationships in data that may not be obvious from looking at raw numbers.'
            },
            {
                'type': 'true_false',
                'question': 'The principle of proportional ink states that the size of graphical elements should be proportional to the data values they represent.',
                'correct_answer': 'True',
                'points': 3,
                'difficulty': 'easy',
                'explanation': 'This is one of Tufte\'s fundamental principles of effective data visualization.'
            },
            {
                'type': 'multiple_choice',
                'question': 'In the context of interaction design for visualizations, what does "brushing and linking" refer to?',
                'options': [
                    'A technique for cleaning messy datasets',
                    'Selecting data points in one view to highlight corresponding points in other views',
                    'A method for creating smooth animations between different chart types',
                    'The process of connecting multiple databases for visualization'
                ],
                'correct_answer': 'B',
                'points': 8,
                'difficulty': 'medium'
            },
            {
                'type': 'short_answer',
                'question': 'Explain the difference between diverging and sequential color scales, and provide an example of when you would use each.',
                'correct_answer': 'Sequential scales show progression from low to high values (e.g., population density). Diverging scales show deviation from a central value with two different hues (e.g., temperature anomalies).',
                'points': 12,
                'difficulty': 'medium'
            },
            {
                'type': 'essay',
                'question': 'Discuss the challenges of visualizing high-dimensional data and describe at least three techniques that can be used to address these challenges. Include specific examples of when each technique would be most appropriate.',
                'correct_answer': 'Challenges include curse of dimensionality, perceptual limitations, and cognitive overload. Techniques include: 1) Dimensionality reduction (PCA, t-SNE), 2) Parallel coordinates for showing multiple dimensions simultaneously, 3) Small multiples for comparing across dimensions.',
                'points': 20,
                'difficulty': 'hard'
            },
            {
                'type': 'fill_blank',
                'question': 'The _______ grammar of graphics provides a systematic approach to creating visualizations by mapping data variables to visual properties.',
                'correct_answer': 'layered',
                'points': 4,
                'difficulty': 'easy'
            },
            {
                'type': 'multiple_choice',
                'question': 'Which visualization type is most appropriate for showing the relationship between three continuous variables?',
                'options': [
                    'Bar chart',
                    'Scatter plot matrix',
                    'Bubble chart',
                    'Parallel coordinates'
                ],
                'correct_answer': 'C',
                'points': 6,
                'difficulty': 'medium'
            },
            {
                'type': 'short_answer',
                'question': 'What are the key considerations when designing visualizations for mobile devices versus desktop displays?',
                'correct_answer': 'Mobile considerations include smaller screen size, touch interactions, limited attention span, and the need for simplified interfaces with larger touch targets.',
                'points': 10,
                'difficulty': 'medium'
            },
            {
                'type': 'true_false',
                'question': 'Color should never be the only method used to convey important information in a visualization.',
                'correct_answer': 'True',
                'points': 3,
                'difficulty': 'easy',
                'explanation': 'This ensures accessibility for colorblind users and follows universal design principles.'
            },
            {
                'type': 'essay',
                'question': 'Analyze the ethical implications of data visualization design choices. How can visualization designers ensure their work promotes understanding rather than misleading audiences? Provide specific examples of both responsible and irresponsible visualization practices.',
                'correct_answer': 'Ethical considerations include accurate representation of data, appropriate scale selection, clear labeling, and avoiding cherry-picking. Examples include using zero baselines for bar charts vs. truncated y-axes that exaggerate differences.',
                'points': 29,
                'difficulty': 'hard'
            }
        ]
    }
    
    print("ðŸ“Š Sample exam content prepared:")
    print(f"   &bull; Title: {enhanced_quiz_data['title']}")
    print(f"   &bull; Questions: {len(enhanced_quiz_data['questions'])}")
    print(f"   &bull; Total Points: {enhanced_quiz_data['total_points']}")
    print(f"   &bull; Duration: {enhanced_quiz_data['estimated_duration']}")
    
    print(f"\nðŸ« University branding configured:")
    print(f"   &bull; University: {enhanced_branding['university_name']}")
    print(f"   &bull; Faculty: {enhanced_branding['faculty']}")
    print(f"   &bull; Department: {enhanced_branding['department']}")
    print(f"   &bull; Course: {enhanced_branding['course']}")
    print(f"   &bull; Academic Year: {enhanced_branding['academic_year']}")
    print(f"   &bull; Semester: {enhanced_branding['semester']}")
    
    print(f"\nðŸ“‹ Student information fields:")
    student_info = enhanced_branding['student_info']
    print(f"   &bull; Student Name: {'âœ“' if student_info['include_student_name'] else 'âœ—'}")
    print(f"   &bull; Student ID: {'âœ“' if student_info['include_student_id'] else 'âœ—'}")
    print(f"   &bull; Signature: {'âœ“' if student_info['include_signature'] else 'âœ—'}")
    print(f"   &bull; Date Field: {'âœ“' if student_info['include_date_field'] else 'âœ—'}")
    
    # Generate exports in all formats
    formats_to_test = ['pdf', 'html', 'docx']
    
    for export_format in formats_to_test:
        print(f"\nðŸ”„ Generating {export_format.upper()} export...")
        
        try:
            if export_format == 'pdf':
                exporter = PDFExporter()
                result_buffer = exporter.export_quiz(enhanced_quiz_data, enhanced_branding)
                
                filename = f'enhanced_demo_harvard_exam.pdf'
                with open(filename, 'wb') as f:
                    f.write(result_buffer.getvalue())
                
                print(f"   ✅ PDF exported successfully")
                print(f"   ðŸ“„ File: {filename} ({len(result_buffer.getvalue())} bytes)")
                
            elif export_format == 'html':
                exporter = HTMLExporter()
                html_content = exporter.export_quiz(enhanced_quiz_data, enhanced_branding)
                
                filename = f'enhanced_demo_harvard_exam.html'
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"   ✅ HTML exported successfully")
                print(f"   ðŸ“„ File: {filename} ({len(html_content)} characters)")
                
            elif export_format == 'docx' and 'DOCXExporter' in globals():
                from exports.services import DOCXExporter
                exporter = DOCXExporter()
                result_buffer = exporter.export_quiz(enhanced_quiz_data, enhanced_branding)
                
                filename = f'enhanced_demo_harvard_exam.docx'
                with open(filename, 'wb') as f:
                    f.write(result_buffer.getvalue())
                
                print(f"   ✅ DOCX exported successfully")
                print(f"   ðŸ“„ File: {filename} ({len(result_buffer.getvalue())} bytes)")
                
        except Exception as e:
            print(f"   âŒ {export_format.upper()} export failed: {str(e)}")
    
    # Test multiple versions
    print(f"\nðŸ“š Generating multiple versions (A/B/C)...")
    try:
        export_service = ExportService()
        zip_result = export_service.export_content(
            content_data=enhanced_quiz_data,
            export_format='zip',
            branding=enhanced_branding,
            versions=['A', 'B', 'C']
        )
        
        if zip_result['success']:
            zip_filename = 'enhanced_demo_harvard_versions.zip'
            with open(zip_filename, 'wb') as f:
                f.write(zip_result['file_data'])
            
            print(f"   ✅ Multiple versions created successfully")
            print(f"   ðŸ“¦ File: {zip_filename} ({len(zip_result['file_data'])} bytes)")
        else:
            print(f"   âŒ Multiple versions failed: {zip_result.get('error')}")
            
    except Exception as e:
        print(f"   âŒ Multiple versions failed: {str(e)}")
    
    print(f"\n" + "=" * 50)
    print("🎉 Enhanced Export Demo Complete!")
    print("\nðŸ“ Generated files:")
    print("   &bull; enhanced_demo_harvard_exam.pdf")
    print("   &bull; enhanced_demo_harvard_exam.html")
    print("   &bull; enhanced_demo_harvard_exam.docx")
    print("   &bull; enhanced_demo_harvard_versions.zip")
    
    print(f"\nâœ¨ Features demonstrated:")
    print("   ðŸ« Complete university branding hierarchy")
    print("   ðŸ‘¤ Student information fields")
    print("   ðŸ“Š Professional exam formatting")
    print("   🍎¨ Multiple export formats")
    print("   ðŸ“š A/B/C version generation")
    print("   ðŸ“‹ Mixed question types")
    print("   ðŸ” Watermark and security features")
    
    print(f"\nðŸ“– To use these features in your web interface:")
    print("   1. Go to your export form")
    print("   2. Fill in all the university branding fields")
    print("   3. Check the student information options you want")
    print("   4. Select your preferred export format")
    print("   5. Enable 'Create A/B/C versions' if desired")

if __name__ == '__main__':
    create_enhanced_demo_export()
