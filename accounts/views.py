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
        response = super().form_valid(form)
        # Log the user in after successful registration
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, _('Welcome to DidactIA! Your account has been created successfully.'))
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Account'
        return context


class CustomLoginView(LoginView):
    """Custom login view"""
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, _('Welcome back!'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


@login_required
def profile_view(request):
    """User profile view"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(
            user=request.user,
            timezone='UTC'
        )

    context = {
        'title': 'My Profile',
        'profile': profile,
        'user': request.user,
    }
    return render(request, 'accounts/simple_profile.html', context)
