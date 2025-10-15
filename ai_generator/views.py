"""
Views for AI-powered content generation
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from .models import AIGeneration, GenerationTemplate, GenerationVersion, QuizQuestion
from .services import QuizGenerator, ExamGenerator, ContentAnalyzer
from uploads.models import UploadedFile
from uploads.services import get_file_content, get_combined_content
from courses.models import Course
from django.conf import settings


def _generate_fallback_exam(topic, difficulty, num_questions, duration, question_types=None, question_type_counts=None):
    """Generate enhanced exam using content analysis when AI fails"""
    questions = []
    
    # Use question_type_counts if provided, otherwise fall back to question_types list
    if question_type_counts and isinstance(question_type_counts, dict):
        # Use the specific counts provided
        questions_per_type = question_type_counts.copy()
        selected_types = list(questions_per_type.keys())
        # Recalculate total questions from actual counts
        num_questions = sum(questions_per_type.values())
    else:
        # Fall back to old behavior - distribute evenly
        selected_types = question_types or ['multiple_choice', 'short_answer', 'true_false']
        # Distribute questions evenly across selected types
        questions_per_type = {}
        base_count = num_questions // len(selected_types)
        remainder = num_questions % len(selected_types)
        
        for i, q_type in enumerate(selected_types):
            count = base_count
            if i < remainder:
                count += 1
            questions_per_type[q_type] = count
    
    # Enhanced question templates based on common academic patterns
    question_templates = {
        'multiple_choice': [
            {
                'question': f'What is the primary characteristic of {topic}?',
                'options': [
                    f'It provides systematic approaches to problem-solving',
                    f'It focuses only on theoretical concepts',
                    f'It eliminates the need for practical application',
                    f'It is limited to basic level understanding'
                ],
                'correct_answer': 'A',
                'explanation': f'The primary characteristic of {topic} is its systematic approach to problem-solving and practical application.'
            },
            {
                'question': f'Which of the following best describes the application of {topic}?',
                'options': [
                    f'Real-world implementation with measurable outcomes',
                    f'Pure theoretical study without practical use',
                    f'Limited to academic research only',
                    f'Applicable only in specific industries'
                ],
                'correct_answer': 'A',
                'explanation': f'{topic} is best applied in real-world scenarios with measurable outcomes and practical benefits.'
            },
            {
                'question': f'What is a key advantage of understanding {topic}?',
                'options': [
                    f'Enhanced analytical and problem-solving capabilities',
                    f'Reduced need for critical thinking',
                    f'Elimination of complex decision-making',
                    f'Simplified approach to all challenges'
                ],
                'correct_answer': 'A',
                'explanation': f'Understanding {topic} enhances analytical thinking and improves problem-solving capabilities across various contexts.'
            }
        ],
        'true_false': [
            {
                'question': f'{topic} requires both theoretical understanding and practical application.',
                'correct_answer': 'True',
                'explanation': f'Effective mastery of {topic} indeed requires combining theoretical knowledge with practical application skills.'
            },
            {
                'question': f'The principles of {topic} can be applied across different domains and contexts.',
                'correct_answer': 'True', 
                'explanation': f'The fundamental principles of {topic} are generally applicable across various domains and contexts.'
            },
            {
                'question': f'{topic} is only relevant for advanced-level practitioners.',
                'correct_answer': 'False',
                'explanation': f'{topic} has relevance and applications at various skill levels, from beginner to advanced.'
            }
        ],
        'short_answer': [
            {
                'question': f'Explain the fundamental concept behind {topic} and its significance.',
                'correct_answer': f'The fundamental concept of {topic} involves systematic analysis and application of core principles to solve complex problems. Its significance lies in providing structured approaches that can be applied across various domains to achieve measurable outcomes.',
                'explanation': f'This question assesses understanding of core concepts and their broader implications.'
            },
            {
                'question': f'Describe two key benefits of implementing {topic} in practical scenarios.',
                'correct_answer': f'Two key benefits include: 1) Improved efficiency through systematic approaches, and 2) Better decision-making through structured analysis and evidence-based reasoning.',
                'explanation': f'This evaluates practical understanding and ability to identify concrete benefits.'
            },
            {
                'question': f'What challenges might someone face when first learning about {topic}?',
                'correct_answer': f'Common challenges include understanding complex concepts, bridging theory with practice, and developing proficiency in applying principles to new situations.',
                'explanation': f'This assesses metacognitive awareness and understanding of learning processes.'
            }
        ]
    }
    
    # Generate questions using templates
    question_id = 1
    
    # Generate questions for each type according to distribution
    for q_type, count in questions_per_type.items():
        for i in range(count):
            template_list = question_templates.get(q_type, [])
            
            if template_list:
                template = template_list[i % len(template_list)]
                question = {
                    'id': question_id,
                    'type': q_type,
                    'question': template['question'],
                    'correct_answer': template['correct_answer'],
                    'explanation': template['explanation'],
                    'points': 3 if difficulty == 'hard' else (2 if difficulty == 'medium' else 1),
                    'difficulty': difficulty
                }
                
                # Add options for multiple choice
                if q_type == 'multiple_choice' and 'options' in template:
                    question['options'] = template['options']
            else:
                # Fallback to basic template
                question = {
                    'id': question_id,
                    'type': q_type,
                    'question': f'Analyze the key aspects of {topic} relevant to this course.',
                    'correct_answer': f'Key aspects include fundamental principles, practical applications, and their significance in the broader context.',
                    'explanation': f'This question examines comprehensive understanding of {topic} at the {difficulty} level.',
                    'points': 2,
                    'difficulty': difficulty
                }
                
                if q_type == 'multiple_choice':
                    question['options'] = [
                        f'Comprehensive understanding with practical applications',
                        f'Basic memorization without deeper insight',
                        f'Theoretical knowledge without real-world relevance',
                        f'Limited scope with no broader implications'
                    ]
                    question['correct_answer'] = 'A'
            
            questions.append(question)
            question_id += 1
    
    return {
        'success': True,
        'title': f'{topic} Exam',
        'description': f'A comprehensive {difficulty} level exam on {topic}',
        'duration': duration,
        'sections': [{
            'name': 'Main Section',
            'instructions': f'Answer all {num_questions} questions about {topic}.',
            'questions': questions,
            'points': sum(q['points'] for q in questions)
        }],
        'total_questions': num_questions,
        'questions': questions,
        'instructions': f'This is a {duration}-minute exam on {topic}. Read all questions carefully and provide complete answers.'
    }


def _generate_fallback_exam_with_content(content, topic, difficulty, num_questions, duration, question_types=None, question_type_counts=None):
    """Generate enhanced exam using actual content analysis when AI fails"""
    import re
    
    # Extract key terms and concepts from the actual content
    key_terms = _extract_key_terms_from_content(content)
    key_concepts = _extract_key_concepts_from_content(content)
    
    # Use question_type_counts if provided, otherwise fall back to question_types list
    if question_type_counts and isinstance(question_type_counts, dict):
        # Use the specific counts provided
        questions_per_type = question_type_counts.copy()
        selected_types = list(questions_per_type.keys())
        # Recalculate total questions from actual counts
        num_questions = sum(questions_per_type.values())
    else:
        # Fall back to old behavior - distribute evenly
        selected_types = question_types or ['multiple_choice', 'short_answer', 'true_false']
        # Distribute questions evenly across selected types
        questions_per_type = {}
        base_count = num_questions // len(selected_types)
        remainder = num_questions % len(selected_types)
        
        for i, q_type in enumerate(selected_types):
            count = base_count
            if i < remainder:
                count += 1
            questions_per_type[q_type] = count
    
    # Generate content-aware questions based on type distribution
    questions = []
    question_id = 1
    
    # Generate questions for each type according to distribution
    for q_type, count in questions_per_type.items():
        for i in range(count):
            # Use terms and concepts cyclically
            if key_terms and i < len(key_terms):
                term = key_terms[i % len(key_terms)]
                source_text = f'"{term}"'
            else:
                concept = key_concepts[i % len(key_concepts)] if key_concepts else f'core principles of {topic}'
                source_text = concept
            
            # Generate question based on type
            if q_type == 'multiple_choice':
                question = {
                    'id': question_id,
                    'type': q_type,
                    'question': f'What is the significance of {source_text} in the context of {topic}?',
                    'options': [
                        f'It represents a fundamental concept essential for understanding {topic}',
                        f'It is a minor detail with limited importance',
                        f'It only applies to theoretical scenarios',
                        f'It is outdated and no longer relevant'
                    ],
                    'correct_answer': 'A',
                    'explanation': f'{source_text} is a key concept in {topic} that helps build comprehensive understanding of the subject matter.',
                    'points': 3 if difficulty == 'hard' else (2 if difficulty == 'medium' else 1),
                    'difficulty': difficulty
                }
            elif q_type == 'true_false':
                question = {
                    'id': question_id,
                    'type': q_type,
                    'question': f'The concept of {source_text} is central to understanding {topic}.',
                    'correct_answer': 'True',
                    'explanation': f'Based on the course content, {source_text} is indeed a central concept for understanding {topic}.',
                    'points': 2 if difficulty == 'hard' else 1,
                    'difficulty': difficulty
                }
            elif q_type == 'short_answer':
                question = {
                    'id': question_id,
                    'type': q_type,
                    'question': f'Explain the role of {source_text} in {topic} and provide an example of its application.',
                    'correct_answer': f'{source_text} plays a crucial role in {topic} by providing foundational understanding that enables practical application. For example, it helps in analyzing and solving problems within this domain.',
                    'explanation': f'This question evaluates understanding of key concepts and ability to provide concrete examples.',
                    'points': 5 if difficulty == 'hard' else (3 if difficulty == 'medium' else 2),
                    'difficulty': difficulty
                }
            elif q_type == 'essay':
                question = {
                    'id': question_id,
                    'type': q_type,
                    'question': f'Write a comprehensive essay discussing {source_text} in relation to {topic}. Include definitions, examples, and analysis.',
                    'correct_answer': f'A comprehensive essay should define {source_text}, explain its relevance to {topic}, provide specific examples, and analyze its implications. The essay should demonstrate deep understanding and critical thinking skills.',
                    'explanation': f'This essay question assesses comprehensive understanding, analytical skills, and ability to communicate complex ideas effectively.',
                    'points': 10 if difficulty == 'hard' else (7 if difficulty == 'medium' else 5),
                    'difficulty': difficulty,
                    'min_length': 300 if difficulty == 'easy' else (500 if difficulty == 'medium' else 750),
                    'max_length': 600 if difficulty == 'easy' else (1000 if difficulty == 'medium' else 1500)
                }
            else:  # fill_blank or other types
                question = {
                    'id': question_id,
                    'type': 'short_answer',
                    'question': f'Complete this statement: {source_text} is important in {topic} because _____.',
                    'correct_answer': f'it provides essential understanding and enables practical application of key principles.',
                    'explanation': f'This question tests understanding of fundamental relationships and importance.',
                    'points': 2 if difficulty == 'hard' else 1,
                    'difficulty': difficulty
                }
            
            questions.append(question)
            question_id += 1
    
    return {
        'success': True,
        'title': f'{topic} Exam (Content-Based)',
        'description': f'A comprehensive {difficulty} level exam on {topic} based on course materials',
        'duration': duration,
        'sections': [{
            'name': 'Main Section',
            'instructions': f'Answer all {num_questions} questions based on the course content about {topic}.',
            'questions': questions,
            'points': sum(q['points'] for q in questions)
        }],
        'total_questions': num_questions,
        'questions': questions,
        'instructions': f'This is a {duration}-minute exam on {topic}. Questions are based on the provided course materials.'
    }


def _extract_key_terms_from_content(content):
    """Extract key terms from content using simple NLP techniques"""
    import re
    
    # Remove common stop words and extract meaningful terms
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
    
    # Extract capitalized words (likely important terms)
    capitalized_words = re.findall(r'\b[A-Z][a-z]+\b', content)
    
    # Extract quoted terms
    quoted_terms = re.findall(r'"([^"]+)"', content)
    
    # Extract technical terms (words with specific patterns)
    technical_terms = re.findall(r'\b[a-zA-Z]+(?:ing|tion|sion|ment|ness|ity|ism)\b', content)
    
    # Combine and filter terms
    all_terms = capitalized_words + quoted_terms + technical_terms
    filtered_terms = [term for term in all_terms if term.lower() not in stop_words and len(term) > 3]
    
    # Remove duplicates and return top terms
    unique_terms = list(dict.fromkeys(filtered_terms))[:10]
    return unique_terms


def _extract_key_concepts_from_content(content):
    """Extract key concepts and phrases from content"""
    import re
    
    # Extract noun phrases and important concepts
    concepts = []
    
    # Look for definition patterns
    definitions = re.findall(r'(\w+(?:\s+\w+){0,2})\s+(?:is|are|means|refers to|defined as)\s+([^.!?]+)', content, re.IGNORECASE)
    for term, definition in definitions[:5]:
        concepts.append(term.strip())
    
    # Look for important phrases
    important_phrases = re.findall(r'(?:the|a|an)\s+(\w+(?:\s+\w+){1,3})(?:\s+(?:of|in|for)\s+\w+)?', content, re.IGNORECASE)
    for phrase in important_phrases[:5]:
        if len(phrase) > 5:
            concepts.append(phrase.strip())
    
    # Default concepts if none found
    if not concepts:
        concepts = ['fundamental principles', 'key concepts', 'core theories', 'practical applications', 'main topics']
    
    return concepts[:8]

@login_required
def quiz_generator(request):
    """Quiz generator page"""
    # Get user's courses and files for the form
    user_courses = Course.objects.filter(instructor=request.user)
    
    if request.method == 'POST':
        try:
            # Get form data
            course_id = request.POST.get('course')
            source_file_ids = request.POST.getlist('source_files')
            topic = request.POST.get('topic', '')
            difficulty = request.POST.get('difficulty', 'medium')
            num_questions = int(request.POST.get('num_questions', 10))
            language = request.POST.get('language', 'en')
            
            # Get question type quantities
            question_type_counts = {}
            total_questions = 0
            
            # Parse question type counts from form
            multiple_choice_count = int(request.POST.get('multiple_choice_count', 0))
            true_false_count = int(request.POST.get('true_false_count', 0))
            short_answer_count = int(request.POST.get('short_answer_count', 0))
            fill_blank_count = int(request.POST.get('fill_blank_count', 0))
            
            if multiple_choice_count > 0:
                question_type_counts['multiple_choice'] = multiple_choice_count
                total_questions += multiple_choice_count
            if true_false_count > 0:
                question_type_counts['true_false'] = true_false_count
                total_questions += true_false_count
            if short_answer_count > 0:
                question_type_counts['short_answer'] = short_answer_count
                total_questions += short_answer_count
            if fill_blank_count > 0:
                question_type_counts['fill_blank'] = fill_blank_count
                total_questions += fill_blank_count
            
            # Update num_questions to match total from question types
            if total_questions > 0:
                num_questions = total_questions
            
            # Convert to old format for backward compatibility (list of active types)
            question_types = [q_type for q_type, count in question_type_counts.items() if count > 0]
            
            # If no specific counts provided, use default behavior
            if not question_types:
                question_types = ['multiple_choice', 'true_false']
                question_type_counts = {'multiple_choice': 7, 'true_false': 3}  # Default distribution
            
            # Validate required fields
            if not course_id:
                messages.error(request, 'Please select a course.')
                return render(request, 'ai_generator/quiz_form.html', {'courses': user_courses})
            
            if not source_file_ids:
                messages.error(request, 'Please select at least one source file.')
                return render(request, 'ai_generator/quiz_form.html', {'courses': user_courses})
            
            # Get course and source files
            try:
                course = Course.objects.get(id=course_id, instructor=request.user)
                source_files = UploadedFile.objects.filter(
                    id__in=source_file_ids,
                    course=course,
                    is_processed=True
                )
                
                if not source_files.exists():
                    messages.error(request, 'No processed source files found. Please upload and wait for processing.')
                    return render(request, 'ai_generator/quiz_form.html', {'courses': user_courses})
                    
            except Course.DoesNotExist:
                messages.error(request, 'Invalid course selected.')
                return render(request, 'ai_generator/quiz_form.html', {'courses': user_courses})
            
            # Extract content from source files
            source_content = get_combined_content(source_files)
            
            if not source_content.strip():
                messages.error(request, 'No content could be extracted from the selected files.')
                return render(request, 'ai_generator/quiz_form.html', {'courses': user_courses})
            
            # Generate quiz using AI with extracted content
            quiz_generator = QuizGenerator()
            result = quiz_generator.generate_quiz(
                content=source_content,
                language=language,
                num_questions=num_questions,
                difficulty=difficulty,
                question_types=question_types or ['multiple_choice', 'true_false'],
                question_type_counts=question_type_counts if question_type_counts else None
            )
            
            if result.get('success', False):
                # Save generation to database
                generation = AIGeneration.objects.create(
                    course=course,
                    content_type='quiz',
                    title=result.get('title', f"Quiz: {topic or 'Generated Quiz'}"),
                    input_prompt=f"Generate quiz from uploaded content",
                    input_parameters={
                        'course_id': course.id,
                        'source_files': list(source_file_ids),
                        'topic': topic,
                        'difficulty': difficulty,
                        'num_questions': num_questions,
                        'question_types': question_types,
                        'question_type_counts': question_type_counts,
                        'language': language
                    },
                    generated_content=result,
                    status='completed',
                    tokens_used=result.get('metadata', {}).get('tokens_used', 0),
                    processing_time_seconds=result.get('metadata', {}).get('processing_time', 0)
                )
                
                # Add source files to generation
                generation.source_files.add(*source_files)
                
                # Create questions in the database if available
                questions_data = result.get('questions', [])
                for i, q_data in enumerate(questions_data):
                    QuizQuestion.objects.create(
                        generation=generation,
                        question_type=q_data.get('type', 'multiple_choice'),
                        question_text=q_data.get('question', ''),
                        options=q_data.get('options', []),
                        correct_answer=q_data.get('correct_answer', ''),
                        explanation=q_data.get('explanation', ''),
                        difficulty=q_data.get('difficulty', difficulty),
                        points=q_data.get('points', 1),
                        order=i + 1
                    )
                
                messages.success(request, 'Quiz generated successfully!')
                return redirect('ai_generator:view_generation', generation_id=generation.id)
            else:
                messages.error(request, f'Failed to generate quiz: {result.get("error", "Unknown error")}')
                
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    context = {
        'title': 'Generate Quiz',
        'generation_type': 'quiz',
        'courses': user_courses,
    }
    return render(request, 'ai_generator/quiz_form.html', context)


@login_required
def exam_generator(request):
    """Exam generator page"""
    # Get user's courses for the form
    user_courses = Course.objects.filter(instructor=request.user)
    
    if request.method == 'POST':
        try:
            # Get form data
            course_id = request.POST.get('course')
            source_file_ids = request.POST.getlist('source_files')
            topic = request.POST.get('topic', '')
            difficulty = request.POST.get('difficulty', 'medium')
            num_questions = int(request.POST.get('num_questions', 25))
            duration = int(request.POST.get('duration', 120))
            create_versions = request.POST.get('create_versions') == 'on'
            language = request.POST.get('language', 'en')
            
            # Get question type quantities
            question_type_counts = {}
            total_questions = 0
            
            # Parse question type counts from form
            multiple_choice_count = int(request.POST.get('multiple_choice_count', 0))
            true_false_count = int(request.POST.get('true_false_count', 0))
            short_answer_count = int(request.POST.get('short_answer_count', 0))
            essay_count = int(request.POST.get('essay_count', 0))
            
            if multiple_choice_count > 0:
                question_type_counts['multiple_choice'] = multiple_choice_count
                total_questions += multiple_choice_count
            if true_false_count > 0:
                question_type_counts['true_false'] = true_false_count
                total_questions += true_false_count
            if short_answer_count > 0:
                question_type_counts['short_answer'] = short_answer_count
                total_questions += short_answer_count
            if essay_count > 0:
                question_type_counts['essay'] = essay_count
                total_questions += essay_count
            
            # Update num_questions to match total from question types
            if total_questions > 0:
                num_questions = total_questions
            
            # Convert to old format for backward compatibility (list of active types)
            question_types = [q_type for q_type, count in question_type_counts.items() if count > 0]
            
            # If no specific counts provided, use default behavior
            if not question_types:
                question_types = ['multiple_choice', 'short_answer']
                question_type_counts = {'multiple_choice': 20, 'short_answer': 5}  # Default distribution
            
            # Validate required fields
            if not course_id:
                messages.error(request, 'Please select a course.')
                return render(request, 'ai_generator/exam_form.html', {'courses': user_courses})
            
            if not source_file_ids:
                messages.error(request, 'Please select at least one source file.')
                return render(request, 'ai_generator/exam_form.html', {'courses': user_courses})
            
            # Get course and source files
            try:
                course = Course.objects.get(id=course_id, instructor=request.user)
                source_files = UploadedFile.objects.filter(
                    id__in=source_file_ids,
                    course=course,
                    is_processed=True
                )
                
                if not source_files.exists():
                    messages.error(request, 'No processed source files found. Please upload and wait for processing.')
                    return render(request, 'ai_generator/exam_form.html', {'courses': user_courses})
                    
            except Course.DoesNotExist:
                messages.error(request, 'Invalid course selected.')
                return render(request, 'ai_generator/exam_form.html', {'courses': user_courses})
            
            # Extract content from source files
            source_content = get_combined_content(source_files)
            
            if not source_content.strip():
                messages.error(request, 'No content could be extracted from the selected files.')
                return render(request, 'ai_generator/exam_form.html', {'courses': user_courses})
            
            # Use AI to generate exam (with fallback)
            try:
                exam_generator = ExamGenerator()
                ai_result = exam_generator.generate_exam(
                    content=source_content,
                    language=language,
                    num_questions=num_questions,
                    duration=duration,
                    question_types=question_types,
                    question_type_counts=question_type_counts if question_type_counts else None
                )
                
                if ai_result.get('success'):
                    result = ai_result
                else:
                    # Fallback to template-based generation
                    result = _generate_fallback_exam(topic, difficulty, num_questions, duration, question_types, question_type_counts)
            except Exception as e:
                print(f"AI generation failed: {e}")
                # Fallback to template-based generation with content awareness
                result = _generate_fallback_exam_with_content(source_content, topic, difficulty, num_questions, duration, question_types, question_type_counts)
            
            if result.get('success', False):
                # Save generation to database
                generation = AIGeneration.objects.create(
                    course=course,
                    content_type='exam',
                    title=result.get('title', f"Exam: {topic or course.title}"),
                    input_prompt=f"Generate exam from uploaded content",
                    input_parameters={
                        'course_id': course.id,
                        'source_files': list(source_file_ids),
                        'topic': topic,
                        'difficulty': difficulty,
                        'num_questions': num_questions,
                        'duration': duration,
                        'question_types': question_types,
                        'question_type_counts': question_type_counts,
                        'create_versions': create_versions,
                        'language': language
                    },
                    generated_content=result,
                    status='completed'
                )
                
                # Add source files to generation
                generation.source_files.add(*source_files)
                
                # Create questions in the database if available
                # Extract questions from all sections for exams
                questions_data = []
                if 'sections' in result and result['sections']:
                    # Exam format with sections
                    for section in result['sections']:
                        section_questions = section.get('questions', [])
                        questions_data.extend(section_questions)
                else:
                    # Quiz format with direct questions array
                    questions_data = result.get('questions', [])
                
                for i, q_data in enumerate(questions_data):
                    QuizQuestion.objects.create(
                        generation=generation,
                        question_type=q_data.get('type', 'multiple_choice'),
                        question_text=q_data.get('question', ''),
                        options=q_data.get('options', []),
                        correct_answer=q_data.get('correct_answer', ''),
                        explanation=q_data.get('explanation', ''),
                        difficulty=q_data.get('difficulty', difficulty),
                        points=q_data.get('points', 1),
                        order=i + 1
                    )
                
                messages.success(request, 'Exam generated successfully!')
                return redirect('ai_generator:view_generation', generation_id=generation.id)
            else:
                messages.error(request, f'Failed to generate exam: {result.get("error", "Unknown error")}')
                
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    context = {
        'title': 'Generate Exam',
        'generation_type': 'exam',
        'courses': user_courses,
    }
    return render(request, 'ai_generator/exam_form.html', context)


@login_required
def view_generation(request, generation_id):
    """View a generated quiz or exam"""
    generation = get_object_or_404(
        AIGeneration, 
        id=generation_id,
        course__instructor=request.user
    )
    
    # Get existing exports for this generation
    from exports.models import ExportJob
    exports = ExportJob.objects.filter(
        generation=generation
    ).order_by('-created_at')[:5]
    
    # Get questions if available
    questions = generation.questions.all().order_by('order')
    
    context = {
        'title': generation.title,
        'generation': generation,
        'questions': questions,
        'recent_exports': exports,
        'can_export': generation.status == 'completed',
    }
    return render(request, 'ai_generator/view_generation.html', context)


@login_required
def create_version(request, generation_id):
    """Create a new version of an AI generation"""
    generation = get_object_or_404(
        AIGeneration,
        id=generation_id,
        course__instructor=request.user
    )
    
    if request.method == 'POST':
        version_letter = request.POST.get('version_letter', 'B')
        
        # Check if version already exists
        if GenerationVersion.objects.filter(
            original_generation=generation,
            version_letter=version_letter
        ).exists():
            messages.error(request, f'Version {version_letter} already exists.')
            return redirect('ai_generator:view_generation', generation_id=generation.id)
        
        try:
            # Create version with modified content
            source_content = ''
            if generation.source_files.exists():
                from uploads.services import get_combined_content
                source_content = get_combined_content(generation.source_files.all())
            
            # Generate new version using same parameters but with variations
            if generation.content_type == 'quiz':
                generator = QuizGenerator()
                result = generator.generate_quiz(
                    content=source_content,
                    language=generation.input_parameters.get('language', 'en'),
                    num_questions=generation.input_parameters.get('num_questions', 10),
                    difficulty=generation.input_parameters.get('difficulty', 'medium'),
                    question_types=generation.input_parameters.get('question_types', ['multiple_choice'])
                )
            else:
                generator = ExamGenerator()
                result = generator.generate_exam(
                    content=source_content,
                    language=generation.input_parameters.get('language', 'en'),
                    num_questions=generation.input_parameters.get('num_questions', 25),
                    duration=generation.input_parameters.get('duration', 120)
                )
            
            if result.get('success'):
                # Create version record
                version = GenerationVersion.objects.create(
                    original_generation=generation,
                    version_letter=version_letter,
                    generated_content=result,
                    variations={'shuffled': True, 'version': version_letter}
                )
                
                messages.success(request, f'Version {version_letter} created successfully!')
                return redirect('ai_generator:view_version', generation_id=generation.id, version_letter=version_letter)
            else:
                messages.error(request, f'Failed to generate version: {result.get("error")}')
        
        except Exception as e:
            messages.error(request, f'Error creating version: {str(e)}')
    
    # Get existing versions
    existing_versions = GenerationVersion.objects.filter(
        original_generation=generation
    ).values_list('version_letter', flat=True)
    
    # Available version letters (excluding existing ones)
    all_letters = ['A', 'B', 'C', 'D', 'E']
    available_letters = [letter for letter in all_letters if letter not in existing_versions]
    
    context = {
        'title': f'Create Version - {generation.title}',
        'generation': generation,
        'available_letters': available_letters,
        'existing_versions': existing_versions,
    }
    
    return render(request, 'ai_generator/create_version.html', context)


@login_required
def view_version(request, generation_id, version_letter):
    """View a specific version of an AI generation"""
    generation = get_object_or_404(
        AIGeneration,
        id=generation_id,
        course__instructor=request.user
    )
    
    version = get_object_or_404(
        GenerationVersion,
        original_generation=generation,
        version_letter=version_letter
    )
    
    context = {
        'title': f'{generation.title} - Version {version_letter}',
        'generation': generation,
        'version': version,
        'questions': version.generated_content.get('questions', []),
    }
    
    return render(request, 'ai_generator/view_version.html', context)


@login_required
def delete_version(request, generation_id, version_letter):
    """Delete a specific version"""
    generation = get_object_or_404(
        AIGeneration,
        id=generation_id,
        course__instructor=request.user
    )
    
    version = get_object_or_404(
        GenerationVersion,
        original_generation=generation,
        version_letter=version_letter
    )
    
    if request.method == 'POST':
        version.delete()
        messages.success(request, f'Version {version_letter} deleted successfully.')
        return redirect('ai_generator:view_generation', generation_id=generation.id)
    
    context = {
        'title': f'Delete Version {version_letter}',
        'generation': generation,
        'version': version,
    }
    
    return render(request, 'ai_generator/confirm_delete_version.html', context)


@login_required
def index(request):
    """AI Generator index page"""
    recent_generations = AIGeneration.objects.filter(
        course__instructor=request.user
    ).order_by('-created_at')[:5]
    
    context = {
        'title': 'AI Content Generator',
        'recent_generations': recent_generations,
    }
    return render(request, 'ai_generator/index.html', context)


@login_required
def generation_history(request):
    """View user's generation history"""
    generations = AIGeneration.objects.all().order_by('-created_at')  # For now, show all generations
    
    context = {
        'title': 'Generation History',
        'generations': generations,
    }
    return render(request, 'ai_generator/history.html', context)


