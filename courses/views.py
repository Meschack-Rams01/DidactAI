from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Course, CourseModule


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Course.objects.filter(instructor=self.request.user)
        search_query = self.request.GET.get('search')
        status_filter = self.request.GET.get('status')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(course_code__icontains=search_query) |
                Q(department__icontains=search_query)
            )
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset.order_by('-updated_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['status_choices'] = Course.STATUS_CHOICES
        return context


class CourseCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Course
    template_name = 'courses/course_form.html'
    fields = [
        'title', 'description', 'course_code', 'department', 'semester', 
        'year', 'language', 'status', 'credits', 'max_students', 'syllabus',
        'learning_objectives', 'tags'
    ]
    success_message = "Course '%(title)s' was created successfully."
    success_url = reverse_lazy('courses:list')
    
    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.object.modules.filter(is_published=True).order_by('order')
        return context


class CourseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Course
    template_name = 'courses/course_form.html'
    fields = [
        'title', 'description', 'course_code', 'department', 'semester', 
        'year', 'language', 'status', 'credits', 'max_students', 'syllabus',
        'learning_objectives', 'tags'
    ]
    success_message = "Course '%(title)s' was updated successfully."
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('courses:detail', kwargs={'pk': self.object.pk})


class CourseDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_message = "Course was deleted successfully."
    success_url = reverse_lazy('courses:list')
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
