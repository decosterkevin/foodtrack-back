release: python manage.py migrate
web: gunicorn foodtrack.wsgi --log-file -
celery-bg: celery -A foodtrack worker -l info
