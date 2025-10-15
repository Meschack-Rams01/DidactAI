#!/bin/bash
# DidactAI Deployment Script

echo "ðŸš€ Starting DidactAI Deployment..."

# Update code
git pull origin main

# Install/update dependencies
pip install -r requirements-fixed.txt --upgrade

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

# Create superuser if it doesn't exist
python manage.py shell -c "
from accounts.models import CustomUser
if not CustomUser.objects.filter(is_superuser=True).exists():
    print('Creating superuser...')
    CustomUser.objects.create_superuser(
        email='admin@yourdomain.com',
        username='admin',
        password='change-this-password'
    )
    print('Superuser created!')
else:
    print('Superuser already exists')
"

# Restart services
sudo systemctl restart DidactAI
sudo systemctl restart nginx

echo "✓œ… Deployment completed!"
