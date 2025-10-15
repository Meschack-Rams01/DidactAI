from django.db import migrations


def create_site(apps, schema_editor):
    """Create or update the Site record for DidactAI"""
    Site = apps.get_model('sites', 'Site')
    
    # Create or update site with id=1
    site, created = Site.objects.get_or_create(
        id=1,
        defaults={
            'domain': 'didactai.onrender.com',
            'name': 'DidactAI'
        }
    )
    
    if not created:
        # Update existing site
        site.domain = 'didactai.onrender.com'
        site.name = 'DidactAI'
        site.save()


def reverse_create_site(apps, schema_editor):
    """Remove the Site record"""
    Site = apps.get_model('sites', 'Site')
    Site.objects.filter(id=1).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_update_gemini_model_2_5'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(create_site, reverse_create_site),
    ]