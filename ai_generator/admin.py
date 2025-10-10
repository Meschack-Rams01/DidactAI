from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    GenerationTemplate, 
    AIGeneration, 
    GenerationVersion, 
    QuizQuestion, 
    GenerationFeedback
)


@admin.register(GenerationTemplate)
class GenerationTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'template_type', 
        'is_system_template', 
        'is_active', 
        'usage_count',
        'created_by',
        'created_at'
    ]
    list_filter = [
        'template_type', 
        'is_system_template', 
        'is_active',
        'created_at'
    ]
    search_fields = ['name', 'description', 'created_by__username']
    readonly_fields = ['usage_count', 'created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'template_type', 'description')
        }),
        ('Template Configuration', {
            'fields': ('prompt_template', 'parameters')
        }),
        ('Settings', {
            'fields': ('is_system_template', 'is_active', 'created_by')
        }),
        ('Statistics', {
            'fields': ('usage_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')


@admin.register(AIGeneration)
class AIGenerationAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'content_type',
        'course',
        'status',
        'ai_model',
        'user_rating',
        'created_at'
    ]
    list_filter = [
        'content_type',
        'status',
        'ai_model',
        'user_rating',
        'is_favorite',
        'created_at'
    ]
    search_fields = [
        'title',
        'description',
        'course__title',
        'course__instructor__username'
    ]
    readonly_fields = [
        'tokens_used',
        'processing_time_seconds',
        'quality_score',
        'created_at',
        'updated_at',
        'completed_at'
    ]
    
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'content_type', 'description')
        }),
        ('Generation Settings', {
            'fields': ('template', 'input_prompt', 'input_parameters')
        }),
        ('AI Configuration', {
            'fields': ('ai_model', 'status')
        }),
        ('Results', {
            'fields': ('generated_content', 'error_message'),
            'classes': ('collapse',)
        }),
        ('Feedback & Rating', {
            'fields': ('user_rating', 'is_favorite', 'tags')
        }),
        ('Statistics', {
            'fields': (
                'tokens_used',
                'processing_time_seconds',
                'quality_score',
                'created_at',
                'updated_at',
                'completed_at'
            ),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'course',
            'course__instructor',
            'template'
        ).prefetch_related('source_files')
    
    def view_course_link(self, obj):
        if obj.course:
            url = reverse('admin:courses_course_change', args=[obj.course.pk])
            return format_html('<a href="{}">{}</a>', url, obj.course.title)
        return '-'
    view_course_link.short_description = 'Course'


@admin.register(GenerationVersion)
class GenerationVersionAdmin(admin.ModelAdmin):
    list_display = [
        'original_generation',
        'version_letter',
        'is_primary',
        'created_at'
    ]
    list_filter = [
        'is_primary',
        'version_letter',
        'created_at'
    ]
    search_fields = [
        'original_generation__title',
        'version_letter'
    ]
    readonly_fields = ['created_at']
    
    fieldsets = (
        (None, {
            'fields': ('original_generation', 'version_letter', 'is_primary')
        }),
        ('Content', {
            'fields': ('generated_content', 'variations', 'answer_key')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = [
        'question_preview',
        'generation',
        'question_type',
        'difficulty',
        'points',
        'order'
    ]
    list_filter = [
        'question_type',
        'difficulty',
        'generation__content_type'
    ]
    search_fields = [
        'question_text',
        'generation__title'
    ]
    readonly_fields = ['created_at']
    
    fieldsets = (
        (None, {
            'fields': ('generation', 'question_type', 'order')
        }),
        ('Question Content', {
            'fields': ('question_text', 'options', 'correct_answer', 'explanation')
        }),
        ('Settings', {
            'fields': ('difficulty', 'points', 'tags')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def question_preview(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_preview.short_description = 'Question'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('generation')


@admin.register(GenerationFeedback)
class GenerationFeedbackAdmin(admin.ModelAdmin):
    list_display = [
        'generation',
        'user',
        'feedback_type',
        'rating',
        'is_public',
        'created_at'
    ]
    list_filter = [
        'feedback_type',
        'rating',
        'is_public',
        'created_at'
    ]
    search_fields = [
        'generation__title',
        'user__username',
        'comment'
    ]
    readonly_fields = ['created_at']
    
    fieldsets = (
        (None, {
            'fields': ('generation', 'user', 'feedback_type')
        }),
        ('Feedback Content', {
            'fields': ('rating', 'comment', 'suggested_improvements')
        }),
        ('Settings', {
            'fields': ('is_public',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'generation',
            'user'
        )
