#!/bin/bash
set -Eeuo pipefail

echo "=== Starting DidactAI Deployment ==="

# Ensure the data directory exists and has proper permissions
mkdir -p /var/data
chmod 755 /var/data

echo "=== Database Configuration ==="
echo "RENDER_DISK_PATH: ${RENDER_DISK_PATH}"
echo "Database will be at: ${RENDER_DISK_PATH}/db.sqlite3"

echo "=== Running Database Migrations ==="
python manage.py showmigrations accounts || true
python manage.py makemigrations accounts --noinput || true
python manage.py migrate --noinput --run-syncdb --verbosity=2
python manage.py migrate accounts --noinput --verbosity=2

echo "=== Setting up Site ==="
python manage.py setup_site

echo "=== Checking Database Tables ==="
python -c "
import sqlite3
import os
db_path = os.environ.get('RENDER_DISK_PATH', '.') + '/db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\" AND name LIKE \"%user%\";')
    tables = cursor.fetchall()
    print('User-related tables:', tables)
    conn.close()
else:
    print('Database file not found at:', db_path)
"

echo "=== Starting Gunicorn Server ==="
exec gunicorn didactia_project.wsgi:application \
    --bind 0.0.0.0:10000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
