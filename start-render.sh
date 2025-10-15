#!/bin/bash
set -e

echo "🚀 Starting DidactAI deployment setup..."

# Run database migrations
echo "📊 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Check if logo files exist
echo "🔍 Checking logo files..."
if [ -f "staticfiles/images/logo-professional.svg" ]; then
    echo "✅ Logo found: staticfiles/images/logo-professional.svg"
else
    echo "⚠️ Logo not found: staticfiles/images/logo-professional.svg"
    echo "📂 Contents of staticfiles/images/:"
    ls -la staticfiles/images/ 2>/dev/null || echo "Directory does not exist"
fi

# Start the application
echo "🌟 Starting DidactAI application..."
exec gunicorn didactia_project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -