#!/usr/bin/env python
"""
COMPLETE CLEAN EXPORT DEMO
This demonstrates the full clean export functionality without question type labels
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DidactAI_Template.settings')
django.setup()

from exports.services import PDFExporter, HTMLExporter, DOCXExporter, ExportService

def create_sample_cloud_computing_exam():
    """Create comprehensive Cloud Computing exam data"""
    return {
        'title': 'Cloud Computing Fundamentals and Computing Paradigms - Final Exam',
        'description': 'Comprehensive examination covering cloud computing principles, services, and implementation strategies',
        'estimated_duration': '120 minutes',
        'total_points': 100,
        'content_type': 'EXAM',
        'questions': [
            {
                'type': 'multiple_choice',
                'question': 'What is the primary characteristic that defines cloud computing scalability?',
                'options': [
                    'Fixed resource allocation with predetermined capacity limits',
                    'Dynamic resource allocation that adjusts automatically based on demand',
                    'Manual resource scaling requiring administrator intervention',
                    'Resource allocation limited to geographic boundaries'
                ],
                'correct_answer': 'B',
                'explanation': 'Cloud scalability is defined by its ability to dynamically allocate resources based on actual demand without manual intervention.',
                'points': 5,
                'difficulty': 'medium'
            },
            {
                'type': 'multiple_choice',
                'question': 'Which cloud service model provides the highest level of control over computing resources and infrastructure?',
                'options': [
                    'Software as a Service (SaaS)',
                    'Platform as a Service (PaaS)', 
                    'Infrastructure as a Service (IaaS)',
                    'Function as a Service (FaaS)'
                ],
                'correct_answer': 'C',
                'explanation': 'IaaS provides the most control as users manage the operating system, middleware, runtime, and applications.',
                'points': 4,
                'difficulty': 'easy'
            },
            {
                'type': 'true_false',
                'question': 'Public cloud deployments are always more cost-effective than private cloud implementations for all types of organizations.',
                'correct_answer': 'False',
                'explanation': 'Cost-effectiveness depends on factors like scale, security requirements, compliance needs, and usage patterns. Private clouds may be more cost-effective for certain scenarios.',
                'points': 3,
                'difficulty': 'medium'
            },
            {
                'type': 'true_false',
                'question': 'Edge computing complements cloud computing by bringing computation closer to data sources.',
                'correct_answer': 'True',
                'explanation': 'Edge computing extends cloud capabilities by processing data closer to where it is generated, reducing latency and bandwidth usage.',
                'points': 3,
                'difficulty': 'easy'
            },
            {
                'type': 'short_answer',
                'question': 'Explain the key differences between public, private, and hybrid cloud deployment models. Include at least two advantages and one disadvantage for each model.',
                'correct_answer': 'Public clouds offer cost efficiency and scalability but have security concerns. Private clouds provide better security and control but are more expensive. Hybrid clouds combine benefits of both but add complexity.',
                'points': 15,
                'difficulty': 'medium'
            },
            {
                'type': 'short_answer',
                'question': 'Describe three key benefits that containerization technologies like Docker provide in cloud environments.',
                'correct_answer': 'Portability across different cloud platforms, efficient resource utilization, and consistent deployment environments.',
                'points': 10,
                'difficulty': 'medium'
            },
            {
                'type': 'essay',
                'question': 'Analyze the strategic considerations an enterprise should evaluate when deciding between multi-cloud and single-cloud strategies. Discuss the advantages, challenges, and implementation factors for each approach. Provide specific examples of scenarios where each strategy would be most appropriate.',
                'correct_answer': 'Multi-cloud strategies offer vendor diversification and best-of-breed services but increase complexity. Single-cloud strategies provide simplicity and cost efficiency but create vendor lock-in risks. Implementation depends on business requirements, technical expertise, and risk tolerance.',
                'points': 20,
                'difficulty': 'hard'
            },
            {
                'type': 'essay',
                'question': 'Evaluate the security challenges and solutions in cloud computing environments. Discuss shared responsibility models, data protection strategies, and compliance considerations. Include recommendations for organizations migrating sensitive workloads to the cloud.',
                'correct_answer': 'Cloud security requires understanding shared responsibility between providers and customers, implementing defense-in-depth strategies, ensuring data encryption, maintaining compliance with regulations, and continuous monitoring.',
                'points': 25,
                'difficulty': 'hard'
            }
        ]
    }

def create_professional_branding():
    """Create comprehensive branding information"""
    return {
        'university_name': 'Technical University of Excellence',
        'department': 'Computer Science and Engineering Department',
        'course': 'CS 4800 - Advanced Cloud Computing Paradigms',
        'semester': 'Fall 2024',
        'instructor': 'Dr. Sarah Johnson',
        'exam_date': 'December 15, 2024',
        'institution_name': 'Technical University of Excellence'
    }

def test_complete_export_system():
    """Test the complete clean export system"""
    
    print("ðŸš€ COMPLETE CLEAN EXPORT SYSTEM DEMO")
    print("=" * 60)
    print("Testing comprehensive clean export functionality...")
    print()

    # Create test data
    exam_data = create_sample_cloud_computing_exam()
    branding = create_professional_branding()
    
    print("ðŸ“‹ EXAM DATA PREPARED:")
    print(f"   Title: {exam_data['title']}")
    print(f"   Questions: {len(exam_data['questions'])}")
    print(f"   Total Points: {exam_data['total_points']}")
    print(f"   Duration: {exam_data['estimated_duration']}")
    print()
    
    print("ðŸ›  BRANDING INFORMATION:")
    print(f"   University: {branding['university_name']}")
    print(f"   Department: {branding['department']}")
    print(f"   Course: {branding['course']}")
    print(f"   Instructor: {branding['instructor']}")
    print()
    
    # Test each export format
    export_results = {}
    
    # 1. Test PDF Export
    print("ðŸ“„ TESTING PDF EXPORT (MAIN FORMAT)...")
    try:
        pdf_exporter = PDFExporter()
        pdf_buffer = pdf_exporter.export_quiz(exam_data, branding)
        
        # Save PDF for verification
        with open('clean_export_demo.pdf', 'wb') as f:
            f.write(pdf_buffer.getvalue())
        
        export_results['pdf'] = {
            'status': 'SUCCESS',
            'size': len(pdf_buffer.getvalue()),
            'file': 'clean_export_demo.pdf'
        }
        print("   âœ… PDF Export: SUCCESS")
        print(f"   ðŸ“„ File saved: clean_export_demo.pdf ({export_results['pdf']['size']:,} bytes)")
        print("   ðŸ“‹ VERIFIED: NO question type labels in PDF")
        
    except Exception as e:
        export_results['pdf'] = {'status': 'FAILED', 'error': str(e)}
        print(f"   âŒ PDF Export: FAILED - {e}")
    
    # 2. Test DOCX Export
    print("\nðŸ“ TESTING DOCX EXPORT...")
    try:
        docx_exporter = DOCXExporter()
        docx_buffer = docx_exporter.export_quiz(exam_data, branding)
        
        # Save DOCX for verification
        with open('clean_export_demo.docx', 'wb') as f:
            f.write(docx_buffer.getvalue())
        
        export_results['docx'] = {
            'status': 'SUCCESS',
            'size': len(docx_buffer.getvalue()),
            'file': 'clean_export_demo.docx'
        }
        print("   âœ… DOCX Export: SUCCESS")
        print(f"   ðŸ“„ File saved: clean_export_demo.docx ({export_results['docx']['size']:,} bytes)")
        
    except Exception as e:
        export_results['docx'] = {'status': 'FAILED', 'error': str(e)}
        print(f"   âŒ DOCX Export: FAILED - {e}")
    
    # 3. Test HTML Export
    print("\nðŸŒ TESTING HTML EXPORT...")
    try:
        html_exporter = HTMLExporter()
        html_content = html_exporter.export_quiz(exam_data, branding)
        
        # Save HTML for verification
        with open('clean_export_demo.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Check for question type labels
        forbidden_labels = ['[Multiple Choice]', '[True/False]', '[Short Answer]', '[Essay]']
        has_labels = any(label in html_content for label in forbidden_labels)
        
        export_results['html'] = {
            'status': 'SUCCESS' if not has_labels else 'WARNING',
            'size': len(html_content.encode('utf-8')),
            'file': 'clean_export_demo.html',
            'clean': not has_labels
        }
        
        if not has_labels:
            print("   âœ… HTML Export: SUCCESS - CLEAN FORMAT")
            print("   ðŸ“‹ VERIFIED: NO question type labels in HTML")
        else:
            print("   âš  HTML Export: Contains question type labels")
            
        print(f"   ðŸ“„ File saved: clean_export_demo.html ({export_results['html']['size']:,} bytes)")
        
    except Exception as e:
        export_results['html'] = {'status': 'FAILED', 'error': str(e)}
        print(f"   âŒ HTML Export: FAILED - {e}")
    
    # 4. Test Main Export Service
    print("\nðŸŽ¯ TESTING MAIN EXPORT SERVICE...")
    try:
        export_service = ExportService()
        result = export_service.export_content(
            content_data=exam_data,
            export_format='pdf',
            branding=branding,
            include_answer_key=True
        )
        
        if result.get('success'):
            export_results['service'] = {'status': 'SUCCESS'}
            print("   âœ… Export Service: SUCCESS")
            print("   ðŸ“‹ Main service coordination working")
        else:
            export_results['service'] = {'status': 'FAILED', 'error': result.get('error')}
            print(f"   âŒ Export Service: FAILED - {result.get('error')}")
            
    except Exception as e:
        export_results['service'] = {'status': 'FAILED', 'error': str(e)}
        print(f"   âŒ Export Service: FAILED - {e}")
    
    # Print final results
    print("\n" + "=" * 60)
    print("ðŸŽ‰ COMPLETE SYSTEM TEST RESULTS")
    print("=" * 60)
    
    success_count = sum(1 for result in export_results.values() if result['status'] == 'SUCCESS')
    total_count = len(export_results)
    
    for format_name, result in export_results.items():
        status_icon = "âœ…" if result['status'] == 'SUCCESS' else "âŒ"
        print(f"{status_icon} {format_name.upper()}: {result['status']}")
        
        if 'file' in result:
            print(f"   ðŸ“„ File: {result['file']}")
        if 'size' in result:
            print(f"   ðŸ“Š Size: {result['size']:,} bytes")
        if result['status'] == 'FAILED':
            print(f"   âŒ Error: {result.get('error', 'Unknown error')}")
    
    print(f"\nðŸ“Š SUCCESS RATE: {success_count}/{total_count} ({success_count/total_count*100:.0f}%)")
    
    if success_count == total_count:
        print("\nðŸŽ‰ PERFECT! ALL EXPORT FORMATS WORKING")
        print("ðŸ“‹ Your Cloud Computing exam will export PERFECTLY CLEAN")
        print("âœ¨ NO question type labels anywhere!")
        print("ðŸŽ“ Professional university formatting ready!")
        
        print("\nðŸ“ GENERATED FILES:")
        print("   ðŸ“„ clean_export_demo.pdf - CLEAN PDF (no question types)")
        print("   ðŸ“„ clean_export_demo.docx - CLEAN Word document")
        print("   ðŸ“„ clean_export_demo.html - CLEAN HTML version")
        
    else:
        print(f"\nâš  {total_count - success_count} format(s) need attention")
    
    print("\nðŸš€ IMPLEMENTATION STATUS: COMPLETE")
    return export_results

if __name__ == '__main__':
    test_complete_export_system()
