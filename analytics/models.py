from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from courses.models import Course
from uploads.models import UploadedFile
from ai_generator.models import AIGeneration
from exports.models import ExportJob


class UserActivityLog(models.Model):
    """Model for tracking user activities"""
    
    ACTION_CHOICES = [
        ('login', _('Login')),
        ('logout', _('Logout')),
        ('course_created', _('Course Created')),
        ('course_updated', _('Course Updated')),
        ('file_uploaded', _('File Uploaded')),
        ('file_downloaded', _('File Downloaded')),
        ('ai_generation_started', _('AI Generation Started')),
        ('ai_generation_completed', _('AI Generation Completed')),
        ('export_created', _('Export Created')),
        ('export_downloaded', _('Export Downloaded')),
        ('settings_updated', _('Settings Updated')),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_logs'
    )
    action = models.CharField(
        _('Action'), 
        max_length=50, 
        choices=ACTION_CHOICES
    )
    description = models.CharField(
        _('Description'), 
        max_length=500, 
        blank=True, 
        null=True
    )
    ip_address = models.GenericIPAddressField(
        _('IP Address'), 
        blank=True, 
        null=True
    )
    user_agent = models.TextField(
        _('User Agent'), 
        blank=True, 
        null=True
    )
    metadata = models.JSONField(
        _('Metadata'), 
        default=dict,
        blank=True,
        help_text=_('Additional data about the activity')
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activity_logs'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('User Activity Log')
        verbose_name_plural = _('User Activity Logs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action', '-created_at']),
            models.Index(fields=['course', '-created_at']),
        ]
        
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_action_display()}"


