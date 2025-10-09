web: gunicorn didactia_project.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A didactia_project worker --loglevel=info
release: python manage.py migrate --settings=didactia_project.production_settings