from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Custom user model with additional fields for DidactAI"""
    
    ROLE_CHOICES = [
        ('instructor', _('Instructor')),
        ('admin', _('Administrator')),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', _('English')),
        ('fr', _('French')),
        ('es', _('Spanish')),
        ('de', _('German')),
        ('it', _('Italian')),
        ('pt', _('Portuguese')),
        ('ru', _('Russian')),
        ('ar', _('Arabic')),
        ('zh', _('Chinese')),
        ('ja', _('Japanese')),
        ('ko', _('Korean')),
        ('tr', _('Turkish')),
    ]
    
    email = models.EmailField(_('Email address'), unique=True)
    role = models.CharField(
        _('Role'), 
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='instructor'
    )
    institution = models.CharField(
        _('Institution'), 
        max_length=200, 
        blank=True, 
        null=True
    )
    department = models.CharField(
        _('Department'), 
        max_length=100, 
        blank=True, 
        null=True
    )
    preferred_language = models.CharField(
        _('Preferred Language'), 
        max_length=10, 
        choices=LANGUAGE_CHOICES, 
        default='en'
    )
    phone_number = models.CharField(
        _('Phone Number'), 
        max_length=20, 
        blank=True, 
        null=True
    )
    bio = models.TextField(
        _('Biography'), 
        blank=True, 
        null=True
    )
    avatar = models.ImageField(
        _('Avatar'), 
        upload_to='avatars/', 
        blank=True, 
        null=True
    )
    is_email_verified = models.BooleanField(
        _('Email Verified'), 
        default=False
    )
    auto_delete_enabled = models.BooleanField(
        _('Auto Delete Files'), 
        default=True,
        help_text=_('Automatically delete old files after configured days')
    )
    auto_delete_days = models.IntegerField(
        _('Auto Delete Days'), 
        default=90,
        help_text=_('Number of days after which files are automatically deleted')
    )
    # Privacy settings
    profile_public = models.BooleanField(
        _('Public Profile'),
        default=False,
        help_text=_('Make profile visible to other users')
    )
    show_email = models.BooleanField(
        _('Show Email'),
        default=False,
        help_text=_('Display email address on public profile')
    )
    email_notifications = models.BooleanField(
        _('Email Notifications'),
        default=True,
        help_text=_('Receive email notifications')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_short_name(self):
        """Return the user's first name."""
        return self.first_name or self.username
    
    @property
    def is_instructor(self):
        return self.role == 'instructor'
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    def get_profile_initials(self):
        """Get user initials for avatar"""
        if self.first_name and self.last_name:
            return f"{self.first_name[0].upper()}{self.last_name[0].upper()}"
        return self.username[:2].upper()
    
    def get_quick_stats(self):
        """Get user's quick statistics"""
        from courses.models import Course
        from uploads.models import UploadedFile
        from ai_generator.models import AIGeneration
        from exports.models import ExportJob
        
        return {
            'courses': Course.objects.filter(instructor=self).count(),
            'files_uploaded': UploadedFile.objects.filter(course__instructor=self).count(),
            'ai_generations': AIGeneration.objects.filter(course__instructor=self).count(),
            'exports': ExportJob.objects.filter(course__instructor=self).count(),
        }


class UserProfile(models.Model):
    """Extended user profile information"""
    
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    timezone = models.CharField(
        _('Timezone'), 
        max_length=50, 
        default='UTC'
    )
    notification_preferences = models.JSONField(
        _('Notification Preferences'), 
        default=dict,
        blank=True
    )
    ui_preferences = models.JSONField(
        _('UI Preferences'), 
        default=dict,
        blank=True,
        help_text=_('User interface preferences like theme, sidebar state, etc.')
    )
    api_usage_stats = models.JSONField(
        _('API Usage Statistics'), 
        default=dict,
        blank=True
    )
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
        
    def __str__(self):
        return f"Profile for {self.user.get_full_name()}"


class UserActivity(models.Model):
    """Track user activities"""
    
    ACTIVITY_CHOICES = [
        ('account_created', _('Account Created')),
        ('login', _('Login')),
        ('logout', _('Logout')),
        ('profile_updated', _('Profile Updated')),
        ('password_changed', _('Password Changed')),
        ('course_created', _('Course Created')),
        ('course_updated', _('Course Updated')),
        ('file_uploaded', _('File Uploaded')),
        ('content_generated', _('Content Generated')),
        ('export_created', _('Export Created')),
        ('settings_updated', _('Settings Updated')),
    ]
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    activity_type = models.CharField(
        _('Activity Type'),
        max_length=30,
        choices=ACTIVITY_CHOICES
    )
    description = models.CharField(
        _('Description'),
        max_length=255
    )
    details = models.JSONField(
        _('Activity Details'),
        default=dict,
        blank=True
    )
    ip_address = models.GenericIPAddressField(
        _('IP Address'),
        blank=True,
        null=True
    )
    timestamp = models.DateTimeField(
        _('Timestamp'),
        default=timezone.now
    )
    
    class Meta:
        verbose_name = _('User Activity')
        verbose_name_plural = _('User Activities')
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"
    
    def time_since(self):
        """Get human-readable time since activity"""
        now = timezone.now()
        diff = now - self.timestamp
        
        if diff.days > 0:
            if diff.days == 1:
                return _('1 day ago')
            elif diff.days < 30:
                return _(f'{diff.days} days ago')
            elif diff.days < 365:
                months = diff.days // 30
                if months == 1:
                    return _('1 month ago')
                return _(f'{months} months ago')
            else:
                years = diff.days // 365
                if years == 1:
                    return _('1 year ago')
                return _(f'{years} years ago')
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            if hours == 1:
                return _('1 hour ago')
            return _(f'{hours} hours ago')
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            if minutes == 1:
                return _('1 minute ago')
            return _(f'{minutes} minutes ago')
        else:
            return _('Just now')


# Activity logging utility functions
def log_user_activity(user, activity_type, description, details=None, request=None):
    """Log user activity"""
    activity_data = {
        'user': user,
        'activity_type': activity_type,
        'description': description,
        'details': details or {},
    }
    
    if request:
        activity_data.update({
            'ip_address': get_client_ip(request),
        })
    
    return UserActivity.objects.create(**activity_data)


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


# Signal handlers for automatic activity logging
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def create_user_activity_on_signup(sender, instance, created, **kwargs):
    """Log account creation activity"""
    if created:
        log_user_activity(
            user=instance,
            activity_type='account_created',
            description=f'Account created for {instance.get_full_name()}'
        )