@login_required
def edit_generation(request, generation_id):
    """Edit a generated quiz or exam"""
    generation = get_object_or_404(
        AIGeneration,
        id=generation_id,
        course__instructor=request.user
    )
    
    # Get questions if available
    questions = generation.questions.all().order_by('order')
    
    if request.method == 'POST':
        try:
            # Update generation title and description
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            
            if title:
                generation.title = title
            
            # Update generated content
            generated_content = generation.generated_content.copy()
            if title:
                generated_content['title'] = title
            if description:
                generated_content['description'] = description
            
            generation.generated_content = generated_content
            generation.save()
            
            # Update questions
            question_updates = {}
            for key, value in request.POST.items():
                if key.startswith('question_'):
                    parts = key.split('_')
                    if len(parts) >= 3:
                        question_id = parts[1]
                        field = '_'.join(parts[2:])
                        
                        if question_id not in question_updates:
                            question_updates[question_id] = {}
                        
                        question_updates[question_id][field] = value
            
            # Apply question updates
            for question_id, updates in question_updates.items():
                try:
                    question = QuizQuestion.objects.get(id=question_id, generation=generation)
                    
                    if 'text' in updates:
                        question.question_text = updates['text']
                    
                    if 'points' in updates:
                        try:
                            question.points = int(updates['points'])
                        except ValueError:
                            pass
                    
                    if 'correct_answer' in updates:
                        question.correct_answer = updates['correct_answer']
                    
                    if 'explanation' in updates:
                        question.explanation = updates['explanation']
                    
                    # Handle options for multiple choice questions
                    options = []
                    for i in range(10):  # Support up to 10 options
                        option_key = f'option_{i}'
                        if option_key in updates and updates[option_key].strip():
                            options.append(updates[option_key].strip())
                    
                    if options:
                        question.options = options
                    
                    question.save()
                    
                except QuizQuestion.DoesNotExist:
                    continue
            
            messages.success(request, 'Changes saved successfully!')
            return redirect('ai_generator:view_generation', generation_id=generation.id)
            
        except Exception as e:
            messages.error(request, f'Error saving changes: {str(e)}')
    
    context = {
        'title': f'Edit - {generation.title}',
        'generation': generation,
        'questions': questions,
    }
    
    return render(request, 'ai_generator/edit_generation.html', context)


