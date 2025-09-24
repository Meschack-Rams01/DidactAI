import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from courses.models import Course
from uploads.models import UploadedFile


class GenerationTemplate(models.Model):
    """Templates for AI content generation"""
    
    TEMPLATE_TYPE_CHOICES = [
        ('quiz', _('Quiz Template')),
        ('exam', _('Exam Template')),
        ('syllabus', _('Syllabus Template')),
        ('flashcards', _('Flashcards Template')),
        ('summary', _('Summary Template')),
    ]
    
    name = models.CharField(_('Template Name'), max_length=200)
    template_type = models.CharField(
        _('Template Type'), 
        max_length=20, 
        choices=TEMPLATE_TYPE_CHOICES
    )
    description = models.TextField(
        _('Description'), 
        blank=True, 
        null=True
    )
    prompt_template = models.TextField(
        _('Prompt Template'),
        help_text=_('AI prompt template with placeholders like {content}, {language}, etc.')
    )
    parameters = models.JSONField(
        _('Template Parameters'), 
        default=dict,
        blank=True,
        help_text=_('Default parameters for this template')
    )
    is_system_template = models.BooleanField(
        _('System Template'), 
        default=False,
        help_text=_('System templates are available to all users')
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='generation_templates'
    )
    is_active = models.BooleanField(_('Active'), default=True)
    usage_count = models.PositiveIntegerField(
        _('Usage Count'), 
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Generation Template')
        verbose_name_plural = _('Generation Templates')
        ordering = ['-usage_count', '-updated_at']
        
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    def increment_usage(self):
        """Increment usage count"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])


class AIGeneration(models.Model):
    """Model for AI-generated content"""
    
    CONTENT_TYPE_CHOICES = [
        ('quiz', _('Quiz')),
        ('exam', _('Exam')),
        ('syllabus', _('Syllabus')),
        ('flashcards', _('Flashcards')),
        ('summary', _('Summary')),
        ('questions', _('Questions')),
        ('answers', _('Answers')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('error', _('Error')),
        ('cancelled', _('Cancelled')),
    ]
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='ai_generations'
    )
    source_files = models.ManyToManyField(
        UploadedFile,
        related_name='ai_generations',
        blank=True,
        help_text=_('Source files used for generation')
    )
    template = models.ForeignKey(
        GenerationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generations'
    )
    content_type = models.CharField(
        _('Content Type'), 
        max_length=20, 
        choices=CONTENT_TYPE_CHOICES
    )
    title = models.CharField(
        _('Generation Title'), 
        max_length=200
    )
    description = models.TextField(
        _('Description'), 
        blank=True, 
        null=True
    )
    input_prompt = models.TextField(
        _('Input Prompt'),
        help_text=_('The prompt sent to the AI model')
    )
    input_parameters = models.JSONField(
        _('Input Parameters'), 
        default=dict,
        blank=True,
        help_text=_('Parameters used for generation (questions count, difficulty, etc.)')
    )
    generated_content = models.JSONField(
        _('Generated Content'), 
        default=dict,
        blank=True,
        help_text=_('The AI-generated content in structured format')
    )
    status = models.CharField(
        _('Status'), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    ai_model = models.CharField(
        _('AI Model'), 
        max_length=50, 
        default='gemini-1.5-flash'
    )
    tokens_used = models.PositiveIntegerField(
        _('Tokens Used'), 
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
    quality_score = models.FloatField(
        _('Quality Score'), 
        blank=True, 
        null=True,
        help_text=_('Auto-calculated quality score (0.0-1.0)')
    )
    user_rating = models.PositiveIntegerField(
        _('User Rating'), 
        blank=True, 
        null=True,
        help_text=_('User rating (1-5 stars)')
    )
    is_favorite = models.BooleanField(
        _('Favorite'), 
        default=False
    )
    tags = models.JSONField(
        _('Tags'), 
        default=list,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(
        _('Completed At'), 
        blank=True, 
        null=True
    )
    
    class Meta:
        verbose_name = _('AI Generation')
        verbose_name_plural = _('AI Generations')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.get_content_type_display()}"
    
    def mark_completed(self):
        """Mark generation as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])
    
    def mark_error(self, error_message):
        """Mark generation as error with message"""
        self.status = 'error'
        self.error_message = error_message
        self.save(update_fields=['status', 'error_message'])


class GenerationVersion(models.Model):
    """Model for versioning AI generations"""
    
    original_generation = models.ForeignKey(
        AIGeneration,
        on_delete=models.CASCADE,
        related_name='versions'
    )
    version_letter = models.CharField(
        _('Version Letter'), 
        max_length=1, 
        default='A',
        help_text=_('Version identifier (A, B, C, etc.)')
    )
    generated_content = models.JSONField(
        _('Generated Content'), 
        default=dict
    )
    variations = models.JSONField(
        _('Content Variations'), 
        default=dict,
        blank=True,
        help_text=_('Specific variations for this version (question order, values, etc.)')
    )
    answer_key = models.JSONField(
        _('Answer Key'), 
        default=dict,
        blank=True
    )
    is_primary = models.BooleanField(
        _('Primary Version'), 
        default=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Generation Version')
        verbose_name_plural = _('Generation Versions')
        ordering = ['version_letter']
        unique_together = ['original_generation', 'version_letter']
        
    def __str__(self):
        return f"{self.original_generation.title} - Version {self.version_letter}"


class QuizQuestion(models.Model):
    """Model for individual quiz questions"""
    
    QUESTION_TYPE_CHOICES = [
        ('mcq', _('Multiple Choice')),
        ('true_false', _('True/False')),
        ('short_answer', _('Short Answer')),
        ('long_answer', _('Long Answer')),
        ('fill_blank', _('Fill in the Blank')),
        ('matching', _('Matching')),
        ('ordering', _('Ordering')),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', _('Easy')),
        ('medium', _('Medium')),
        ('hard', _('Hard')),
    ]
    
    generation = models.ForeignKey(
        AIGeneration,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_type = models.CharField(
        _('Question Type'), 
        max_length=20, 
        choices=QUESTION_TYPE_CHOICES
    )
    question_text = models.TextField(_('Question Text'))
    options = models.JSONField(
        _('Answer Options'), 
        default=list,
        blank=True,
        help_text=_('List of answer options for MCQ questions')
    )
    correct_answer = models.TextField(
        _('Correct Answer'),
        help_text=_('The correct answer or answer key')
    )
    explanation = models.TextField(
        _('Explanation'), 
        blank=True, 
        null=True
    )
    difficulty = models.CharField(
        _('Difficulty'), 
        max_length=10, 
        choices=DIFFICULTY_CHOICES, 
        default='medium'
    )
    points = models.PositiveIntegerField(
        _('Points'), 
        default=1
    )
    order = models.PositiveIntegerField(
        _('Order'), 
        default=0
    )
    tags = models.JSONField(
        _('Tags'), 
        default=list,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Quiz Question')
        verbose_name_plural = _('Quiz Questions')
        ordering = ['generation', 'order']
        
    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}..."


class GenerationFeedback(models.Model):
    """Model for user feedback on AI generations"""
    
    FEEDBACK_TYPE_CHOICES = [
        ('rating', _('Rating')),
        ('correction', _('Correction')),
        ('suggestion', _('Suggestion')),
        ('complaint', _('Complaint')),
    ]
    
    generation = models.ForeignKey(
        AIGeneration,
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_feedback'
    )
    feedback_type = models.CharField(
        _('Feedback Type'), 
        max_length=20, 
        choices=FEEDBACK_TYPE_CHOICES
    )
    rating = models.PositiveIntegerField(
        _('Rating'), 
        blank=True, 
        null=True,
        help_text=_('Rating from 1 to 5')
    )
    comment = models.TextField(
        _('Comment'), 
        blank=True, 
        null=True
    )
    suggested_improvements = models.JSONField(
        _('Suggested Improvements'), 
        default=dict,
        blank=True
    )
    is_public = models.BooleanField(
        _('Public Feedback'), 
        default=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Generation Feedback')
        verbose_name_plural = _('Generation Feedback')
        ordering = ['-created_at']
        unique_together = ['generation', 'user', 'feedback_type']
        
    def __str__(self):
        return f"{self.get_feedback_type_display()} for {self.generation.title}"
