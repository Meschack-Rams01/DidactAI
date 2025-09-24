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
            question_types = request.POST.getlist('question_types')
            language = request.POST.get('language', 'en')
            
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
                question_types=question_types or ['multiple_choice', 'true_false']
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
            question_types = request.POST.getlist('question_types')
            create_versions = request.POST.get('create_versions') == 'on'
            language = request.POST.get('language', 'en')
            
            # Validate required fields
            if not course_id:
                messages.error(request, 'Please select a course.')
                return render(request, 'ai_generator/exam_form.html', {'courses': user_courses})
            
            if not source_file_ids:
                messages.error(request, 'Please select at least one source file.')
                return render(request, 'ai_generator/exam_form.html', {'courses': user_courses})
            
            # Generate exam using fallback data (replace with real AI later)
            questions = []
            selected_types = question_types or ['multiple_choice', 'short_answer']
            
            for i in range(num_questions):
                q_type = selected_types[i % len(selected_types)]
                question = {
                    'id': i+1,
                    'type': q_type,
                    'question': f'Question {i+1}: Analyze an important aspect of {topic}',
                    'points': 3 if difficulty == 'hard' else 2,
                    'explanation': f'This examines {topic} understanding at {difficulty} level.'
                }
                
                if q_type == 'multiple_choice':
                    question.update({
                        'options': [
                            f'Primary concept in {topic}',
                            f'Secondary aspect of {topic}',
                            f'Related theory in {topic}',
                            f'Alternative view of {topic}'
                        ],
                        'correct_answer': 'A'
                    })
                elif q_type == 'essay':
                    question.update({
                        'correct_answer': f'Comprehensive analysis of {topic} covering key concepts, applications, and implications.',
                        'min_length': 300,
                        'max_length': 1000
                    })
                else:  # short_answer, true_false, etc.
                    question.update({
                        'correct_answer': f'Key insight about {topic}'
                    })
                
                questions.append(question)
            
            result = {
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
                'instructions': f'This is a {duration}-minute exam on {topic}. Read all questions carefully and provide complete answers.'
            }
            
            if result.get('success', False):
                # Save generation to database
                generation = AIGeneration.objects.create(
                    course_id=1,  # Temporary - you'll need to handle course association properly
                    content_type='exam',
                    title=result.get('title', f"Exam: {topic}"),
                    input_prompt=f"Generate exam about {topic}",
                    input_parameters={
                        'topic': topic,
                        'difficulty': difficulty,
                        'num_questions': num_questions,
                        'duration': duration,
                        'question_types': question_types,
                        'create_versions': create_versions
                    },
                    generated_content=result,
                    status='completed'
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
    """Export an AI generation"""
    generation = get_object_or_404(
        AIGeneration,
        id=generation_id,
        course__instructor=request.user
    )
    
    if request.method == 'POST':
        try:
            from exports.models import ExportJob
            from exports.services import ExportService
            
            export_format = request.POST.get('format', 'pdf')
            export_options = {
                'include_answers': request.POST.get('include_answers') == 'on',
                'include_explanations': request.POST.get('include_explanations') == 'on',
                'watermark': request.POST.get('watermark', ''),
                'format': export_format
            }
            
            # Create export job
            export_job = ExportJob.objects.create(
                generation=generation,
                export_format=export_format,
                export_options=export_options,
                status='pending'
            )
            
            # Process export
            export_service = ExportService()
            result = export_service.export_generation(export_job)
            
            if result['success']:
                messages.success(request, 'Export completed successfully!')
                return redirect('exports:detail', pk=export_job.id)
            else:
                messages.error(request, f'Export failed: {result.get("error")}')
        
        except Exception as e:
            messages.error(request, f'Error creating export: {str(e)}')
    
    context = {
        'title': f'Export - {generation.title}',
        'generation': generation,
    }
    
    return render(request, 'ai_generator/export_form.html', context)
