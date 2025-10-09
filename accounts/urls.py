"""
URL configuration for accounts app
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Registration
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    
    # Account Settings
    path('settings/password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/change_password.html',
        success_url='/accounts/profile/'
    ), name='change_password'),
    path('settings/notifications/', views.notifications_view, name='notifications'),
    path('settings/privacy/', views.privacy_view, name='privacy'),
    
    # Password reset
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]