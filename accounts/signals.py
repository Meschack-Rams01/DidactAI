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
    Send email notification when user logs in
    """
    try:
        # Only send email if user has an email and email backend is configured
        if not user.email or not hasattr(settings, 'EMAIL_HOST_USER') or not settings.EMAIL_HOST_USER:
            return
        
        # Get user's IP address and user agent for security info
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        login_time = timezone.now()
        
        # Prepare context for email template
        context = {
            'user': user,
            'login_time': login_time,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'site_name': 'DidactAI',
            'site_url': request.build_absolute_uri('/'),
        }
        
        # Render email templates
        html_message = render_to_string('emails/login_notification.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject='New Sign-in to Your DidactAI Account',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=True,  # Don't break login if email fails
        )
        
        logger.info(f"Login notification sent to {user.email}")
        
    except Exception as e:
        logger.error(f"Failed to send login notification to {user.email}: {str(e)}")


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
