"""
File Upload Views
"""

import os
import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.conf import settings
from django.utils import timezone

from .models import UploadedFile, FileShare, ProcessingLog
from courses.models import Course
from .services import FileProcessor


@login_required
def file_list(request):
    """Display user's uploaded files"""
    # Get user's courses
    user_courses = Course.objects.filter(instructor=request.user)
    
    # Get files for user's courses
    files = UploadedFile.objects.filter(
        course__instructor=request.user
    ).select_related('course').order_by('-created_at')
    
    # Filter by course if specified
    course_id = request.GET.get('course')
    if course_id:
        files = files.filter(course_id=course_id)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        files = files.filter(
            Q(original_filename__icontains=search) |
            Q(description__icontains=search) |
            Q(extracted_text__icontains=search)
        )
    
    # Filter by file type
    file_type = request.GET.get('type')
    if file_type:
        files = files.filter(file_type=file_type)
    
    # Pagination
    paginator = Paginator(files, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_files = files.count()
    total_size = files.aggregate(total=Sum('file_size'))['total'] or 0
    
    context = {
        'title': 'My Files',
        'files': page_obj,
        'courses': user_courses,
        'selected_course': course_id,
        'search': search,
        'selected_type': file_type,
        'total_files': total_files,
        'total_size': format_file_size(total_size),
        'file_types': UploadedFile.FILE_TYPE_CHOICES,
    }
    
    return render(request, 'uploads/file_list.html', context)


@login_required
def upload_file(request):
    """Handle file upload"""
    user_courses = Course.objects.filter(instructor=request.user)
    
    if request.method == 'POST':
        course_id = request.POST.get('course')
        uploaded_file = request.FILES.get('file')
        description = request.POST.get('description', '')
        
        if not course_id or not uploaded_file:
            messages.error(request, 'Please select a course and choose a file to upload.')
            return render(request, 'uploads/upload_form.html', {'courses': user_courses})
        
        try:
            course = Course.objects.get(id=course_id, instructor=request.user)
        except Course.DoesNotExist:
            messages.error(request, 'Invalid course selected.')
            return render(request, 'uploads/upload_form.html', {'courses': user_courses})
        
        # Validate file size (10MB limit for demo)
        max_size = 10 * 1024 * 1024  # 10MB
        if uploaded_file.size > max_size:
            messages.error(request, f'File size exceeds {format_file_size(max_size)} limit.')
            return render(request, 'uploads/upload_form.html', {'courses': user_courses})
        
        # Determine file type
        file_type = get_file_type(uploaded_file.name, uploaded_file.content_type)
        
        # Calculate file checksum
        checksum = calculate_file_checksum(uploaded_file)
        
        # Create file record
        file_record = UploadedFile.objects.create(
            course=course,
            original_filename=uploaded_file.name,
            file=uploaded_file,
            file_type=file_type,
            file_size=uploaded_file.size,
            mime_type=uploaded_file.content_type,
            description=description,
            checksum=checksum,
            status='uploading'
        )
        
        # Process file to extract content
        processor = FileProcessor()
        processing_result = processor.process_file(file_record)
        
        # Log the upload
        ProcessingLog.objects.create(
            file=file_record,
            level='success',
            message=f'File uploaded successfully: {uploaded_file.name}'
        )
        
        messages.success(request, f'File "{uploaded_file.name}" uploaded successfully!')
        return redirect('uploads:detail', file_id=file_record.id)
    
    context = {
        'title': 'Upload File',
        'courses': user_courses,
    }
    
    return render(request, 'uploads/upload_form.html', context)


@login_required
def file_detail(request, file_id):
    """Display file details"""
    file_obj = get_object_or_404(
        UploadedFile, 
        id=file_id, 
        course__instructor=request.user
    )
    
    # Get processing logs
    logs = file_obj.processing_logs.all()[:10]
    
    # Get file shares
    shares = file_obj.shares.filter(is_active=True)
    
    context = {
        'title': file_obj.original_filename,
        'file': file_obj,
        'logs': logs,
        'shares': shares,
    }
    
    return render(request, 'uploads/file_detail.html', context)


@login_required
def download_file(request, file_id):
    """Download a file"""
    file_obj = get_object_or_404(
        UploadedFile, 
        id=file_id, 
        course__instructor=request.user
    )
    
    # Increment download count
    file_obj.increment_download_count()
    
    # Serve file
    response = HttpResponse(
        file_obj.file.read(), 
        content_type=file_obj.mime_type or 'application/octet-stream'
    )
    response['Content-Disposition'] = f'attachment; filename="{file_obj.original_filename}"'
    
    return response


@login_required
def delete_file(request, file_id):
    """Delete a file"""
    file_obj = get_object_or_404(
        UploadedFile, 
        id=file_id, 
        course__instructor=request.user
    )
    
    if request.method == 'POST':
        filename = file_obj.original_filename
        
        # Delete physical file
        if file_obj.file:
            try:
                os.remove(file_obj.file.path)
            except OSError:
                pass
        
        # Delete database record
        file_obj.delete()
        
        messages.success(request, f'File "{filename}" deleted successfully.')
        return redirect('uploads:list')
    
    context = {
        'title': f'Delete {file_obj.original_filename}',
        'file': file_obj,
    }
    
    return render(request, 'uploads/confirm_delete.html', context)


# Utility functions
def get_file_type(filename, mime_type):
    """Determine file type from filename and MIME type"""
    ext = os.path.splitext(filename)[1].lower()
    
    if ext in ['.pdf']:
        return 'pdf'
    elif ext in ['.doc', '.docx']:
        return 'docx'
    elif ext in ['.ppt', '.pptx']:
        return 'pptx'
    elif ext in ['.txt', '.md', '.rtf']:
        return 'txt'
    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
        return 'image'
    elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv']:
        return 'video'
    elif ext in ['.mp3', '.wav', '.flac', '.aac']:
        return 'audio'
    else:
        return 'other'


def calculate_file_checksum(file_obj):
    """Calculate SHA-256 checksum of a file"""
    hash_sha256 = hashlib.sha256()
    for chunk in file_obj.chunks():
        hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"


# AJAX endpoints
@login_required
@require_http_methods(["POST"])
def ajax_upload(request):
    """Handle AJAX file upload"""
    if not request.FILES.get('file'):
        return JsonResponse({'success': False, 'error': 'No file provided'})
    
    course_id = request.POST.get('course_id')
    if not course_id:
        return JsonResponse({'success': False, 'error': 'No course specified'})
    
    try:
        course = Course.objects.get(id=course_id, instructor=request.user)
        uploaded_file = request.FILES['file']
        
        # Basic validation
        max_size = 10 * 1024 * 1024  # 10MB
        if uploaded_file.size > max_size:
            return JsonResponse({
                'success': False, 
                'error': f'File size exceeds {format_file_size(max_size)} limit'
            })
        
        # Create file record
        file_record = UploadedFile.objects.create(
            course=course,
            original_filename=uploaded_file.name,
            file=uploaded_file,
            file_type=get_file_type(uploaded_file.name, uploaded_file.content_type),
            file_size=uploaded_file.size,
            mime_type=uploaded_file.content_type,
            checksum=calculate_file_checksum(uploaded_file),
            status='uploading'
        )
        
        # Process file to extract content
        processor = FileProcessor()
        processing_result = processor.process_file(file_record)
        
        return JsonResponse({
            'success': True,
            'file_id': file_record.id,
            'filename': file_record.original_filename,
            'file_size': format_file_size(file_record.file_size),
            'file_type': file_record.get_file_type_display()
        })
        
    except Course.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid course'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def api_course_files(request, course_id):
    """API endpoint to get files for a specific course"""
    try:
        course = Course.objects.get(id=course_id, instructor=request.user)
        files = UploadedFile.objects.filter(
            course=course,
            is_processed=True
        ).order_by('-created_at')
        
        files_data = []
        for file_obj in files:
            files_data.append({
                'id': file_obj.id,
                'original_filename': file_obj.original_filename,
                'file_type': file_obj.file_type,
                'file_size_human': file_obj.file_size_human,
                'status': file_obj.status,
                'created_at': file_obj.created_at.strftime('%Y-%m-%d %H:%M'),
            })
        
        return JsonResponse(files_data, safe=False)
        
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
