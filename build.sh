#!/usr/bin/env bash
# Render.com build script for DidactIA
# Exit on error
set -o errexit

echo "🚀 Starting DidactIA build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files for production
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "🗄️ Applying database migrations..."
python manage.py migrate

echo "✅ Build process completed successfully!"
echo "🎉 DidactIA is ready for deployment!"