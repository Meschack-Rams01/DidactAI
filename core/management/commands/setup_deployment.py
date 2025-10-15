"""
Django management command to setup deployment environment
"""

import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Setup deployment environment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-migrate',
            action='store_true',
            help='Skip database migrations',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Setting up DidactAI deployment environment...')
        )

        # Run migrations unless skipped
        if not options['skip_migrate']:
            self.stdout.write('📊 Running database migrations...')
            try:
                call_command('migrate', verbosity=1, interactive=False)
                self.stdout.write(self.style.SUCCESS('✅ Database migrations completed'))
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Migration warning: {e}')
                )

        # Collect static files
        self.stdout.write('📁 Collecting static files...')
        try:
            call_command('collectstatic', verbosity=1, interactive=False, clear=True)
            self.stdout.write(self.style.SUCCESS('✅ Static files collected'))
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Static files warning: {e}')
            )

        # Check if logo files exist in staticfiles
        static_root = settings.STATIC_ROOT
        logo_path = os.path.join(static_root, 'images', 'logo-professional.svg')
        
        if os.path.exists(logo_path):
            self.stdout.write(
                self.style.SUCCESS(f'✅ Logo found: {logo_path}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Logo not found: {logo_path}')
            )
            
            # List what's in the images directory
            images_dir = os.path.join(static_root, 'images')
            if os.path.exists(images_dir):
                files = os.listdir(images_dir)
                self.stdout.write(f'📂 Images directory contains: {files}')
            else:
                self.stdout.write('📂 Images directory does not exist')

        self.stdout.write(
            self.style.SUCCESS('🎉 Deployment setup completed!')
        )