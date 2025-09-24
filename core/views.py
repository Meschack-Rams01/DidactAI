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
        'title': 'DidactIA - Educational Content Management Platform',
        'description': 'AI-powered educational content generation and management platform',
    }
    return render(request, 'core/home.html', context)


@login_required
def dashboard(request):
    """User dashboard view"""
    try:
        from analytics.services import AnalyticsService
        
        # Get dashboard data
        analytics_service = AnalyticsService()
        dashboard_data = analytics_service.get_user_dashboard_data(request.user)
    except Exception as e:
        # Fallback if analytics service fails
        dashboard_data = {
            'activity_summary': {'total_activities': 0},
            'content_stats': {
                'courses_created': 0,
                'files_uploaded': 0,
                'ai_generations': 0,
                'exports_created': 0
            },
            'recent_activities': [],
            'achievement_progress': [],
            'learning_streak': {'current_streak': 0, 'longest_streak': 0}
        }
    
    context = {
        'title': 'Dashboard',
        'dashboard_data': dashboard_data,
        'user': request.user,
    }
    
    return render(request, 'simple_dashboard.html', context)


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
        'message': 'DidactIA is running successfully',
        'features': {
            'ai_generation': True,
            'file_upload': True,
            'analytics': True,
            'versioning': True,
            'internationalization': True,
        }
    })
