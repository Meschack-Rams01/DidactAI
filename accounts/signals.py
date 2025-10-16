"""
Signal handlers for user authentication events
"""

import logging
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def send_login_notification(sender, user, request, **kwargs):
    """
    Send email notification when user logs in (disabled for now to prevent timeouts)
    """
    try:
        # TEMPORARILY DISABLED: Email notifications cause timeouts on Render
        # Skip email sending until proper email backend is configured
        
        # Log the login for security purposes instead
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')[:100]  # Truncate user agent
        login_time = timezone.now()
        
        logger.info(
            f"User login: {user.username} ({user.email}) from {ip_address} "
            f"at {login_time} using {user_agent}"
        )
        
        # TODO: Re-enable email notifications when proper email backend is set up
        # For now, just return without sending email
        return
        
    except Exception as e:
        logger.error(f"Error in login notification handler: {str(e)}")
        # Don't re-raise - this should never break the login process


def get_client_ip(request):
    """
    Get the client's IP address from the request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
