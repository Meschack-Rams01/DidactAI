"""
URL Configuration for Uploads app
"""

from django.urls import path
from . import views

app_name = 'uploads'

urlpatterns = [
    # File management views
    path('', views.file_list, name='list'),
    path('upload/', views.upload_file, name='upload'),
    path('<int:file_id>/', views.file_detail, name='detail'),
    path('<int:file_id>/download/', views.download_file, name='download'),
    path('<int:file_id>/delete/', views.delete_file, name='delete'),
    
    # AJAX endpoints
    path('ajax/upload/', views.ajax_upload, name='ajax_upload'),
    
    # API endpoints
    path('api/course/<int:course_id>/files/', views.api_course_files, name='api_course_files'),
]
