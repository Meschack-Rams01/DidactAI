#!/usr/bin/env bash
# Render.com build script for DidactAI
# Exit on error
set -o errexit

echo "ðŸš€ Starting DidactAI build process..."

# Install Python dependencies
echo "ðŸ“¦ Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files for production
echo "ðŸŽ¨ Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "ðŸ—„ï¸ Applying database migrations..."
python manage.py migrate

echo "âœ… Build process completed successfully!"
echo "ðŸŽ‰ DidactAI is ready for deployment!"
