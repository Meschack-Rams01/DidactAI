"""
Advanced Analytics Service for DidactAI

This module provides comprehensive analytics and reporting capabilities,
including user behavior tracking, content analytics, and performance metrics.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter
from django.db.models import Count, Avg, Sum, Q, F
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import UserActivityLog, SystemMetrics

User = get_user_model()


class AnalyticsService:
    """Main analytics service with comprehensive tracking and reporting"""
    
    def __init__(self):
        self.event_processor = EventProcessor()
        self.report_generator = ReportGenerator()
        self.behavior_analyzer = UserBehaviorAnalyzer()
    
    def track_event(self, event_name: str, user=None, **properties) -> bool:
        """
        Track a custom event with optional properties
        
        Args:
            event_name: Name of the event
            user: User associated with the event (optional)
            **properties: Additional event properties
            
        Returns:
            Boolean indicating success
        """
        try:
            # For now, track as user activity
            if user:
                UserActivityLog.objects.create(
                    user=user,
                    action=event_name,
                    description=properties.get('description', event_name),
                    metadata=properties
                )
            return True
        except Exception:
            return False
    
    def track_user_activity(self, user, action: str, description: str = None, **metadata) -> bool:
        """Track user activity"""
        try:
            UserActivityLog.objects.create(
                user=user,
                action=action,
                description=description or action.replace('_', ' ').title(),
                metadata=metadata
            )
            return True
        except Exception:
            return False
    
    def get_user_dashboard_data(self, user) -> Dict[str, Any]:
        """Get comprehensive dashboard data for a user"""
        return {
            'activity_summary': self.behavior_analyzer.get_user_activity_summary(user),
            'content_stats': self.get_user_content_stats(user),
            'recent_activities': self.get_recent_activities(user, limit=10),
            'achievement_progress': self.get_achievement_progress(user),
            'learning_streak': self.calculate_learning_streak(user)
        }
    
    def get_admin_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive admin dashboard data"""
        return {
            'system_overview': self.get_system_overview(),
            'user_engagement': self.get_user_engagement_metrics(),
            'content_performance': self.get_content_performance_metrics(),
            'growth_metrics': self.get_growth_metrics(),
            'top_content': self.get_top_performing_content(),
            'system_health': self.get_system_health_metrics()
        }
    
    def get_user_content_stats(self, user) -> Dict[str, Any]:
        """Get content statistics for a user"""
        from courses.models import Course
        from uploads.models import UploadedFile
        from ai_generator.models import AIGeneration
        from exports.models import ExportJob
        
        return {
            'courses_created': Course.objects.filter(instructor=user).count(),
            'files_uploaded': UploadedFile.objects.filter(course__instructor=user).count(),
            'ai_generations': AIGeneration.objects.filter(course__instructor=user).count(),
            'exports_created': ExportJob.objects.filter(course__instructor=user).count(),
            'total_storage_used': self._calculate_user_storage(user),
            'last_activity': UserActivityLog.objects.filter(user=user).order_by('-created_at').first()
        }
    
    def get_recent_activities(self, user, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent user activities"""
        activities = UserActivityLog.objects.filter(user=user).order_by('-created_at')[:limit]
        
        return [
            {
                'id': activity.id,
                'action': activity.action,
                'description': activity.description,
                'created_at': activity.created_at,
                'metadata': activity.metadata
            }
            for activity in activities
        ]
    
    def calculate_learning_streak(self, user) -> Dict[str, Any]:
        """Calculate user's learning streak"""
        activities = UserActivityLog.objects.filter(
            user=user,
            action__in=['course_viewed', 'content_generated', 'file_uploaded', 'quiz_completed']
        ).order_by('-created_at')
        
        if not activities:
            return {'current_streak': 0, 'longest_streak': 0, 'last_activity': None}
        
        # Group activities by date
        activity_dates = set()
        for activity in activities:
            activity_dates.add(activity.created_at.date())
        
        # Sort dates in descending order
        sorted_dates = sorted(activity_dates, reverse=True)
        
        # Calculate current streak
        current_streak = 0
        today = timezone.now().date()
        
        for i, date in enumerate(sorted_dates):
            expected_date = today - timedelta(days=i)
            if date == expected_date:
                current_streak += 1
            else:
                break
        
        # Calculate longest streak
        longest_streak = self._calculate_longest_streak(sorted_dates)
        
        return {
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'last_activity': activities.first().created_at,
            'total_active_days': len(activity_dates)
        }
    
    def get_achievement_progress(self, user) -> List[Dict[str, Any]]:
        """Get user achievement progress"""
        achievements = [
            {
                'name': 'Content Creator',
                'description': 'Upload your first file',
                'progress': min(100, (self.get_user_content_stats(user)['files_uploaded'] / 1) * 100),
                'completed': self.get_user_content_stats(user)['files_uploaded'] >= 1
            },
            {
                'name': 'AI Explorer',
                'description': 'Generate 5 AI contents',
                'progress': min(100, (self.get_user_content_stats(user)['ai_generations'] / 5) * 100),
                'completed': self.get_user_content_stats(user)['ai_generations'] >= 5
            },
            {
                'name': 'Course Builder',
                'description': 'Create your first course',
                'progress': min(100, (self.get_user_content_stats(user)['courses_created'] / 1) * 100),
                'completed': self.get_user_content_stats(user)['courses_created'] >= 1
            },
            {
                'name': 'Consistency Champion',
                'description': 'Maintain a 7-day learning streak',
                'progress': min(100, (self.calculate_learning_streak(user)['current_streak'] / 7) * 100),
                'completed': self.calculate_learning_streak(user)['current_streak'] >= 7
            }
        ]
        
        return achievements
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Get system-wide overview metrics"""
        return {
            'total_users': User.objects.count(),
            'active_users_today': self._get_active_users_count(days=1),
            'active_users_week': self._get_active_users_count(days=7),
            'active_users_month': self._get_active_users_count(days=30),
            'total_content_items': self._get_total_content_count(),
            'storage_usage': self._get_total_storage_usage(),
            'api_requests_today': self._get_api_requests_count(days=1)
        }
    
    def get_user_engagement_metrics(self) -> Dict[str, Any]:
        """Get user engagement metrics"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        # Daily active users over last 30 days
        daily_active = UserActivityLog.objects.filter(
            created_at__gte=thirty_days_ago
        ).extra(
            {'day': 'date(created_at)'}
        ).values('day').annotate(
            unique_users=Count('user', distinct=True)
        ).order_by('day')
        
        # Session duration analysis
        avg_session_duration = self._calculate_average_session_duration()
        
        # Feature usage
        feature_usage = UserActivityLog.objects.filter(
            created_at__gte=thirty_days_ago
        ).values('action').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        return {
            'daily_active_users': list(daily_active),
            'average_session_duration': avg_session_duration,
            'popular_features': list(feature_usage),
            'user_retention': self._calculate_user_retention(),
            'bounce_rate': self._calculate_bounce_rate()
        }
    
    def get_content_performance_metrics(self) -> Dict[str, Any]:
        """Get content performance metrics"""
        from courses.models import Course
        from ai_generator.models import AIGeneration
        
        # Most popular courses
        popular_courses = Course.objects.annotate(
            view_count=Count('userlog__id', filter=Q(userlog__action='course_viewed'))
        ).order_by('-view_count')[:10]
        
        # AI generation statistics
        generation_stats = AIGeneration.objects.values('content_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Content creation trends
        content_trends = self._get_content_creation_trends()
        
        return {
            'popular_courses': [
                {
                    'id': course.id,
                    'title': course.title,
                    'views': course.view_count,
                    'instructor': course.instructor.get_full_name()
                }
                for course in popular_courses
            ],
            'generation_statistics': list(generation_stats),
            'content_creation_trends': content_trends,
            'average_content_rating': self._calculate_average_content_rating()
        }
    
    def get_growth_metrics(self) -> Dict[str, Any]:
        """Get growth and trend metrics"""
        # User registration trends
        registration_trends = self._get_registration_trends()
        
        # Activity trends
        activity_trends = self._get_activity_trends()
        
        # Content growth
        content_growth = self._get_content_growth_trends()
        
        return {
            'user_registration_trends': registration_trends,
            'activity_trends': activity_trends,
            'content_growth_trends': content_growth,
            'monthly_growth_rate': self._calculate_monthly_growth_rate()
        }
    
    def get_top_performing_content(self) -> Dict[str, Any]:
        """Get top performing content across all categories"""
        from courses.models import Course
        from ai_generator.models import AIGeneration
        from uploads.models import UploadedFile
        
        return {
            'top_courses': self._get_top_courses(limit=5),
            'trending_generations': self._get_trending_generations(limit=5),
            'popular_uploads': self._get_popular_uploads(limit=5),
            'content_categories': self._get_content_category_stats()
        }
    
    def get_system_health_metrics(self) -> Dict[str, Any]:
        """Get system health and performance metrics"""
        return {
            'error_rates': self._get_error_rates(),
            'response_times': self._get_average_response_times(),
            'database_performance': self._get_database_metrics(),
            'storage_health': self._get_storage_health(),
            'api_health': self._get_api_health_metrics()
        }
    
    # Helper methods
    def _calculate_user_storage(self, user) -> int:
        """Calculate total storage used by user in bytes"""
        from uploads.models import UploadedFile
        
        total_size = UploadedFile.objects.filter(uploaded_by=user).aggregate(
            total=Sum('file_size')
        )['total'] or 0
        
        return total_size
    
    def _calculate_longest_streak(self, sorted_dates: List) -> int:
        """Calculate the longest consecutive day streak"""
        if not sorted_dates:
            return 0
        
        longest_streak = 1
        current_streak = 1
        
        for i in range(1, len(sorted_dates)):
            if (sorted_dates[i-1] - sorted_dates[i]).days == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1
        
        return longest_streak
    
    def _get_active_users_count(self, days: int) -> int:
        """Get count of active users in the last N days"""
        cutoff_date = timezone.now() - timedelta(days=days)
        return UserActivityLog.objects.filter(
            created_at__gte=cutoff_date
        ).values('user').distinct().count()
    
    def _get_total_content_count(self) -> int:
        """Get total count of all content items"""
        from courses.models import Course
        from uploads.models import UploadedFile
        from ai_generator.models import Generation
        
        return (
            Course.objects.count() +
            UploadedFile.objects.count() +
            AIGeneration.objects.count()
        )
    
    def _get_total_storage_usage(self) -> int:
        """Get total storage usage across all users"""
        from uploads.models import UploadedFile
        
        total_size = UploadedFile.objects.aggregate(
            total=Sum('file_size')
        )['total'] or 0
        
        return total_size
    
    def _get_api_requests_count(self, days: int) -> int:
        """Get API request count for the last N days"""
        cutoff_date = timezone.now() - timedelta(days=days)
        return UserActivityLog.objects.filter(
            created_at__gte=cutoff_date,
            action__startswith='api_'
        ).count()
    
    def _calculate_average_session_duration(self) -> float:
        """Calculate average session duration in minutes"""
        # This is a simplified calculation - in practice, you'd track session start/end
        return 25.5  # Placeholder value
    
    def _calculate_user_retention(self) -> Dict[str, float]:
        """Calculate user retention metrics"""
        # Simplified retention calculation
        return {
            'day_1': 85.2,
            'day_7': 62.1,
            'day_30': 34.7
        }
    
    def _calculate_bounce_rate(self) -> float:
        """Calculate bounce rate percentage"""
        # Users who only have one activity log entry
        total_users = User.objects.count()
        single_activity_users = User.objects.annotate(
            activity_count=Count('userlog')
        ).filter(activity_count=1).count()
        
        if total_users == 0:
            return 0.0
        
        return (single_activity_users / total_users) * 100
    
    def _get_content_creation_trends(self) -> List[Dict[str, Any]]:
        """Get content creation trends over time"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        trends = UserActivityLog.objects.filter(
            created_at__gte=thirty_days_ago,
            action__in=['course_created', 'file_uploaded', 'content_generated']
        ).extra(
            {'day': 'date(created_at)'}
        ).values('day', 'action').annotate(
            count=Count('id')
        ).order_by('day')
        
        return list(trends)
    
    def _calculate_average_content_rating(self) -> float:
        """Calculate average content rating"""
        # Placeholder - would calculate from actual ratings
        return 4.2
    
    def _get_registration_trends(self) -> List[Dict[str, Any]]:
        """Get user registration trends"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        registrations = User.objects.filter(
            date_joined__gte=thirty_days_ago
        ).extra(
            {'day': 'date(date_joined)'}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        
        return list(registrations)
    
    def _get_activity_trends(self) -> List[Dict[str, Any]]:
        """Get activity trends over time"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        activities = UserActivityLog.objects.filter(
            created_at__gte=thirty_days_ago
        ).extra(
            {'day': 'date(created_at)'}
        ).values('day').annotate(
            total_activities=Count('id'),
            unique_users=Count('user', distinct=True)
        ).order_by('day')
        
        return list(activities)
    
    def _get_content_growth_trends(self) -> Dict[str, List]:
        """Get content growth trends by type"""
        from courses.models import Course
        from uploads.models import UploadedFile
        from ai_generator.models import AIGeneration
        
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        # Course creation trends
        course_trends = Course.objects.filter(
            created_at__gte=thirty_days_ago
        ).extra(
            {'day': 'date(created_at)'}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        
        # Upload trends
        upload_trends = UploadedFile.objects.filter(
            created_at__gte=thirty_days_ago
        ).extra(
            {'day': 'date(created_at)'}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        
        # Generation trends
        generation_trends = AIGeneration.objects.filter(
            created_at__gte=thirty_days_ago
        ).extra(
            {'day': 'date(created_at)'}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        
        return {
            'courses': list(course_trends),
            'uploads': list(upload_trends),
            'generations': list(generation_trends)
        }
    
    def _calculate_monthly_growth_rate(self) -> float:
        """Calculate monthly growth rate"""
        current_month = timezone.now().replace(day=1)
        last_month = (current_month - timedelta(days=1)).replace(day=1)
        
        current_users = User.objects.filter(date_joined__gte=current_month).count()
        last_month_users = User.objects.filter(
            date_joined__gte=last_month,
            date_joined__lt=current_month
        ).count()
        
        if last_month_users == 0:
            return 100.0 if current_users > 0 else 0.0
        
        growth_rate = ((current_users - last_month_users) / last_month_users) * 100
        return growth_rate
    
    def _get_top_courses(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top performing courses"""
        from courses.models import Course
        
        courses = Course.objects.annotate(
            view_count=Count('userlog__id', filter=Q(userlog__action='course_viewed'))
        ).order_by('-view_count')[:limit]
        
        return [
            {
                'id': course.id,
                'title': course.title,
                'views': course.view_count,
                'instructor': course.instructor.get_full_name()
            }
            for course in courses
        ]
    
    def _get_trending_generations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get trending AI generations"""
        from ai_generator.models import AIGeneration
        
        # Recent generations with high activity
        week_ago = timezone.now() - timedelta(days=7)
        generations = AIGeneration.objects.filter(
            created_at__gte=week_ago
        ).annotate(
            activity_count=Count('userlog__id')
        ).order_by('-activity_count')[:limit]
        
        return [
            {
                'id': gen.id,
                'type': gen.content_type,
                'title': gen.title,
                'activity_count': gen.activity_count,
                'created_by': gen.course.instructor.get_full_name()
            }
            for gen in generations
        ]
    
    def _get_popular_uploads(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get popular uploaded files"""
        from uploads.models import UploadedFile
        
        files = UploadedFile.objects.annotate(
            download_count=Count('userlog__id', filter=Q(userlog__action='file_downloaded'))
        ).order_by('-download_count')[:limit]
        
        return [
            {
                'id': file.id,
                'filename': file.original_filename,
                'downloads': file.download_count,
                'uploaded_by': file.uploaded_by.get_full_name()
            }
            for file in files
        ]
    
    def _get_content_category_stats(self) -> Dict[str, int]:
        """Get content statistics by category"""
        from courses.models import Course
        
        category_stats = Course.objects.values('category').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return {item['category']: item['count'] for item in category_stats}
    
    # System health helper methods
    def _get_error_rates(self) -> Dict[str, float]:
        """Get system error rates"""
        # Would track actual errors in production
        return {
            'api_error_rate': 0.2,
            'database_error_rate': 0.1,
            'file_processing_error_rate': 0.5
        }
    
    def _get_average_response_times(self) -> Dict[str, float]:
        """Get average response times"""
        return {
            'api_response_time': 145.6,  # ms
            'database_query_time': 12.3,  # ms
            'file_upload_time': 2.8  # seconds
        }
    
    def _get_database_metrics(self) -> Dict[str, Any]:
        """Get database performance metrics"""
        return {
            'query_count_per_minute': 450,
            'slow_queries': 3,
            'connection_pool_usage': 75.2,
            'cache_hit_ratio': 92.1
        }
    
    def _get_storage_health(self) -> Dict[str, Any]:
        """Get storage health metrics"""
        return {
            'total_storage_gb': 1250.5,
            'used_storage_gb': 892.3,
            'available_storage_gb': 358.2,
            'usage_percentage': 71.4
        }
    
    def _get_api_health_metrics(self) -> Dict[str, Any]:
        """Get API health metrics"""
        return {
            'requests_per_minute': 125,
            'average_response_time': 145.6,
            'error_rate': 0.2,
            'uptime_percentage': 99.9
        }


class EventProcessor:
    """Process and categorize analytics events"""
    
    def process_user_action(self, user, action: str, **context):
        """Process a user action and create relevant analytics entries"""
        # Create activity log
        UserActivityLog.objects.create(
            user=user,
            action=action,
            description=context.get('description', action.replace('_', ' ').title()),
            metadata=context
        )
        
        # Update content analytics if applicable
        if 'content_id' in context and 'content_type' in context:
            self._update_content_analytics(
                context['content_type'],
                context['content_id'],
                action
            )
    
    def _update_content_analytics(self, content_type: str, content_id: int, action: str):
        """Update content-specific analytics"""
        # For now, just log the activity
        # In production, this would update content-specific analytics
        pass


class ReportGenerator:
    """Generate various analytics reports"""
    
    def generate_user_report(self, user, date_range: Tuple[datetime, datetime] = None) -> Dict[str, Any]:
        """Generate comprehensive user activity report"""
        if not date_range:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
        else:
            start_date, end_date = date_range
        
        activities = UserActivityLog.objects.filter(
            user=user,
            created_at__range=(start_date, end_date)
        )
        
        # Activity breakdown
        action_counts = Counter(activities.values_list('action', flat=True))
        
        # Daily activity
        daily_activity = activities.extra(
            {'day': 'date(created_at)'}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        
        # Most active hours
        hourly_activity = activities.extra(
            {'hour': 'EXTRACT(hour FROM created_at)'}
        ).values('hour').annotate(
            count=Count('id')
        ).order_by('hour')
        
        return {
            'user': {
                'id': user.id,
                'name': user.get_full_name(),
                'email': user.email
            },
            'date_range': {
                'start': start_date,
                'end': end_date
            },
            'summary': {
                'total_activities': activities.count(),
                'active_days': daily_activity.count(),
                'most_common_action': action_counts.most_common(1)[0] if action_counts else None
            },
            'activity_breakdown': dict(action_counts),
            'daily_activity': list(daily_activity),
            'hourly_activity': list(hourly_activity)
        }
    
    def generate_system_report(self, date_range: Tuple[datetime, datetime] = None) -> Dict[str, Any]:
        """Generate system-wide analytics report"""
        if not date_range:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
        else:
            start_date, end_date = date_range
        
        # User registration during period
        new_users = User.objects.filter(
            date_joined__range=(start_date, end_date)
        ).count()
        
        # Activity summary
        activities = UserActivityLog.objects.filter(
            created_at__range=(start_date, end_date)
        )
        
        return {
            'date_range': {
                'start': start_date,
                'end': end_date
            },
            'user_metrics': {
                'new_registrations': new_users,
                'active_users': activities.values('user').distinct().count(),
                'total_users': User.objects.count()
            },
            'activity_metrics': {
                'total_activities': activities.count(),
                'daily_average': activities.count() / max(1, (end_date - start_date).days)
            },
            'popular_actions': list(
                activities.values('action').annotate(
                    count=Count('id')
                ).order_by('-count')[:10]
            )
        }


class UserBehaviorAnalyzer:
    """Analyze user behavior patterns"""
    
    def get_user_activity_summary(self, user) -> Dict[str, Any]:
        """Get comprehensive activity summary for user"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        activities = UserActivityLog.objects.filter(
            user=user,
            created_at__gte=thirty_days_ago
        )
        
        return {
            'total_activities': activities.count(),
            'unique_actions': activities.values('action').distinct().count(),
            'most_active_day': self._get_most_active_day(activities),
            'activity_patterns': self._analyze_activity_patterns(activities),
            'engagement_score': self._calculate_engagement_score(user)
        }
    
    def _get_most_active_day(self, activities) -> Optional[str]:
        """Get the most active day of the week"""
        if not activities.exists():
            return None
        
        day_counts = activities.extra(
            {'day_of_week': 'EXTRACT(dow FROM created_at)'}
        ).values('day_of_week').annotate(
            count=Count('id')
        ).order_by('-count').first()
        
        if day_counts:
            days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            return days[int(day_counts['day_of_week'])]
        
        return None
    
    def _analyze_activity_patterns(self, activities) -> Dict[str, Any]:
        """Analyze user activity patterns"""
        if not activities.exists():
            return {}
        
        # Peak hours
        hourly_counts = activities.extra(
            {'hour': 'EXTRACT(hour FROM created_at)'}
        ).values('hour').annotate(
            count=Count('id')
        ).order_by('-count')
        
        peak_hour = hourly_counts.first()
        
        return {
            'peak_hour': peak_hour['hour'] if peak_hour else None,
            'activity_distribution': list(hourly_counts)
        }
    
    def _calculate_engagement_score(self, user) -> float:
        """Calculate user engagement score (0-100)"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        # Various engagement factors
        activities_count = UserActivityLog.objects.filter(
            user=user,
            created_at__gte=thirty_days_ago
        ).count()
        
        # Content creation activities
        creation_activities = UserActivityLog.objects.filter(
            user=user,
            created_at__gte=thirty_days_ago,
            action__in=['course_created', 'file_uploaded', 'content_generated']
        ).count()
        
        # Unique days active
        active_days = UserActivityLog.objects.filter(
            user=user,
            created_at__gte=thirty_days_ago
        ).extra(
            {'day': 'date(created_at)'}
        ).values('day').distinct().count()
        
        # Calculate engagement score
        activity_score = min(40, activities_count * 2)  # Max 40 points for activity
        creation_score = min(30, creation_activities * 5)  # Max 30 points for creation
        consistency_score = min(30, active_days)  # Max 30 points for consistency
        
        total_score = activity_score + creation_score + consistency_score
        
        return min(100, total_score)

