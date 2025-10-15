release: python manage.py migrate --run-syncdb && python manage.py setup_site
web: gunicorn didactia_project.wsgi:application --bind 0.0.0.0:$PORT
