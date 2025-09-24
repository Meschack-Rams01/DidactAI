from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Custom user model with additional fields for DidactIA"""
    
    ROLE_CHOICES = [
        ('instructor', _('Instructor')),
        ('admin', _('Administrator')),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', _('English')),
        ('fr', _('French')),
        ('es', _('Spanish')),
        ('de', _('German')),
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
