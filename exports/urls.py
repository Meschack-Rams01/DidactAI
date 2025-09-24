from django.urls import path
from . import views

app_name = 'exports'

urlpatterns = [
    path('', views.ExportListView.as_view(), name='list'),
    path('create/', views.ExportCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ExportDetailView.as_view(), name='detail'),
    path('<int:pk>/download/', views.ExportDownloadView.as_view(), name='download'),
    path('<int:pk>/delete/', views.ExportDeleteView.as_view(), name='delete'),
    
    # Export from AI generation
    path('generation/<int:generation_id>/', views.export_generation, name='export_generation'),
    
]
