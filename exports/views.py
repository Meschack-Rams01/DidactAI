from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.db import models
from .models import ExportJob, ExportTemplate
from ai_generator.models import AIGeneration


class ExportListView(LoginRequiredMixin, ListView):
    model = ExportJob
    template_name = 'exports/export_list.html'
    context_object_name = 'exports'
    paginate_by = 12
    
    def get_queryset(self):
        return ExportJob.objects.filter(
            course__instructor=self.request.user
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_exports'] = self.get_queryset().count()
        context['completed_exports'] = self.get_queryset().filter(status='completed').count()
        return context


class ExportCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ExportJob
    template_name = 'exports/export_form.html'
    fields = ['title', 'description', 'export_format', 'template']
    success_message = "Export '%(title)s' was created successfully."
    success_url = reverse_lazy('exports:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['templates'] = ExportTemplate.objects.filter(
            is_active=True
        ).order_by('-usage_count')
        return context


class ExportDetailView(LoginRequiredMixin, DetailView):
    model = ExportJob
    template_name = 'exports/export_detail.html'
    context_object_name = 'export'
    
    def get_queryset(self):
        return ExportJob.objects.filter(
            course__instructor=self.request.user
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['versions'] = self.object.versions.all()
        context['logs'] = self.object.logs.all()[:10]
        return context


class ExportDownloadView(LoginRequiredMixin, DetailView):
    model = ExportJob
    
    def get_queryset(self):
        return ExportJob.objects.filter(
            course__instructor=self.request.user,
            status='completed'
        )
    
    def get(self, request, *args, **kwargs):
        export = self.get_object()
        
        if not export.generated_file:
            raise Http404("Export file not found")
        
        # Increment download count
        export.increment_download_count()
        
        # Determine content type based on export format
        content_type_mapping = {
            'pdf': 'application/pdf',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'html': 'text/html; charset=utf-8',
            'txt': 'text/plain; charset=utf-8',
            'zip': 'application/zip',
            'json': 'application/json; charset=utf-8',
            'xml': 'application/xml; charset=utf-8'
        }
        
        content_type = content_type_mapping.get(
            export.export_format.lower(), 
            'application/octet-stream'
        )
        
        # Prepare response
        response = HttpResponse(
            export.generated_file.read(),
            content_type=content_type
        )
        
        # Set proper file extension and encoding for filename
        import urllib.parse
        
        # Ensure filename has correct extension
        filename = export.title
        if not filename.lower().endswith(f'.{export.export_format.lower()}'):
            filename = f"{filename}.{export.export_format.lower()}"
        
        # Encode filename properly for international characters
        safe_filename = urllib.parse.quote(filename, safe='')
        response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'\'{safe_filename}'
        
        # Set additional headers for better download experience
        response['Content-Length'] = export.generated_file.size
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        # Track download for analytics
        try:
            from .analytics import track_download
            track_download(export, request.user)
        except Exception as e:
            # Don't break download if analytics fails
            import logging
            logging.getLogger(__name__).warning(f"Analytics tracking failed: {str(e)}")
        
        return response


class ExportDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ExportJob
    template_name = 'exports/export_confirm_delete.html'
    success_message = "Export was deleted successfully."
    success_url = reverse_lazy('exports:list')
    
    def get_queryset(self):
        return ExportJob.objects.filter(
            course__instructor=self.request.user
        )
    
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


@login_required
def export_generation(request, generation_id):
    """Create export from AI generation"""
    generation = get_object_or_404(
        AIGeneration, 
        id=generation_id, 
        course__instructor=request.user
    )
    
    # If it's a GET request, show the export form
    if request.method == 'GET':
        context = {
            'title': f'Export: {generation.title}',
            'generation': generation,
            'format_choices': ExportJob.FORMAT_CHOICES,
        }
        return render(request, 'exports/export_generation_form.html', context)
    
    if request.method == 'POST':
        export_format = request.POST.get('format', 'pdf')
        include_answer_key = request.POST.get('include_answer_key') == 'on'
        include_instructions = request.POST.get('include_instructions', 'on') == 'on'
        create_versions = request.POST.get('create_versions') == 'on'
        title = request.POST.get('title') or generation.title
        
        # Create export job
        export_job = ExportJob.objects.create(
            course=generation.course,
            generation=generation,
            title=title,
            description=request.POST.get('description', ''),
            export_format=export_format,
            include_answer_key=include_answer_key,
            include_instructions=include_instructions,
            watermark=request.POST.get('watermark', ''),
            university_logo=request.FILES.get('university_logo'),
            branding_settings={
                'institution_name': request.POST.get('institution_name', ''),
                'department': request.POST.get('department', '')
            }
        )
        
        # Process export with enhanced branding
        try:
            from .services import ExportService, WEASYPRINT_AVAILABLE
            
            # Check if WeasyPrint is available for certain formats
            # Note: ReportLab is used as primary PDF generator on Windows
            export_service = ExportService()
            
            # Enhanced branding settings with comprehensive university information
            export_job.branding_settings.update({
                'university_name': request.POST.get('university_name', request.POST.get('institution_name', '')),
                'faculty': request.POST.get('faculty', ''),
                'department': request.POST.get('department', ''),
                'course': request.POST.get('course', ''),
                'academic_year': request.POST.get('academic_year', ''),
                'semester': request.POST.get('semester', ''),
                'instructor': request.POST.get('instructor', ''),
                'exam_date': request.POST.get('exam_date', ''),
                'additional_notes': request.POST.get('additional_notes', ''),
                # Student information fields configuration
                'student_info': {
                    'include_student_name': request.POST.get('include_student_name') == 'on',
                    'include_student_id': request.POST.get('include_student_id') == 'on',
                    'include_signature': request.POST.get('include_signature') == 'on',
                    'include_date_field': request.POST.get('include_date_field') == 'on'
                },
                # Logo upload handling
                'has_logo': 'university_logo' in request.FILES
            })
            
            # Handle logo upload if present
            if export_job.university_logo:
                # Update branding settings with logo information
                export_job.branding_settings['logo_path'] = export_job.university_logo.path
                export_job.branding_settings['logo_url'] = export_job.university_logo.url
                export_job.branding_settings['logo_filename'] = export_job.university_logo.name
            export_job.save()
            
            if create_versions and export_format in ['pdf', 'zip']:
                # Create multiple versions for exams
                result = export_service.export_content(
                    content_data=export_service._prepare_generation_data(generation),
                    export_format='zip',
                    branding=export_job.branding_settings,
                    versions=['A', 'B', 'C']
                )
            else:
                result = export_service.export_generation(export_job)
            
            if result['success']:
                # Track export creation for analytics
                try:
                    from .analytics import ExportAnalytics
                    analytics = ExportAnalytics()
                    analytics.track_export_creation(
                        export_job=export_job,
                        user=request.user,
                        creation_details={
                            'branding': export_job.branding_settings,
                            'versions': 3 if create_versions else 1,
                            'include_answer_key': include_answer_key,
                            'format': export_format
                        }
                    )
                except Exception as e:
                    # Don't break the flow if analytics fails
                    import logging
                    logging.getLogger(__name__).warning(f"Analytics tracking failed: {str(e)}")
                
                messages.success(request, f'Export "{title}" created successfully!')
                return redirect('exports:detail', pk=export_job.id)
            else:
                messages.error(request, f'Export failed: {result.get("error")}')
        except Exception as e:
            messages.error(request, f'Export error: {str(e)}')
    
    context = {
        'title': f'Export: {generation.title}',
        'generation': generation,
        'format_choices': ExportJob.FORMAT_CHOICES,
    }
    
    return render(request, 'exports/export_generation_form.html', context)


# Export Template Views
class ExportTemplateListView(LoginRequiredMixin, ListView):
    model = ExportTemplate
    template_name = 'exports/template_list.html'
    context_object_name = 'templates'
    paginate_by = 12
    
    def get_queryset(self):
        return ExportTemplate.objects.filter(
            models.Q(created_by=self.request.user) |
            models.Q(is_system_template=True)
        ).filter(is_active=True).order_by('-usage_count', '-updated_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_templates'] = self.get_queryset().count()
        context['user_templates'] = ExportTemplate.objects.filter(
            created_by=self.request.user, is_active=True
        ).count()
        context['system_templates'] = ExportTemplate.objects.filter(
            is_system_template=True, is_active=True
        ).count()
        return context


class ExportTemplateDetailView(LoginRequiredMixin, DetailView):
    model = ExportTemplate
    template_name = 'exports/template_detail.html'
    context_object_name = 'template'
    
    def get_queryset(self):
        return ExportTemplate.objects.filter(
            models.Q(created_by=self.request.user) |
            models.Q(is_system_template=True)
        ).filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_exports'] = ExportJob.objects.filter(
            template=self.object,
            course__instructor=self.request.user
        ).order_by('-created_at')[:5]
        return context


class ExportTemplateCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ExportTemplate
    template_name = 'exports/template_form.html'
    fields = ['name', 'template_type', 'content_type', 'description', 'template_content', 'css_styles']
    success_message = "Template '%(name)s' was created successfully."
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('exports:template_detail', kwargs={'pk': self.object.pk})


@login_required
def test_clean_export(request):
    """Quick test endpoint for clean export functionality"""
    from .services import PDFExporter, HTMLExporter
    
    # Sample data for testing
    test_data = {
        'title': 'Cloud Computing Fundamentals and Computing Paradigms - CLEAN TEST',
        'description': 'Professional exam format without question type labels',
        'questions': [
            {
                'type': 'multiple_choice',
                'question': 'What is the primary benefit of cloud computing scalability?',
                'options': [
                    'Reduced hardware costs',
                    'Automatic resource adjustment based on demand', 
                    'Faster network speeds',
                    'Better security protocols'
                ],
                'correct_answer': 'B',
                'points': 5
            },
            {
                'type': 'true_false',
                'question': 'Infrastructure as a Service (IaaS) provides the highest level of control over computing resources.',
                'correct_answer': 'True', 
                'points': 3
            },
            {
                'type': 'short_answer',
                'question': 'Explain the difference between public and private cloud deployments.',
                'points': 10
            }
        ]
    }
    
    branding = {
        'university_name': 'Technical University',
        'department': 'Computer Science Department',
        'course': 'CS 4800 - Cloud Computing',
        'semester': 'Fall 2024',
        'instructor': 'Dr. Smith'
    }
    
    try:
        pdf_exporter = PDFExporter() 
        pdf_buffer = pdf_exporter.export_quiz(test_data, branding)
        
        response = HttpResponse(
            pdf_buffer.getvalue(),
            content_type='application/pdf'
        )
        response['Content-Disposition'] = 'attachment; filename="clean_export_test.pdf"'
        return response
        
    except Exception as e:
        messages.error(request, f'Test export failed: {str(e)}')
        return redirect('exports:list')


@login_required
def use_template(request, template_id):
    """View to use a template for creating exports"""
    # Get the template with proper filtering
    try:
        template = ExportTemplate.objects.get(
            id=template_id,
            is_active=True
        )
        # Check access permission
        if not (template.created_by == request.user or template.is_system_template):
            raise Http404("Template not found or access denied")
    except ExportTemplate.DoesNotExist:
        raise Http404("Template not found")
    
    # Get user's recent AI generations
    from ai_generator.models import AIGeneration
    recent_generations = AIGeneration.objects.filter(
        course__instructor=request.user,
        status='completed'
    ).order_by('-created_at')[:10]
    
    if request.method == 'POST':
        generation_id = request.POST.get('generation_id')
        export_format = request.POST.get('format', 'html')
        include_answer_key = request.POST.get('include_answer_key') == 'on'
        title = request.POST.get('title') or f'Export using {template.name}'
        
        if generation_id:
            generation = get_object_or_404(
                AIGeneration,
                id=generation_id,
                course__instructor=request.user
            )
            
            # Create export job with the selected template
            export_job = ExportJob.objects.create(
                course=generation.course,
                generation=generation,
                template=template,
                title=title,
                description=request.POST.get('description', ''),
                export_format=export_format,
                include_answer_key=include_answer_key,
                include_instructions=request.POST.get('include_instructions', 'on') == 'on',
                watermark=request.POST.get('watermark', ''),
                branding_settings={
                    'institution_name': request.POST.get('institution_name', ''),
                    'department': request.POST.get('department', '')
                }
            )
            
            # Process export
            try:
                from .services import ExportService
                export_service = ExportService()
                result = export_service.export_generation(export_job)
                
                if result['success']:
                    # Increment template usage
                    template.increment_usage()
                    messages.success(request, f'Export "{title}" created successfully using template "{template.name}"!')
                    return redirect('exports:detail', pk=export_job.id)
                else:
                    messages.error(request, f'Export failed: {result.get("error")}')
            except Exception as e:
                messages.error(request, f'Export error: {str(e)}')
        else:
            messages.error(request, 'Please select an AI generation to export.')
    
    context = {
        'template': template,
        'recent_generations': recent_generations,
        'format_choices': ExportJob.FORMAT_CHOICES,
    }
    
    return render(request, 'exports/use_template.html', context)
