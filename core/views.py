from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils.translation import gettext as _
from django.conf import settings


def home(request):
    """Home page view"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    context = {
        'title': 'DidactAI - Educational Content Management Platform',
        'description': 'AI-powered educational content generation and management platform',
    }
    return render(request, 'core/home.html', context)


@login_required
def dashboard(request):
    """User dashboard view with real-time statistics"""
    
    # Get real data from database
    from courses.models import Course
    from uploads.models import UploadedFile
    from ai_generator.models import AIGeneration
    from exports.models import ExportJob
    
    # Calculate actual statistics for current user
    user_courses = Course.objects.filter(instructor=request.user)
    user_files = UploadedFile.objects.filter(course__instructor=request.user)  # Files linked through course
    user_generations = AIGeneration.objects.filter(course__instructor=request.user)
    user_exports = ExportJob.objects.filter(course__instructor=request.user)
    
    # Calculate growth percentages (basic implementation)
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Recent counts for growth calculation
    recent_courses = user_courses.filter(created_at__gte=thirty_days_ago).count()
    recent_files = user_files.filter(created_at__gte=thirty_days_ago).count()
    recent_generations = user_generations.filter(created_at__gte=thirty_days_ago).count()
    recent_exports = user_exports.filter(created_at__gte=thirty_days_ago).count()
    
    # Calculate simple growth percentages
    total_courses = user_courses.count()
    total_files = user_files.count()
    total_generations = user_generations.count()
    total_exports = user_exports.count()
    
    def calculate_growth(recent, total):
        if total == 0:
            return 0
        return min(100, (recent / max(1, total - recent)) * 100) if total > recent else 0
    
    # Real statistics
    stats = {
        'total_courses': total_courses,
        'total_files': total_files,
        'total_generations': total_generations,
        'total_exports': total_exports,
        'courses_growth': calculate_growth(recent_courses, total_courses),
        'files_growth': calculate_growth(recent_files, total_files),
        'generations_growth': calculate_growth(recent_generations, total_generations),
        'exports_growth': calculate_growth(recent_exports, total_exports),
    }
    
    # Get recent activities (simple implementation)
    recent_activities = []
    
    # Add recent course activities
    for course in user_courses.order_by('-created_at')[:3]:
        recent_activities.append({
            'action': 'course_created',
            'description': f'Created course "{course.title}"',
            'created_at': course.created_at,
            'get_action_display': 'Course Created'
        })
    
    # Add recent file activities
    for file in user_files.order_by('-created_at')[:3]:
        recent_activities.append({
            'action': 'file_uploaded',
            'description': f'Uploaded file "{file.original_filename}"',
            'created_at': file.created_at,
            'get_action_display': 'File Uploaded'
        })
    
    # Add recent generation activities
    for generation in user_generations.order_by('-created_at')[:3]:
        recent_activities.append({
            'action': 'content_generated',
            'description': f'Generated {generation.content_type}: "{generation.title}"',
            'created_at': generation.created_at,
            'get_action_display': 'Content Generated'
        })
    
    # Sort activities by date
    recent_activities.sort(key=lambda x: x['created_at'], reverse=True)
    recent_activities = recent_activities[:10]  # Keep only top 10
    
    # Try to get analytics data as additional context
    dashboard_data = {
        'content_stats': {
            'courses_created': total_courses,
            'files_uploaded': total_files,
            'ai_generations': total_generations,
            'exports_created': total_exports
        },
        'recent_activities': recent_activities,
    }
    
    try:
        from analytics.services import AnalyticsService
        analytics_service = AnalyticsService()
        extra_data = analytics_service.get_user_dashboard_data(request.user)
        dashboard_data.update(extra_data)
    except Exception as e:
        # Continue with basic data if analytics fails
        print(f"Analytics service unavailable: {e}")
    
    context = {
        'title': 'Dashboard',
        'stats': stats,  # Main dashboard template expects 'stats'
        'dashboard_data': dashboard_data,  # Keep for compatibility
        'recent_activities': recent_activities,
        'user': request.user,
    }
    
    # Use the main dashboard template with real data
    return render(request, 'dashboard.html', context)


@login_required
@require_http_methods(["POST"])
def test_notification(request):
    """Test notification endpoint for the dashboard"""
    notification_type = request.POST.get('type', 'info')
    
    if notification_type == 'success':
        messages.success(request, _('This is a test success notification!'))
    elif notification_type == 'warning':
        messages.warning(request, _('This is a test warning notification!'))
    elif notification_type == 'error':
        messages.error(request, _('This is a test error notification!'))
    else:
        messages.info(request, _('This is a test info notification!'))
    
    return JsonResponse({'status': 'success'})


@login_required
def activity(request):
    """Activity page view"""
    try:
        from analytics.services import AnalyticsService
        
        # Get activity data
        analytics_service = AnalyticsService()
        activity_data = analytics_service.get_user_activity_timeline(request.user)
    except Exception as e:
        # Fallback if analytics service fails
        activity_data = {
            'activities': [],
            'total_count': 0,
        }
    
    context = {
        'title': 'Activity Timeline',
        'activity_data': activity_data,
        'user': request.user,
    }
    
    return render(request, 'core/activity.html', context)


def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'DidactAI is running successfully',
        'features': {
            'ai_generation': True,
            'file_upload': True,
            'analytics': True,
            'versioning': True,
            'internationalization': True,
        }
    })