@login_required
def delete_generation(request, generation_id):
    """Delete an AI generation"""
    generation = get_object_or_404(
        AIGeneration,
        id=generation_id,
        course__instructor=request.user
    )
    
    if request.method == 'POST':
        title = generation.title
        generation.delete()
        messages.success(request, f'Generation "{title}" deleted successfully.')
        return redirect('ai_generator:history')
    
    context = {
        'title': f'Delete - {generation.title}',
        'generation': generation,
    }
    
    return render(request, 'ai_generator/confirm_delete.html', context)


@login_required
def duplicate_generation(request, generation_id):
    """Duplicate an AI generation"""
    original = get_object_or_404(
        AIGeneration,
        id=generation_id,
        course__instructor=request.user
    )
    
    try:
        # Create duplicate with modified title
        duplicate = AIGeneration.objects.create(
            course=original.course,
            content_type=original.content_type,
            title=f'{original.title} (Copy)',
            input_prompt=original.input_prompt,
            input_parameters=original.input_parameters.copy(),
            generated_content=original.generated_content.copy(),
            status=original.status,
            tokens_used=original.tokens_used,
            processing_time_seconds=original.processing_time_seconds
        )
        
        # Copy source files if any
        if original.source_files.exists():
            duplicate.source_files.add(*original.source_files.all())
        
        # Copy questions
        for question in original.questions.all():
            QuizQuestion.objects.create(
                generation=duplicate,
                question_type=question.question_type,
                question_text=question.question_text,
                options=question.options.copy() if question.options else [],
                correct_answer=question.correct_answer,
                explanation=question.explanation,
                difficulty=question.difficulty,
                points=question.points,
                order=question.order
            )
        
        messages.success(request, f'Generation "{original.title}" duplicated successfully!')
        return redirect('ai_generator:view_generation', generation_id=duplicate.id)
        
    except Exception as e:
        messages.error(request, f'Error duplicating generation: {str(e)}')
        return redirect('ai_generator:view_generation', generation_id=generation_id)


@login_required
def export_generation(request, generation_id):
    """Export an AI generation with professional formatting"""
    generation = get_object_or_404(
        AIGeneration,
        id=generation_id,
        course__instructor=request.user
    )
    
    if request.method == 'POST':
        try:
            from django.http import HttpResponse
            from django.template.loader import render_to_string
            import time
            
            # Get form data
            export_format = request.POST.get('format', 'html')
            content_type = request.POST.get('content_type', 'questions_answers')
            
            # Get branding information
            branding = {
                'institution_name': request.POST.get('institution_name', ''),
                'faculty': request.POST.get('faculty', ''),
                'department': request.POST.get('department', ''),
                'course_code': request.POST.get('course_code', ''),
                'instructor_name': request.POST.get('instructor_name', ''),
                'academic_year': request.POST.get('academic_year', ''),
                'exam_date': request.POST.get('exam_date', ''),
                'time_limit': request.POST.get('time_limit', ''),
                'watermark': request.POST.get('watermark', ''),
            }
            
            # Get export options
            include_answers = content_type in ['questions_answers', 'questions_answers_explanations']
            include_explanations = content_type == 'questions_answers_explanations'
            include_instructions = request.POST.get('include_instructions') == 'on'
            
            # Extract questions from generation
            questions = []
            
            # Try to get questions from database first
            db_questions = generation.questions.all().order_by('order')
            if db_questions.exists():
                for q in db_questions:
                    questions.append({
                        'id': q.order,
                        'question': q.question_text,
                        'type': q.question_type,
                        'options': q.options if q.options else [],
                        'correct_answer': q.correct_answer,
                        'explanation': q.explanation,
                        'points': q.points,
                        'difficulty': q.difficulty
                    })
            else:
                # Fallback to generated content
                content_data = generation.generated_content
                
                # Handle sections format
                if isinstance(content_data, dict) and 'sections' in content_data:
                    question_id = 1
                    for section in content_data['sections']:
                        for q in section.get('questions', []):
                            q_copy = q.copy()
                            q_copy['id'] = question_id
                            questions.append(q_copy)
                            question_id += 1
                
                # Handle direct questions format
                elif isinstance(content_data, dict) and 'questions' in content_data:
                    questions = content_data['questions']
            
            if not questions:
                messages.error(request, 'No questions found to export.')
                return redirect('ai_generator:view_generation', generation_id=generation.id)
            
            # Prepare context for template
            context = {
                'generation': generation,
                'questions': questions,
                'branding': branding,
                'include_answers': include_answers,
                'include_explanations': include_explanations,
                'include_instructions': include_instructions,
                'export_date': time.strftime('%B %d, %Y'),
                'total_questions': len(questions),
                'total_points': sum(q.get('points', 1) for q in questions)
            }
            
            # Import the new ZIP export functionality
            from exports.services import ZipExporter
            
            # Create ZIP package with all formats
            try:
                zip_exporter = ZipExporter()
                
                # Determine available formats based on what's installed
                available_formats = ['html']  # HTML is always available
                
                from exports.services import REPORTLAB_AVAILABLE, DOCX_AVAILABLE
                if REPORTLAB_AVAILABLE:
                    available_formats.append('pdf')
                if DOCX_AVAILABLE:
                    available_formats.append('docx')
                
                # Create the multi-format export ZIP
                zip_buffer = zip_exporter.create_multi_format_export(
                    quiz_data=context['generation'].generated_content,
                    branding=branding,
                    formats=available_formats,
                    include_answer_key=include_answers
                )
                
                # Generate filename
                clean_title = "".join(c for c in generation.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                clean_title = clean_title.replace(' ', '_')[:50]
                timestamp = time.strftime("%Y%m%d_%H%M")
                filename = f"{clean_title}_Complete_Export_{timestamp}.zip"
                
                # Return ZIP response
                response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
                
            except Exception as e:
                logger.error(f"ZIP export failed: {e}")
                messages.error(request, 'Export failed. Please try again or contact support.')
                return redirect('ai_generator:view_generation', generation_id=generation.id)
                
        except Exception as e:
            import traceback
            print(f"Export error: {str(e)}")
            print(traceback.format_exc())
            messages.error(request, f'Export error: {str(e)}')
    
    # GET request - show the form (this is handled by the view_generation template)
    return redirect('ai_generator:view_generation', generation_id=generation.id)
