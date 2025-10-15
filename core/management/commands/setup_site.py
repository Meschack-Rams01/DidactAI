from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Setup Django Site with correct domain'

    def handle(self, *args, **options):
        site_id = getattr(settings, 'SITE_ID', 1)
        domain = 'didactai.onrender.com'
        name = 'DidactAI'
        
        try:
            site, created = Site.objects.get_or_create(
                id=site_id,
                defaults={
                    'domain': domain,
                    'name': name
                }
            )
            
            if not created:
                # Update existing site
                site.domain = domain
                site.name = name
                site.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Updated site: {name} ({domain})')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Created site: {name} ({domain})')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error setting up site: {e}')
            )
            raise e