"""
Export Analytics Module for DidactAI

This module provides comprehensive analytics tracking for export functionality,
including download statistics, usage patterns, format preferences, and performance metrics.
"""

import logging
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional
from django.utils import timezone
from django.db.models import Count, Q, Avg, Sum, Min, Max
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()


class ExportAnalytics:
    """Comprehensive analytics for export functionality"""
    
    def __init__(self):
        self.logger = logger
    
    def track_export_download(self, export_job, user, format_type: str, content_type: str):
        """Track export download event"""
        try:
            # Import here to avoid circular imports
            from .models import ExportLog
            
            # Log the download event
            ExportLog.objects.create(
                export_job=export_job,
                level='info',
                message=f'Export downloaded by {user.username}',
                details={
                    'format_type': format_type,
                    'content_type': content_type,
                    'download_timestamp': timezone.now().isoformat(),
                    'user_id': user.id,
                    'file_size': export_job.file_size,
                    'processing_time': export_job.processing_time_seconds
                }
            )
            
            self.logger.info(
                f"Export download tracked: {format_type} format, "
                f"{content_type} content, user: {user.username}"
            )
            
        except Exception as e:
            self.logger.error(f"Error tracking export download: {str(e)}")
    
    def track_export_creation(self, export_job, user, creation_details: Dict[str, Any]):
        """Track export creation event"""
        try:
            from .models import ExportLog
            
            ExportLog.objects.create(
                export_job=export_job,
                level='info',
                message=f'Export created by {user.username}',
                details={
                    'creation_timestamp': timezone.now().isoformat(),
                    'user_id': user.id,
                    'branding_configured': bool(creation_details.get('branding')),
                    'versions_created': creation_details.get('versions', 1),
                    'include_answer_key': creation_details.get('include_answer_key', False),
                    'template_used': creation_details.get('template_id')
                }
            )
            
            self.logger.info(f"Export creation tracked for user: {user.username}")
            
        except Exception as e:
            self.logger.error(f"Error tracking export creation: {str(e)}")
    
    def get_export_statistics(self, user=None, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive export statistics"""
        try:
            from .models import ExportJob, ExportVersion
            
            # Base queryset
            base_query = ExportJob.objects.all()
            if user:
                base_query = base_query.filter(course__instructor=user)
            
            # Date range filter
            start_date = timezone.now() - timedelta(days=days)
            recent_exports = base_query.filter(created_at__gte=start_date)
            
            # Basic statistics
            stats = {
                'total_exports': base_query.count(),
                'recent_exports': recent_exports.count(),
                'completed_exports': base_query.filter(status='completed').count(),
                'failed_exports': base_query.filter(status='error').count(),
                'total_downloads': base_query.aggregate(
                    total=Sum('download_count')
                )['total'] or 0,
                'total_file_size': base_query.aggregate(
                    total=Sum('file_size')
                )['total'] or 0,
                'average_processing_time': base_query.filter(
                    processing_time_seconds__isnull=False
                ).aggregate(
                    avg=Avg('processing_time_seconds')
                )['avg'] or 0.0
            }
            
            # Format preferences
            format_stats = base_query.values('export_format').annotate(
                count=Count('id')
            ).order_by('-count')
            stats['format_preferences'] = {
                item['export_format']: item['count'] 
                for item in format_stats
            }
            
            # Content type breakdown
            content_stats = base_query.filter(
                generation__isnull=False
            ).values('generation__content_type').annotate(
                count=Count('id')
            ).order_by('-count')
            stats['content_types'] = {
                item['generation__content_type']: item['count']
                for item in content_stats
            }
            
            # Success rate
            total_attempts = base_query.count()
            if total_attempts > 0:
                stats['success_rate'] = (
                    stats['completed_exports'] / total_attempts
                ) * 100
            else:
                stats['success_rate'] = 0.0
            
            # Recent activity (last 7 days)
            last_week = timezone.now() - timedelta(days=7)
            recent_activity = []
            for i in range(7):
                day_start = last_week + timedelta(days=i)
                day_end = day_start + timedelta(days=1)
                day_count = base_query.filter(
                    created_at__gte=day_start,
                    created_at__lt=day_end
                ).count()
                recent_activity.append({
                    'date': day_start.date().isoformat(),
                    'exports': day_count
                })
            stats['recent_activity'] = recent_activity
            
            # Version statistics
            version_stats = ExportVersion.objects.filter(
                export_job__in=base_query
            ).values('version_letter').annotate(
                count=Count('id'),
                total_downloads=Sum('download_count')
            ).order_by('version_letter')
            stats['version_statistics'] = {
                item['version_letter']: {
                    'created': item['count'],
                    'downloads': item['total_downloads'] or 0
                }
                for item in version_stats
            }
            
            # Template usage
            template_stats = base_query.filter(
                template__isnull=False
            ).values('template__name').annotate(
                count=Count('id')
            ).order_by('-count')
            stats['template_usage'] = {
                item['template__name']: item['count']
                for item in template_stats
            }
            
            # Branding usage
            exports_with_branding = base_query.exclude(
                branding_settings={}
            ).count()
            stats['branding_usage_rate'] = (
                (exports_with_branding / total_attempts) * 100
                if total_attempts > 0 else 0.0
            )
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error generating export statistics: {str(e)}")
            return {}
    
    def get_user_export_analytics(self, user) -> Dict[str, Any]:
        """Get detailed analytics for a specific user"""
        try:
            from .models import ExportJob, ExportTemplate
            
            user_exports = ExportJob.objects.filter(course__instructor=user)
            
            analytics = {
                'user_id': user.id,
                'username': user.username,
                'total_exports': user_exports.count(),
                'successful_exports': user_exports.filter(status='completed').count(),
                'failed_exports': user_exports.filter(status='error').count(),
                'total_downloads': user_exports.aggregate(
                    total=Sum('download_count')
                )['total'] or 0,
                'favorite_format': None,
                'favorite_content_type': None,
                'average_processing_time': user_exports.filter(
                    processing_time_seconds__isnull=False
                ).aggregate(
                    avg=Avg('processing_time_seconds')
                )['avg'] or 0.0,
                'templates_created': ExportTemplate.objects.filter(
                    created_by=user
                ).count(),
                'most_recent_export': None,
                'export_frequency': 'low'  # low, medium, high
            }
            
            # Find favorite format
            format_counts = user_exports.values('export_format').annotate(
                count=Count('id')
            ).order_by('-count').first()
            if format_counts:
                analytics['favorite_format'] = format_counts['export_format']
            
            # Find favorite content type
            content_counts = user_exports.filter(
                generation__isnull=False
            ).values('generation__content_type').annotate(
                count=Count('id')
            ).order_by('-count').first()
            if content_counts:
                analytics['favorite_content_type'] = content_counts['generation__content_type']
            
            # Most recent export
            recent_export = user_exports.order_by('-created_at').first()
            if recent_export:
                analytics['most_recent_export'] = {
                    'title': recent_export.title,
                    'format': recent_export.export_format,
                    'created_at': recent_export.created_at.isoformat(),
                    'downloads': recent_export.download_count
                }
            
            # Calculate export frequency
            if user_exports.exists():
                first_export = user_exports.order_by('created_at').first()
                days_active = (timezone.now() - first_export.created_at).days
                if days_active > 0:
                    exports_per_day = user_exports.count() / days_active
                    if exports_per_day >= 1.0:
                        analytics['export_frequency'] = 'high'
                    elif exports_per_day >= 0.3:
                        analytics['export_frequency'] = 'medium'
                    else:
                        analytics['export_frequency'] = 'low'
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Error generating user analytics: {str(e)}")
            return {}
    
    def get_system_performance_metrics(self) -> Dict[str, Any]:
        """Get system-wide performance metrics"""
        try:
            from .models import ExportJob
            
            # Get all completed exports for performance analysis
            completed_exports = ExportJob.objects.filter(
                status='completed',
                processing_time_seconds__isnull=False
            )
            
            metrics = {
                'total_processed': completed_exports.count(),
                'average_processing_time': completed_exports.aggregate(
                    avg=Avg('processing_time_seconds')
                )['avg'] or 0.0,
                'fastest_export': completed_exports.aggregate(
                    min=Min('processing_time_seconds')
                )['min'] or 0.0,
                'slowest_export': completed_exports.aggregate(
                    max=Max('processing_time_seconds')  
                )['max'] or 0.0,
                'total_file_size_gb': (completed_exports.aggregate(
                    total=Sum('file_size')
                )['total'] or 0) / (1024 ** 3),
                'average_file_size_mb': (completed_exports.aggregate(
                    avg=Avg('file_size')
                )['avg'] or 0) / (1024 ** 2)
            }
            
            # Performance by format
            format_performance = {}
            for format_choice in ExportJob.FORMAT_CHOICES:
                format_code = format_choice[0]
                format_exports = completed_exports.filter(export_format=format_code)
                if format_exports.exists():
                    format_performance[format_code] = {
                        'count': format_exports.count(),
                        'avg_processing_time': format_exports.aggregate(
                            avg=Avg('processing_time_seconds')
                        )['avg'],
                        'avg_file_size_mb': (format_exports.aggregate(
                            avg=Avg('file_size')
                        )['avg'] or 0) / (1024 ** 2)
                    }
            
            metrics['performance_by_format'] = format_performance
            
            # Error analysis
            error_exports = ExportJob.objects.filter(status='error')
            metrics['error_rate'] = (
                error_exports.count() / ExportJob.objects.count() * 100
                if ExportJob.objects.exists() else 0.0
            )
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error generating performance metrics: {str(e)}")
            return {}
    
    def generate_export_report(self, user=None, format='json') -> Dict[str, Any]:
        """Generate comprehensive export report"""
        try:
            report = {
                'generated_at': timezone.now().isoformat(),
                'report_type': 'export_analytics',
                'user_specific': user is not None,
                'statistics': self.get_export_statistics(user=user),
                'performance_metrics': self.get_system_performance_metrics()
            }
            
            if user:
                report['user_analytics'] = self.get_user_export_analytics(user)
            
            # Add recommendations
            report['recommendations'] = self._generate_recommendations(report)
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating export report: {str(e)}")
            return {'error': str(e)}
    
    def _generate_recommendations(self, report_data: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on analytics"""
        recommendations = []
        
        try:
            stats = report_data.get('statistics', {})
            
            # Performance recommendations
            avg_processing_time = stats.get('average_processing_time', 0)
            if avg_processing_time > 30:  # More than 30 seconds
                recommendations.append(
                    "Consider optimizing export processing - average time is above 30 seconds"
                )
            
            # Success rate recommendations
            success_rate = stats.get('success_rate', 0)
            if success_rate < 95:
                recommendations.append(
                    f"Export success rate is {success_rate:.1f}% - investigate common failure causes"
                )
            
            # Format usage recommendations
            format_prefs = stats.get('format_preferences', {})
            if format_prefs:
                most_used = max(format_prefs.items(), key=lambda x: x[1])
                if most_used[0] == 'html' and most_used[1] > len(format_prefs) * 0.7:
                    recommendations.append(
                        "Consider promoting PDF exports for better professional presentation"
                    )
            
            # Branding usage
            branding_rate = stats.get('branding_usage_rate', 0)
            if branding_rate < 50:
                recommendations.append(
                    "Encourage users to configure university branding for professional documents"
                )
            
            # Template usage
            template_usage = stats.get('template_usage', {})
            if not template_usage:
                recommendations.append(
                    "No custom templates are being used - consider creating default templates"
                )
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            return ["Error generating recommendations"]


# Convenience functions for quick analytics access
def get_quick_stats(user=None):
    """Get quick export statistics"""
    analytics = ExportAnalytics()
    return analytics.get_export_statistics(user=user, days=30)


def track_download(export_job, user):
    """Quick function to track a download"""
    analytics = ExportAnalytics()
    return analytics.track_export_download(
        export_job=export_job,
        user=user,
        format_type=export_job.export_format,
        content_type=export_job.generation.content_type if export_job.generation else 'unknown'
    )
