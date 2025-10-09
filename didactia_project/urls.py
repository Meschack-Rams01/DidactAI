﻿"""
URL configuration for DidactAI_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('health-check/', health_check, name='health_check'),  # Health check endpoint
    path('accounts/', include('accounts.urls')),
    path('auth/', include('django.contrib.auth.urls')),  # Keep for built-in auth views
    path('courses/', include('courses.urls')),
    path('exports/', include('exports.urls')),
    path('ai-generator/', include('ai_generator.urls')),
    path('uploads/', include('uploads.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

