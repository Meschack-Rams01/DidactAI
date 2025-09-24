from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Course(models.Model):
    """Model representing a course"""
    
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('archived', _('Archived')),
        ('draft', _('Draft')),
    ]
    
    SEMESTER_CHOICES = [
        ('fall', _('Fall')),
        ('spring', _('Spring')),
        ('summer', _('Summer')),
        ('winter', _('Winter')),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', _('English')),
        ('fr', _('French')),
        ('es', _('Spanish')),
        ('de', _('German')),
    ]
    
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    title = models.CharField(_('Course Title'), max_length=200)
    slug = models.SlugField(
        _('Slug'), 
        max_length=250, 
        unique=True, 
        blank=True
    )
    description = models.TextField(
        _('Description'), 
        blank=True, 
        null=True
    )
    course_code = models.CharField(
        _('Course Code'), 
        max_length=20, 
        blank=True, 
        null=True,
        help_text=_('e.g., CS101, MATH200')
    )
    department = models.CharField(
        _('Department'), 
        max_length=100, 
        blank=True, 
        null=True
    )
    semester = models.CharField(
        _('Semester'), 
        max_length=10, 
        choices=SEMESTER_CHOICES, 
        blank=True, 
        null=True
    )
    year = models.IntegerField(
        _('Year'), 
        blank=True, 
        null=True
    )
    language = models.CharField(
        _('Course Language'), 
        max_length=10, 
        choices=LANGUAGE_CHOICES, 
        default='en'
    )
    status = models.CharField(
        _('Status'), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active'
    )
    credits = models.IntegerField(
        _('Credits'), 
        blank=True, 
        null=True
    )
    max_students = models.IntegerField(
        _('Maximum Students'), 
        blank=True, 
        null=True
    )
    syllabus = models.TextField(
        _('Syllabus'), 
        blank=True, 
        null=True
    )
    learning_objectives = models.JSONField(
        _('Learning Objectives'), 
        default=list,
        blank=True,
        help_text=_('List of learning objectives for the course')
    )
    tags = models.JSONField(
        _('Tags'), 
        default=list,
        blank=True,
        help_text=_('Tags to categorize the course')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ['-updated_at']
        unique_together = ['instructor', 'slug']
        
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Course.objects.filter(
                instructor=self.instructor, 
                slug=slug
            ).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.title} - {self.instructor.get_full_name()}"
    
    @property
    def full_course_name(self):
        """Return full course name with code if available"""
        if self.course_code:
            return f"{self.course_code}: {self.title}"
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('courses:detail', kwargs={'slug': self.slug})


class CourseModule(models.Model):
    """Model representing course modules/chapters"""
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules'
    )
    title = models.CharField(_('Module Title'), max_length=200)
    description = models.TextField(
        _('Description'), 
        blank=True, 
        null=True
    )
    order = models.PositiveIntegerField(
        _('Order'), 
        default=0
    )
    content = models.TextField(
        _('Module Content'), 
        blank=True, 
        null=True
    )
    learning_outcomes = models.JSONField(
        _('Learning Outcomes'), 
        default=list,
        blank=True
    )
    duration_hours = models.FloatField(
        _('Duration (hours)'), 
        blank=True, 
        null=True
    )
    is_published = models.BooleanField(
        _('Published'), 
        default=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Course Module')
        verbose_name_plural = _('Course Modules')
        ordering = ['course', 'order']
        unique_together = ['course', 'order']
        
    def __str__(self):
        return f"{self.course.title} - Module {self.order}: {self.title}"


class CourseSettings(models.Model):
    """Model for course-specific settings"""
    
    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE,
        related_name='settings'
    )
    auto_generate_quizzes = models.BooleanField(
        _('Auto Generate Quizzes'), 
        default=False
    )
    quiz_generation_frequency = models.CharField(
        _('Quiz Generation Frequency'), 
        max_length=20,
        choices=[
            ('weekly', _('Weekly')),
            ('biweekly', _('Bi-weekly')),
            ('monthly', _('Monthly')),
            ('manual', _('Manual')),
        ],
        default='manual'
    )
    default_quiz_questions = models.IntegerField(
        _('Default Quiz Questions'), 
        default=10
    )
    exam_versions_count = models.IntegerField(
        _('Exam Versions Count'), 
        default=3
    )
    allow_file_sharing = models.BooleanField(
        _('Allow File Sharing'), 
        default=True
    )
    notification_settings = models.JSONField(
        _('Notification Settings'), 
        default=dict,
        blank=True
    )
    branding_settings = models.JSONField(
        _('Branding Settings'), 
        default=dict,
        blank=True,
        help_text=_('Custom branding for exports (logo, colors, etc.)')
    )
    
    class Meta:
        verbose_name = _('Course Settings')
        verbose_name_plural = _('Course Settings')
        
    def __str__(self):
        return f"Settings for {self.course.title}"
