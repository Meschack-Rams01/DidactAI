from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='list'),
    path('create/', views.CourseCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='delete'),
]