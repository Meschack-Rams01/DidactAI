"""
Custom authentication backends for DidactAI
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows users to login with either
    their email address or username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        
        if username is None or password is None:
            return None
        
        try:
            # Try to find user by email or username
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # Multiple users found, try to be more specific
            # First try exact username match
            try:
                user = User.objects.get(username__iexact=username)
            except User.DoesNotExist:
                # Then try exact email match
                try:
                    user = User.objects.get(email__iexact=username)
                except User.DoesNotExist:
                    return None
                except User.MultipleObjectsReturned:
                    # Still multiple results, return None for security
                    return None
            except User.MultipleObjectsReturned:
                # Multiple users with same username (shouldn't happen), return None
                return None

        # Check password and user status
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        """
        Get user by ID.
        """
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None