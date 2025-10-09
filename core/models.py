from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
import json


class ContentTranslation(models.Model):
    """
    Model to store translations for any content object
    """
    content_type = models.CharField(max_length=50)  # Model name
    object_id = models.PositiveIntegerField()  # Object ID
    language = models.CharField(max_length=10)  # Language code (e.g., 'fr', 'es')
    translations = models.JSONField(default=dict)  # Field translations
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['content_type', 'object_id', 'language']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['language']),
        ]
    
    def __str__(self):
        return f"{self.content_type} #{self.object_id} - {self.language}"


class GlobalSettings(models.Model):
    """Model for global application settings"""
    
    # AI Settings
    default_ai_model = models.CharField(
        _('Default AI Model'), 
        max_length=50, 
        default='gemini-2.5-flash'
    )
    max_tokens_per_request = models.PositiveIntegerField(
        _('Max Tokens per Request'), 
        default=4000
    )
    ai_timeout_seconds = models.PositiveIntegerField(
        _('AI Timeout (seconds)'), 
        default=120
    )
    
    # File Upload Settings
    max_file_size_mb = models.PositiveIntegerField(
        _('Max File Size (MB)'), 
        default=50
    )
    allowed_file_extensions = models.JSONField(
        _('Allowed File Extensions'), 
        default=list,
        help_text=_('List of allowed file extensions')
    )
    
    # Export Settings
    export_retention_days = models.PositiveIntegerField(
        _('Export Retention Days'), 
        default=30,
        help_text=_('Number of days to keep exported files')
    )
    watermark_text = models.CharField(
        _('Default Watermark'), 
        max_length=200, 
        blank=True, 
        null=True
    )
    
    # System Limits
    max_generations_per_day = models.PositiveIntegerField(
        _('Max Generations per Day'), 
        default=100
    )
    max_exports_per_day = models.PositiveIntegerField(
        _('Max Exports per Day'), 
        default=50
    )
    
    # Maintenance
    maintenance_mode = models.BooleanField(
        _('Maintenance Mode'), 
        default=False
    )
    maintenance_message = models.TextField(
        _('Maintenance Message'), 
        blank=True, 
        null=True
    )
    
    # Feature Flags
    enable_ai_generation = models.BooleanField(
        _('Enable AI Generation'), 
        default=True
    )
    enable_file_sharing = models.BooleanField(
        _('Enable File Sharing'), 
        default=True
    )
    enable_analytics = models.BooleanField(
        _('Enable Analytics'), 
        default=True
    )
    enable_export_versioning = models.BooleanField(
        _('Enable Export Versioning'), 
        default=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Global Settings')
        verbose_name_plural = _('Global Settings')
        
    def __str__(self):
        return "Global Application Settings"
    
    @classmethod
    def get_settings(cls):
        """Get or create global settings instance"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class Notification(models.Model):
    """Model for user notifications"""
    
    TYPE_CHOICES = [
        ('info', _('Information')),
        ('success', _('Success')),
        ('warning', _('Warning')),
        ('error', _('Error')),
        ('system', _('System')),
    ]
    
    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('normal', _('Normal')),
        ('high', _('High')),
        ('urgent', _('Urgent')),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(_('Title'), max_length=200)
    message = models.TextField(_('Message'))
    notification_type = models.CharField(
        _('Type'), 
        max_length=20, 
        choices=TYPE_CHOICES, 
        default='info'
    )
    priority = models.CharField(
        _('Priority'), 
        max_length=20, 
        choices=PRIORITY_CHOICES, 
        default='normal'
    )
    is_read = models.BooleanField(_('Read'), default=False)
    is_dismissed = models.BooleanField(_('Dismissed'), default=False)
    action_url = models.URLField(
        _('Action URL'), 
        blank=True, 
        null=True,
        help_text=_('URL to redirect when notification is clicked')
    )
    action_label = models.CharField(
        _('Action Label'), 
        max_length=50, 
        blank=True, 
        null=True
    )
    metadata = models.JSONField(
        _('Metadata'), 
        default=dict,
        blank=True
    )
    expires_at = models.DateTimeField(
        _('Expires At'), 
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(
        _('Read At'), 
        blank=True, 
        null=True
    )
    
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['is_read', '-created_at']),
        ]
        
    def __str__(self):
        return f"{self.title} - {self.recipient.get_full_name()}"
    
    def mark_read(self):
        """Mark notification as read"""
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=['is_read', 'read_at'])


class SystemAnnouncement(models.Model):
    """Model for system-wide announcements"""
    
    ANNOUNCEMENT_TYPE_CHOICES = [
        ('maintenance', _('Maintenance')),
        ('feature', _('New Feature')),
        ('update', _('System Update')),
        ('warning', _('Warning')),
        ('info', _('Information')),
    ]
    
    title = models.CharField(_('Title'), max_length=200)
    content = models.TextField(_('Content'))
    announcement_type = models.CharField(
        _('Type'), 
        max_length=20, 
        choices=ANNOUNCEMENT_TYPE_CHOICES, 
        default='info'
    )
    is_active = models.BooleanField(_('Active'), default=True)
    is_dismissible = models.BooleanField(_('Dismissible'), default=True)
    target_roles = models.JSONField(
        _('Target Roles'), 
        default=list,
        blank=True,
        help_text=_('Roles that should see this announcement. Empty for all users.')
    )
    display_from = models.DateTimeField(_('Display From'))
    display_until = models.DateTimeField(
        _('Display Until'), 
        blank=True, 
        null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='announcements'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('System Announcement')
        verbose_name_plural = _('System Announcements')
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    @property
    def is_current(self):
        """Check if announcement is currently active and within display period"""
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_active:
            return False
        
        if self.display_from > now:
            return False
        
        if self.display_until and self.display_until < now:
            return False
        
        return True


class UserPreference(models.Model):
    """Model for user-specific preferences and settings"""
    
    THEME_CHOICES = [
        ('light', _('Light')),
        ('dark', _('Dark')),
        ('auto', _('Auto')),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='preferences'
    )
    
    # UI Preferences
    theme = models.CharField(
        _('Theme'), 
        max_length=10, 
        choices=THEME_CHOICES, 
        default='light'
    )
    sidebar_collapsed = models.BooleanField(
        _('Sidebar Collapsed'), 
        default=False
    )
    items_per_page = models.PositiveIntegerField(
        _('Items per Page'), 
        default=20,
        validators=[MinValueValidator(5), MaxValueValidator(100)]
    )
    
    # Notification Preferences
    email_notifications = models.BooleanField(
        _('Email Notifications'), 
        default=True
    )
    notification_frequency = models.CharField(
        _('Notification Frequency'),
        max_length=20,
        choices=[
            ('immediate', _('Immediate')),
            ('daily', _('Daily Digest')),
            ('weekly', _('Weekly Digest')),
            ('never', _('Never')),
        ],
        default='immediate'
    )
    
    # Generation Preferences
    default_quiz_questions = models.PositiveIntegerField(
        _('Default Quiz Questions'), 
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    default_exam_versions = models.PositiveIntegerField(
        _('Default Exam Versions'), 
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    preferred_export_format = models.CharField(
        _('Preferred Export Format'),
        max_length=10,
        choices=[
            ('pdf', _('PDF')),
            ('docx', _('Word')),
            ('html', _('HTML')),
        ],
        default='pdf'
    )
    
    # Privacy Preferences
    allow_analytics = models.BooleanField(
        _('Allow Analytics'), 
        default=True
    )
    allow_usage_tracking = models.BooleanField(
        _('Allow Usage Tracking'), 
        default=True
    )
    
    # Custom Settings
    custom_settings = models.JSONField(
        _('Custom Settings'), 
        default=dict,
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User Preference')
        verbose_name_plural = _('User Preferences')
        
    def __str__(self):
        return f"Preferences for {self.user.get_full_name()}"


class Tag(models.Model):
    """Model for tagging system"""
    
    name = models.CharField(_('Name'), max_length=100, unique=True)
    slug = models.SlugField(_('Slug'), unique=True)
    color = models.CharField(
        _('Color'), 
        max_length=7, 
        default='#6B7280',
        help_text=_('Hex color code for the tag')
    )
    description = models.TextField(
        _('Description'), 
        blank=True, 
        null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tags'
    )
    is_system_tag = models.BooleanField(
        _('System Tag'), 
        default=False,
        help_text=_('System tags are available to all users')
    )
    usage_count = models.PositiveIntegerField(
        _('Usage Count'), 
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def increment_usage(self):
        """Increment usage count"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])


class AuditLog(models.Model):
    """Model for audit logging important actions"""
    
    ACTION_CHOICES = [
        ('create', _('Create')),
        ('update', _('Update')),
        ('delete', _('Delete')),
        ('login', _('Login')),
        ('logout', _('Logout')),
        ('export', _('Export')),
        ('share', _('Share')),
        ('download', _('Download')),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(
        _('Action'), 
        max_length=20, 
        choices=ACTION_CHOICES
    )
    model_name = models.CharField(
        _('Model Name'), 
        max_length=100
    )
    object_id = models.PositiveIntegerField(
        _('Object ID'), 
        blank=True, 
        null=True
    )
    object_repr = models.CharField(
        _('Object Representation'), 
        max_length=200, 
        blank=True, 
        null=True
    )
    changes = models.JSONField(
        _('Changes'), 
        default=dict,
        blank=True,
        help_text=_('Record of what was changed')
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
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Audit Log')
        verbose_name_plural = _('Audit Logs')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['model_name', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]
        
    def __str__(self):
        user_name = self.user.get_full_name() if self.user else 'System'
        return f"{user_name} - {self.get_action_display()} {self.model_name}"
