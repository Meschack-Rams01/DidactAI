web: python prestart.py && gunicorn didactia_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
worker: celery -A didactia_project worker --loglevel=info
release: python manage.py migrate --noinput --settings=didactia_project.settings
