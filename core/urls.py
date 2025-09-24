"""
URL configuration for core app
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activity/', views.activity, name='activity'),
    path('test-notification/', views.test_notification, name='test_notification'),
    path('health/', views.health_check, name='health_check'),
]
