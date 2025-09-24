from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('Profile')
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'avatar', 'role', 'institution', 'department', 'preferred_language', 'phone_number', 'bio')}),
        (_('Auto-delete settings'), {'fields': ('auto_delete_enabled', 'auto_delete_days')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_email_verified', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'last_activity')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'role'),
        }),
    )
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'institution', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'is_email_verified', 'preferred_language')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'institution', 'department')
    ordering = ('-date_joined',)
    readonly_fields = ('last_activity',)


admin.site.register(CustomUser, CustomUserAdmin)
