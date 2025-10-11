import os
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from courses.models import Course
from ai_generator.models import AIGeneration


def export_file_path(instance, filename):
    """Generate export path for files"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(
        'exports',
        str(instance.course.instructor.id),
        str(instance.course.id),
        filename
    )


def export_version_file_path(instance, filename):
    """Generate export path for version files"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(
        'exports',
        str(instance.export_job.course.instructor.id),
        str(instance.export_job.course.id),
        'versions',
        filename
    )


class ExportTemplate(models.Model):
    """Templates for document exports"""
    
    TEMPLATE_TYPE_CHOICES = [
        ('pdf', _('PDF Template')),
        ('docx', _('Word Template')),
        ('html', _('HTML Template')),
        ('latex', _('LaTeX Template')),
    ]
    
    CONTENT_TYPE_CHOICES = [
        ('quiz', _('Quiz')),
        ('exam', _('Exam')),
        ('syllabus', _('Syllabus')),
        ('flashcards', _('Flashcards')),
        ('report', _('Report')),
        ('certificate', _('Certificate')),
    ]
    
    name = models.CharField(_('Template Name'), max_length=200)
    template_type = models.CharField(
        _('Template Type'), 
        max_length=20, 
        choices=TEMPLATE_TYPE_CHOICES
    )
    content_type = models.CharField(
        _('Content Type'), 
        max_length=20, 
        choices=CONTENT_TYPE_CHOICES
    )
    description = models.TextField(
        _('Description'), 
        blank=True, 
        null=True
    )
    template_file = models.FileField(
        _('Template File'), 
        upload_to='export_templates/',
        blank=True,
        null=True
    )
    template_content = models.TextField(
        _('Template Content'),
        blank=True,
        null=True,
        help_text=_('Template content for HTML/text-based templates')
    )
    css_styles = models.TextField(
        _('CSS Styles'), 
        blank=True, 
        null=True
    )
    variables = models.JSONField(
        _('Template Variables'), 
        default=dict,
        blank=True,
        help_text=_('Available variables and their descriptions')
    )
    is_system_template = models.BooleanField(
        _('System Template'), 
        default=False
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='export_templates'
    )
    is_active = models.BooleanField(_('Active'), default=True)
    usage_count = models.PositiveIntegerField(
        _('Usage Count'), 
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Export Template')
        verbose_name_plural = _('Export Templates')
        ordering = ['-usage_count', '-updated_at']
        
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    def increment_usage(self):
        """Increment usage count"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])


class ExportJob(models.Model):
    """Model for export jobs"""
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('error', _('Error')),
        ('cancelled', _('Cancelled')),
    ]
    
    FORMAT_CHOICES = [
        ('pdf', _('PDF')),
        ('docx', _('Word Document')),
        ('html', _('HTML')),
    ]
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='export_jobs'
    )
    generation = models.ForeignKey(
        AIGeneration,
        on_delete=models.CASCADE,
        related_name='export_jobs',
        blank=True,
        null=True
    )
    template = models.ForeignKey(
        ExportTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='export_jobs'
    )
    title = models.CharField(_('Export Title'), max_length=200)
    description = models.TextField(
        _('Description'), 
        blank=True, 
        null=True
    )
    export_format = models.CharField(
        _('Export Format'), 
        max_length=20, 
        choices=FORMAT_CHOICES
    )
    status = models.CharField(
        _('Status'), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    parameters = models.JSONField(
        _('Export Parameters'), 
        default=dict,
        blank=True,
        help_text=_('Export configuration and options')
    )
    branding_settings = models.JSONField(
        _('Branding Settings'), 
        default=dict,
        blank=True,
        help_text=_('Custom branding (logo, colors, university info)')
    )
    include_answer_key = models.BooleanField(
        _('Include Answer Key'), 
        default=True
    )
    include_instructions = models.BooleanField(
        _('Include Instructions'), 
        default=True
    )
    watermark = models.CharField(
        _('Watermark'), 
        max_length=200, 
        blank=True, 
        null=True
    )
    university_logo = models.ImageField(
        _('University Logo'), 
        upload_to='export_logos/',
        blank=True, 
        null=True,
        help_text=_('Upload university logo for branding in exports')
    )
    generated_file = models.FileField(
        _('Generated File'), 
        upload_to=export_file_path,
        blank=True,
        null=True
    )
    file_size = models.BigIntegerField(
        _('File Size (bytes)'), 
        default=0
    )
    download_count = models.PositiveIntegerField(
        _('Download Count'), 
        default=0
    )
    processing_time_seconds = models.FloatField(
        _('Processing Time (seconds)'), 
        blank=True, 
        null=True
    )
    error_message = models.TextField(
        _('Error Message'), 
        blank=True, 
        null=True
    )
    expires_at = models.DateTimeField(
        _('Expires At'), 
        blank=True, 
        null=True,
        help_text=_('When this export file should be automatically deleted')
    )
    last_downloaded = models.DateTimeField(
        _('Last Downloaded'), 
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(
        _('Completed At'), 
        blank=True, 
        null=True
    )
    
    class Meta:
        verbose_name = _('Export Job')
        verbose_name_plural = _('Export Jobs')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} ({self.get_export_format_display()})"
    
    def mark_completed(self):
        """Mark export as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])
    
    def mark_error(self, error_message):
        """Mark export as error with message"""
        self.status = 'error'
        self.error_message = error_message
        self.save(update_fields=['status', 'error_message'])
    
    def increment_download_count(self):
        """Increment download count and update analytics"""
        self.download_count += 1
        self.last_downloaded = timezone.now()
        self.save(update_fields=['download_count', 'last_downloaded'])
        
        # Update analytics automatically
        self._update_analytics()
    
    def _update_analytics(self):
        """Update export analytics automatically"""
        try:
            from .analytics import ExportAnalytics
            analytics = ExportAnalytics()
            analytics.track_export_download(
                export_job=self,
                user=self.course.instructor,
                format_type=self.export_format,
                content_type=self.generation.content_type if self.generation else 'unknown'
            )
        except ImportError:
            # Analytics module not available, skip
            pass
        except Exception as e:
            # Log error but don't break the download
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error updating export analytics: {str(e)}")
    
    @property
    def file_size_human(self):
        """Return human-readable file size"""
        if self.file_size == 0:
            return "0 bytes"
        
        for unit in ['bytes', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"
    
    @property
    def is_expired(self):
        """Check if export is expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class ExportVersion(models.Model):
    """Model for versioned exports (A, B, C versions)"""
    
    export_job = models.ForeignKey(
        ExportJob,
        on_delete=models.CASCADE,
        related_name='versions'
    )
    version_letter = models.CharField(
        _('Version Letter'), 
        max_length=1, 
        default='A'
    )
    generated_file = models.FileField(
        _('Generated File'), 
        upload_to=export_version_file_path
    )
    file_size = models.BigIntegerField(
        _('File Size (bytes)'), 
        default=0
    )
    variations = models.JSONField(
        _('Version Variations'), 
        default=dict,
        blank=True,
        help_text=_('Specific variations applied to this version')
    )
    download_count = models.PositiveIntegerField(
        _('Download Count'), 
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Export Version')
        verbose_name_plural = _('Export Versions')
        ordering = ['version_letter']
        unique_together = ['export_job', 'version_letter']
        
    def __str__(self):
        return f"{self.export_job.title} - Version {self.version_letter}"
    
    def increment_download_count(self):
        """Increment download count"""
        self.download_count += 1
        self.save(update_fields=['download_count'])


class ExportLog(models.Model):
    """Model for export processing logs"""
    
    LOG_LEVEL_CHOICES = [
        ('info', _('Info')),
        ('warning', _('Warning')),
        ('error', _('Error')),
        ('success', _('Success')),
    ]
    
    export_job = models.ForeignKey(
        ExportJob,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    level = models.CharField(
        _('Log Level'), 
        max_length=10, 
        choices=LOG_LEVEL_CHOICES
    )
    message = models.TextField(_('Message'))
    details = models.JSONField(
        _('Details'), 
        default=dict,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Export Log')
        verbose_name_plural = _('Export Logs')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.level.upper()}: {self.message[:50]}..."


class ExportShare(models.Model):
    """Model for sharing exported documents"""
    
    export_job = models.ForeignKey(
        ExportJob,
        on_delete=models.CASCADE,
        related_name='shares'
    )
    share_token = models.UUIDField(
        default=uuid.uuid4, 
        unique=True, 
        editable=False
    )
    shared_with_email = models.EmailField(
        _('Shared with Email'), 
        blank=True, 
        null=True
    )
    can_download = models.BooleanField(
        _('Can Download'), 
        default=True
    )
    expires_at = models.DateTimeField(
        _('Expires At'), 
        blank=True, 
        null=True
    )
    access_count = models.PositiveIntegerField(
        _('Access Count'), 
        default=0
    )
    last_accessed = models.DateTimeField(
        _('Last Accessed'), 
        blank=True, 
        null=True
    )
    is_active = models.BooleanField(
        _('Active'), 
        default=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Export Share')
        verbose_name_plural = _('Export Shares')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.export_job.title} shared via {self.share_token}"
    
    @property
    def is_expired(self):
        """Check if the share link is expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def increment_access_count(self):
        """Increment access count"""
        self.access_count += 1
        self.last_accessed = timezone.now()
        self.save(update_fields=['access_count', 'last_accessed'])
