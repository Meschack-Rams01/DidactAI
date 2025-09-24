import os
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from courses.models import Course


def upload_file_path(instance, filename):
    """Generate upload path for files"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    filename = f"{uuid.uuid4().hex}.{ext}"
    # Return path: uploads/user_id/course_id/filename
    return os.path.join(
        'uploads',
        str(instance.course.instructor.id),
        str(instance.course.id),
        filename
    )


class UploadedFile(models.Model):
    """Model for uploaded files"""
    
    FILE_TYPE_CHOICES = [
        ('pdf', _('PDF Document')),
        ('docx', _('Word Document')),
        ('pptx', _('PowerPoint Presentation')),
        ('txt', _('Text File')),
        ('image', _('Image File')),
        ('video', _('Video File')),
        ('audio', _('Audio File')),
        ('other', _('Other')),
    ]
    
    STATUS_CHOICES = [
        ('uploading', _('Uploading')),
        ('processing', _('Processing')),
        ('ready', _('Ready')),
        ('error', _('Error')),
    ]
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='uploaded_files'
    )
    original_filename = models.CharField(
        _('Original Filename'), 
        max_length=255
    )
    file = models.FileField(
        _('File'), 
        upload_to=upload_file_path
    )
    file_type = models.CharField(
        _('File Type'), 
        max_length=20, 
        choices=FILE_TYPE_CHOICES
    )
    file_size = models.BigIntegerField(
        _('File Size (bytes)')
    )
    mime_type = models.CharField(
        _('MIME Type'), 
        max_length=100, 
        blank=True, 
        null=True
    )
    description = models.TextField(
        _('Description'), 
        blank=True, 
        null=True
    )
    tags = models.JSONField(
        _('Tags'), 
        default=list,
        blank=True
    )
    status = models.CharField(
        _('Status'), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='uploading'
    )
    extracted_text = models.TextField(
        _('Extracted Text'), 
        blank=True, 
        null=True,
        help_text=_('Text extracted from the file using OCR or other methods')
    )
    detected_language = models.CharField(
        _('Detected Language'), 
        max_length=10, 
        blank=True, 
        null=True
    )
    metadata = models.JSONField(
        _('File Metadata'), 
        default=dict,
        blank=True,
        help_text=_('Additional metadata extracted from the file')
    )
    is_processed = models.BooleanField(
        _('Is Processed'), 
        default=False
    )
    processing_error = models.TextField(
        _('Processing Error'), 
        blank=True, 
        null=True
    )
    checksum = models.CharField(
        _('File Checksum'), 
        max_length=64, 
        blank=True, 
        null=True,
        help_text=_('SHA-256 checksum of the file')
    )
    download_count = models.PositiveIntegerField(
        _('Download Count'), 
        default=0
    )
    last_accessed = models.DateTimeField(
        _('Last Accessed'), 
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Uploaded File')
        verbose_name_plural = _('Uploaded Files')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.original_filename} - {self.course.title}"
    
    def get_file_extension(self):
        """Get the file extension"""
        return os.path.splitext(self.original_filename)[1].lower()
    
    @property
    def file_size_human(self):
        """Return human-readable file size"""
        for unit in ['bytes', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"
    
    def should_auto_delete(self):
        """Check if file should be auto-deleted based on course settings"""
        if not self.course.instructor.auto_delete_enabled:
            return False
        
        days_old = (timezone.now() - self.created_at).days
        return days_old >= self.course.instructor.auto_delete_days
    
    def increment_download_count(self):
        """Increment download count and update last accessed"""
        self.download_count += 1
        self.last_accessed = timezone.now()
        self.save(update_fields=['download_count', 'last_accessed'])


class FileVersion(models.Model):
    """Model for file versioning"""
    
    original_file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        related_name='versions'
    )
    version_number = models.PositiveIntegerField(
        _('Version Number')
    )
    file = models.FileField(
        _('File'), 
        upload_to=upload_file_path
    )
    file_size = models.BigIntegerField(
        _('File Size (bytes)')
    )
    change_notes = models.TextField(
        _('Change Notes'), 
        blank=True, 
        null=True
    )
    checksum = models.CharField(
        _('File Checksum'), 
        max_length=64, 
        blank=True, 
        null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='file_versions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('File Version')
        verbose_name_plural = _('File Versions')
        ordering = ['-version_number']
        unique_together = ['original_file', 'version_number']
        
    def __str__(self):
        return f"{self.original_file.original_filename} v{self.version_number}"


class ProcessingLog(models.Model):
    """Model for tracking file processing logs"""
    
    LOG_LEVEL_CHOICES = [
        ('info', _('Info')),
        ('warning', _('Warning')),
        ('error', _('Error')),
        ('success', _('Success')),
    ]
    
    file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        related_name='processing_logs'
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
        verbose_name = _('Processing Log')
        verbose_name_plural = _('Processing Logs')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.level.upper()}: {self.message[:50]}..."


class FileShare(models.Model):
    """Model for sharing files with other users"""
    
    PERMISSION_CHOICES = [
        ('view', _('View Only')),
        ('download', _('View & Download')),
        ('edit', _('View, Download & Edit')),
    ]
    
    file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        related_name='shares'
    )
    shared_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shared_files'
    )
    shared_with = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_files',
        blank=True,
        null=True
    )
    shared_with_email = models.EmailField(
        _('Shared with Email'), 
        blank=True, 
        null=True
    )
    permission = models.CharField(
        _('Permission'), 
        max_length=20, 
        choices=PERMISSION_CHOICES, 
        default='view'
    )
    share_token = models.UUIDField(
        default=uuid.uuid4, 
        unique=True, 
        editable=False
    )
    expires_at = models.DateTimeField(
        _('Expires At'), 
        blank=True, 
        null=True
    )
    is_active = models.BooleanField(
        _('Is Active'), 
        default=True
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
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('File Share')
        verbose_name_plural = _('File Shares')
        ordering = ['-created_at']
        
    def __str__(self):
        recipient = self.shared_with.email if self.shared_with else self.shared_with_email
        return f"{self.file.original_filename} shared with {recipient}"
    
    @property
    def is_expired(self):
        """Check if the share link is expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def increment_access_count(self):
        """Increment access count and update last accessed"""
        self.access_count += 1
        self.last_accessed = timezone.now()
        self.save(update_fields=['access_count', 'last_accessed'])