class UsageStatistics(models.Model):
    """Model for aggregated usage statistics"""
    
    PERIOD_CHOICES = [
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
        ('yearly', _('Yearly')),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='usage_stats'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='usage_stats',
        blank=True,
        null=True
    )
    period_type = models.CharField(
        _('Period Type'), 
        max_length=20, 
        choices=PERIOD_CHOICES
    )
    date = models.DateField(_('Date'))
    
    # File Upload Statistics
    files_uploaded_count = models.PositiveIntegerField(
        _('Files Uploaded'), 
        default=0
    )
    total_upload_size = models.BigIntegerField(
        _('Total Upload Size (bytes)'), 
        default=0
    )
    files_processed_count = models.PositiveIntegerField(
        _('Files Processed'), 
        default=0
    )
    
    # AI Generation Statistics
    ai_generations_count = models.PositiveIntegerField(
        _('AI Generations'), 
        default=0
    )
    quiz_generations_count = models.PositiveIntegerField(
        _('Quiz Generations'), 
        default=0
    )
    exam_generations_count = models.PositiveIntegerField(
        _('Exam Generations'), 
        default=0
    )
    syllabus_generations_count = models.PositiveIntegerField(
        _('Syllabus Generations'), 
        default=0
    )
    total_tokens_used = models.PositiveIntegerField(
        _('Total Tokens Used'), 
        default=0
    )
    avg_generation_time = models.FloatField(
        _('Average Generation Time (seconds)'), 
        default=0.0
    )
    
    # Export Statistics
    exports_created_count = models.PositiveIntegerField(
        _('Exports Created'), 
        default=0
    )
    exports_downloaded_count = models.PositiveIntegerField(
        _('Exports Downloaded'), 
        default=0
    )
    pdf_exports_count = models.PositiveIntegerField(
        _('PDF Exports'), 
        default=0
    )
    docx_exports_count = models.PositiveIntegerField(
        _('DOCX Exports'), 
        default=0
    )
    zip_exports_count = models.PositiveIntegerField(
        _('ZIP Exports'), 
        default=0
    )
    
    # Session Statistics
    login_count = models.PositiveIntegerField(
        _('Login Count'), 
        default=0
    )
    total_session_time = models.PositiveIntegerField(
        _('Total Session Time (minutes)'), 
        default=0
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Usage Statistics')
        verbose_name_plural = _('Usage Statistics')
        ordering = ['-date']
        unique_together = ['user', 'course', 'period_type', 'date']
        indexes = [
            models.Index(fields=['user', 'period_type', '-date']),
            models.Index(fields=['course', 'period_type', '-date']),
        ]
        
    def __str__(self):
        course_name = self.course.title if self.course else 'All Courses'
        return f"{self.user.get_full_name()} - {course_name} - {self.date}"


class SystemMetrics(models.Model):
    """Model for system-wide metrics"""
    
    date = models.DateField(_('Date'), unique=True)
    
    # User Metrics
    total_users = models.PositiveIntegerField(
        _('Total Users'), 
        default=0
    )
    active_users = models.PositiveIntegerField(
        _('Active Users'), 
        default=0
    )
    new_users = models.PositiveIntegerField(
        _('New Users'), 
        default=0
    )
    
    # Course Metrics
    total_courses = models.PositiveIntegerField(
        _('Total Courses'), 
        default=0
    )
    active_courses = models.PositiveIntegerField(
        _('Active Courses'), 
        default=0
    )
    new_courses = models.PositiveIntegerField(
        _('New Courses'), 
        default=0
    )
    
    # File Metrics
    total_files = models.PositiveIntegerField(
        _('Total Files'), 
        default=0
    )
    total_file_size = models.BigIntegerField(
        _('Total File Size (bytes)'), 
        default=0
    )
    files_uploaded_today = models.PositiveIntegerField(
        _('Files Uploaded Today'), 
        default=0
    )
    
    # AI Generation Metrics
    total_generations = models.PositiveIntegerField(
        _('Total Generations'), 
        default=0
    )
    generations_today = models.PositiveIntegerField(
        _('Generations Today'), 
        default=0
    )
    total_tokens_used = models.BigIntegerField(
        _('Total Tokens Used'), 
        default=0
    )
    
    # Export Metrics
    total_exports = models.PositiveIntegerField(
        _('Total Exports'), 
        default=0
    )
    exports_today = models.PositiveIntegerField(
        _('Exports Today'), 
        default=0
    )
    total_downloads = models.PositiveIntegerField(
        _('Total Downloads'), 
        default=0
    )
    
    # Performance Metrics
    avg_response_time = models.FloatField(
        _('Average Response Time (ms)'), 
        default=0.0
    )
    error_rate = models.FloatField(
        _('Error Rate (%)'), 
        default=0.0
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('System Metrics')
        verbose_name_plural = _('System Metrics')
        ordering = ['-date']
        
    def __str__(self):
        return f"System Metrics - {self.date}"


class APIUsageLog(models.Model):
    """Model for tracking API usage (AI model calls)"""
    
    SERVICE_CHOICES = [
        ('gemini', _('Google Gemini')),
        ('huggingface', _('Hugging Face')),
        ('tesseract', _('Tesseract OCR')),
        ('langdetect', _('Language Detection')),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='api_usage_logs'
    )
    service = models.CharField(
        _('Service'), 
        max_length=50, 
        choices=SERVICE_CHOICES
    )
    endpoint = models.CharField(
        _('API Endpoint'), 
        max_length=200
    )
    method = models.CharField(
        _('HTTP Method'), 
        max_length=10, 
        default='POST'
    )
    request_size = models.PositiveIntegerField(
        _('Request Size (bytes)'), 
        default=0
    )
    response_size = models.PositiveIntegerField(
        _('Response Size (bytes)'), 
        default=0
    )
    tokens_consumed = models.PositiveIntegerField(
        _('Tokens Consumed'), 
        default=0
    )
    response_time_ms = models.PositiveIntegerField(
        _('Response Time (ms)'), 
        default=0
    )
    status_code = models.PositiveIntegerField(
        _('HTTP Status Code'), 
        default=200
    )
    success = models.BooleanField(
        _('Success'), 
        default=True
    )
    error_message = models.TextField(
        _('Error Message'), 
        blank=True, 
        null=True
    )
    cost_estimate = models.DecimalField(
        _('Cost Estimate'), 
        max_digits=10, 
        decimal_places=6, 
        default=0.0,
        help_text=_('Estimated cost in USD')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('API Usage Log')
        verbose_name_plural = _('API Usage Logs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['service', '-created_at']),
            models.Index(fields=['success', '-created_at']),
        ]
        
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.service} - {self.created_at}"


class ContentAnalytics(models.Model):
    """Model for tracking content usage and analytics"""
    
    CONTENT_TYPE_CHOICES = [
        ('quiz', _('Quiz')),
        ('exam', _('Exam')),
        ('syllabus', _('Syllabus')),
        ('lesson', _('Lesson')),
        ('assignment', _('Assignment')),
        ('other', _('Other')),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='content_analytics'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='content_analytics',
        blank=True,
        null=True
    )
    content_type = models.CharField(
        _('Content Type'), 
        max_length=50, 
        choices=CONTENT_TYPE_CHOICES
    )
    content_title = models.CharField(
        _('Content Title'), 
        max_length=200
    )
    content_id = models.PositiveIntegerField(
        _('Content ID'),
        help_text=_('ID of the related content object')
    )
    
    # Analytics data
    view_count = models.PositiveIntegerField(
        _('View Count'), 
        default=0
    )
    download_count = models.PositiveIntegerField(
        _('Download Count'), 
        default=0
    )
    share_count = models.PositiveIntegerField(
        _('Share Count'), 
        default=0
    )
    edit_count = models.PositiveIntegerField(
        _('Edit Count'), 
        default=0
    )
    
    # Engagement metrics
    total_time_spent = models.PositiveIntegerField(
        _('Total Time Spent (seconds)'), 
        default=0
    )
    average_session_time = models.FloatField(
        _('Average Session Time (seconds)'), 
        default=0.0
    )
    bounce_rate = models.FloatField(
        _('Bounce Rate (%)'), 
        default=0.0,
        help_text=_('Percentage of users who left without interaction')
    )
    
    # Performance metrics
    load_time_avg = models.FloatField(
        _('Average Load Time (seconds)'), 
        default=0.0
    )
    error_count = models.PositiveIntegerField(
        _('Error Count'), 
        default=0
    )
    
    # Metadata
    language = models.CharField(
        _('Language'), 
        max_length=10, 
        default='en'
    )
    difficulty_level = models.CharField(
        _('Difficulty Level'), 
        max_length=20, 
        blank=True, 
        null=True
    )
    tags = models.JSONField(
        _('Tags'), 
        default=list,
        blank=True
    )
    
    # Tracking dates
    first_accessed = models.DateTimeField(
        _('First Accessed'), 
        auto_now_add=True
    )
    last_accessed = models.DateTimeField(
        _('Last Accessed'), 
        auto_now=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Content Analytics')
        verbose_name_plural = _('Content Analytics')
        ordering = ['-last_accessed']
        unique_together = ['user', 'content_type', 'content_id']
        indexes = [
            models.Index(fields=['user', 'content_type', '-last_accessed']),
            models.Index(fields=['course', '-last_accessed']),
            models.Index(fields=['content_type', '-view_count']),
        ]
        
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.content_title}"
    
    def increment_view_count(self):
        """Increment view count and update last accessed"""
        self.view_count += 1
        self.last_accessed = timezone.now()
        self.save(update_fields=['view_count', 'last_accessed'])
    
    def increment_download_count(self):
        """Increment download count"""
        self.download_count += 1
        self.save(update_fields=['download_count'])
    
    def increment_share_count(self):
        """Increment share count"""
        self.share_count += 1
        self.save(update_fields=['share_count'])
    
    def increment_edit_count(self):
        """Increment edit count"""
        self.edit_count += 1
        self.save(update_fields=['edit_count'])
    
    def update_engagement_metrics(self, session_time: float):
        """Update engagement metrics with new session data"""
        # Update total time spent
        self.total_time_spent += int(session_time)
        
        # Recalculate average session time
        if self.view_count > 0:
            self.average_session_time = self.total_time_spent / self.view_count
        
        self.save(update_fields=['total_time_spent', 'average_session_time'])
    
    def update_performance_metrics(self, load_time: float, had_error: bool = False):
        """Update performance metrics"""
        # Update load time average
        if self.view_count > 0:
            total_load_time = self.load_time_avg * (self.view_count - 1) + load_time
            self.load_time_avg = total_load_time / self.view_count
        else:
            self.load_time_avg = load_time
        
        # Update error count
        if had_error:
            self.error_count += 1
        
        self.save(update_fields=['load_time_avg', 'error_count'])


class ErrorLog(models.Model):
    """Model for tracking application errors"""
    
    SEVERITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('critical', _('Critical')),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='error_logs'
    )
    error_type = models.CharField(
        _('Error Type'), 
        max_length=200
    )
    error_message = models.TextField(_('Error Message'))
    stack_trace = models.TextField(
        _('Stack Trace'), 
        blank=True, 
        null=True
    )
    severity = models.CharField(
        _('Severity'), 
        max_length=20, 
        choices=SEVERITY_CHOICES, 
        default='medium'
    )
    url = models.URLField(
        _('URL'), 
        blank=True, 
        null=True
    )
    http_method = models.CharField(
        _('HTTP Method'), 
        max_length=10, 
        blank=True, 
        null=True
    )
    ip_address = models.GenericIPAddressField(
        _('IP Address'), 
        blank=True, 
        null=True
    )
    user_agent = models.TextField(
        _('User Agent'), 
        blank=True, 
        null=True
    )
    additional_data = models.JSONField(
        _('Additional Data'), 
        default=dict,
        blank=True
    )
    is_resolved = models.BooleanField(
        _('Resolved'), 
        default=False
    )
    resolution_notes = models.TextField(
        _('Resolution Notes'), 
        blank=True, 
        null=True
    )
    occurrence_count = models.PositiveIntegerField(
        _('Occurrence Count'), 
        default=1
    )
    first_occurred = models.DateTimeField(auto_now_add=True)
    last_occurred = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Error Log')
        verbose_name_plural = _('Error Logs')
        ordering = ['-last_occurred']
        indexes = [
            models.Index(fields=['severity', '-last_occurred']),
            models.Index(fields=['is_resolved', '-last_occurred']),
            models.Index(fields=['error_type', '-last_occurred']),
        ]
        
    def __str__(self):
        return f"{self.error_type} - {self.get_severity_display()}"
    
    def increment_occurrence(self):
        """Increment occurrence count and update last occurred time"""
        self.occurrence_count += 1
        self.last_occurred = timezone.now()
        self.save(update_fields=['occurrence_count', 'last_occurred'])
