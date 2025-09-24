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
        
        # Prepare response
        response = HttpResponse(
            export.generated_file.read(),
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = f'attachment; filename="{export.title}.{export.export_format}"'
        
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
            branding_settings={
                'institution_name': request.POST.get('institution_name', ''),
                'department': request.POST.get('department', '')
            }
        )
        
        # Process export
        try:
            from .services import ExportService
            export_service = ExportService()
            if create_versions and export_format in ['pdf', 'zip']:
                result = export_service.export_with_versions(export_job, num_versions=3)
            else:
                result = export_service.export_generation(export_job)
            
            if result['success']:
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
