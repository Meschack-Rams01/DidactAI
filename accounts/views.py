"""
Views for user authentication and account management
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm, UserProfileForm, ExtendedProfileForm
from .models import UserProfile


class RegisterView(CreateView):
    """User registration view"""
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('core:dashboard')

    def form_valid(self, form):
        try:
            print("[REGISTER] Form is valid, saving user...")
            response = super().form_valid(form)
            print("[REGISTER] User saved successfully")
            
            # Log the user in after successful registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            print(f"[REGISTER] Attempting to authenticate user: {username}")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(self.request, user)
                messages.success(self.request, _('Welcome to DidactAI! Your account has been created successfully.'))
                print(f"[REGISTER] User {username} logged in successfully")
            else:
                print(f"[REGISTER] Authentication failed for user: {username}")
            return response
        except Exception as e:
            print(f"[REGISTER] Form valid error: {e}")
            import traceback
            traceback.print_exc()
            messages.error(self.request, _('An error occurred during registration. Please try again.'))
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
        except Exception as e:
            # If Site lookup fails, create basic context without site
            context = {
                'form': kwargs.get('form', self.form_class()),
            }
        context['title'] = 'Create Account'
        return context


class CustomLoginView(LoginView):
    """Custom login view"""
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        try:
            # Log login activity
            from .models import log_user_activity
            log_user_activity(
                user=form.get_user(),
                activity_type='login',
                description=f'Logged in from {form.get_user().get_full_name()}',
                request=self.request
            )
            
            messages.success(self.request, _('Welcome back!'))
            return super().form_valid(form)
        except Exception as e:
            # If logging activity fails, still allow login
            import traceback
            traceback.print_exc()
            messages.success(self.request, _('Welcome back!'))
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
        except Exception as e:
            # If Site lookup fails, create basic context without site
            from django.contrib.auth.forms import AuthenticationForm
            context = {
                'form': kwargs.get('form', self.form_class()),
            }
        context['title'] = 'Login'
        return context


@login_required
def profile_view(request):
    """User profile view with real statistics"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(
            user=request.user,
            timezone='UTC'
        )
    
    # Get real statistics
    quick_stats = request.user.get_quick_stats()
    
    # Get recent activities
    from .models import UserActivity
    recent_activities = UserActivity.objects.filter(
        user=request.user
    ).order_by('-timestamp')[:10]
    
    # Calculate member since
    member_since = request.user.date_joined
    
    context = {
        'title': 'My Profile',
        'profile': profile,
        'user': request.user,
        'quick_stats': quick_stats,
        'recent_activities': recent_activities,
        'member_since': member_since,
        'initials': request.user.get_profile_initials(),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    """Edit user profile view"""
    from .models import log_user_activity, UserProfile
    from .forms import ExtendedProfileForm
    
    # Ensure user has a profile
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(
            user=request.user,
            timezone='UTC'
        )
    
    if request.method == 'POST':
        form = ExtendedProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            
            # Log activity
            log_user_activity(
                user=request.user,
                activity_type='profile_updated',
                description='Updated profile information',
                request=request
            )
            
            messages.success(request, _('Profile updated successfully!'))
            return redirect('accounts:profile')
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ExtendedProfileForm(instance=request.user)
    
    context = {
        'title': 'Edit Profile',
        'user': request.user,
        'profile': profile,
        'form': form,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def notifications_view(request):
    """Notifications settings view"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(
            user=request.user,
            timezone='UTC'
        )
    
    if request.method == 'POST':
        # Update notification preferences
        notifications_prefs = {
            'email_notifications': request.POST.get('email_notifications') == 'on',
            'course_updates': request.POST.get('course_updates') == 'on',
            'file_processed': request.POST.get('file_processed') == 'on',
            'export_ready': request.POST.get('export_ready') == 'on',
            'system_updates': request.POST.get('system_updates') == 'on',
        }
        
        profile.notification_preferences = notifications_prefs
        profile.save()
        
        # Also update user email_notifications field if exists
        request.user.email_notifications = notifications_prefs.get('email_notifications', True)
        request.user.save()
        
        from .models import log_user_activity
        log_user_activity(
            user=request.user,
            activity_type='settings_updated',
            description='Updated notification preferences',
            request=request
        )
        
        messages.success(request, _('Notification settings updated successfully!'))
        return redirect('accounts:notifications')
    
    # Get current preferences
    current_prefs = profile.notification_preferences or {}
    
    context = {
        'title': 'Notification Settings',
        'profile': profile,
        'preferences': current_prefs,
    }
    return render(request, 'accounts/notifications.html', context)


@login_required
def privacy_view(request):
    """Privacy settings view"""
    if request.method == 'POST':
        # Update privacy settings
        user = request.user
        user.profile_public = request.POST.get('profile_public') == 'on'
        user.show_email = request.POST.get('show_email') == 'on'
        user.save()
        
        from .models import log_user_activity
        log_user_activity(
            user=request.user,
            activity_type='settings_updated',
            description='Updated privacy settings',
            request=request
        )
        
        messages.success(request, _('Privacy settings updated successfully!'))
        return redirect('accounts:privacy')
    
    context = {
        'title': 'Privacy Settings',
        'user': request.user,
    }
    return render(request, 'accounts/privacy.html', context)

