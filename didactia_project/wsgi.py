"""
WSGI config for DidactAI_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didactia_project.settings')

application = get_wsgi_application()

# One-time startup hooks: run migrations and collectstatic if not already done
try:
    RUN_STARTUP = os.environ.get('RUN_DJANGO_STARTUP_TASKS', '1')
    STARTUP_FLAG = '/tmp/didactai_startup_done'
    if RUN_STARTUP == '1' and not os.path.exists(STARTUP_FLAG):
        from django.core.management import call_command
        # Run migrations (non-interactive)
        call_command('migrate', interactive=False, verbosity=1)
        # Collect static files to STATIC_ROOT
        call_command('collectstatic', interactive=False, clear=True, verbosity=1)
        # Create a flag file so we don't repeat on subsequent worker spawns
        with open(STARTUP_FLAG, 'w') as f:
            f.write('ok')
except Exception as _e:
    # Don't crash app if startup tasks fail; app may still serve basic pages
    pass

