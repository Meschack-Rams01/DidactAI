"""
URL Configuration for AI Generator app
"""

from django.urls import path
from . import views

app_name = 'ai_generator'

urlpatterns = [
    # Index page
    path('', views.index, name='index'),
    
    # Generator views
    path('quiz/', views.quiz_generator, name='quiz_generator'),
    path('exam/', views.exam_generator, name='exam_generator'),
    
    # View generated content
    path('view/<int:generation_id>/', views.view_generation, name='view_generation'),
    path('edit/<int:generation_id>/', views.edit_generation, name='edit_generation'),
    
    # Versioning
    path('create-version/<int:generation_id>/', views.create_version, name='create_version'),
    path('version/<int:generation_id>/<str:version_letter>/', views.view_version, name='view_version'),
    path('delete-version/<int:generation_id>/<str:version_letter>/', views.delete_version, name='delete_version'),
    
    # History
    path('history/', views.generation_history, name='history'),
    
    # Delete, Duplicate, Export
    path('delete/<int:generation_id>/', views.delete_generation, name='delete_generation'),
    path('duplicate/<int:generation_id>/', views.duplicate_generation, name='duplicate_generation'),
    path('export/<int:generation_id>/', views.export_generation, name='export_generation'),
]
