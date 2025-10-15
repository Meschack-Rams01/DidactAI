#!/bin/bash

# Startup script for DidactAI on Render
echo "Starting DidactAI application..."

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --settings=didactia_project.settings

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=didactia_project.settings

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn didactia_project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info