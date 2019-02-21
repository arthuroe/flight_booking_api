release: python manage.py db migrate
release: python manage.py db upgrade

web: gunicorn app:app

worker: celery worker -A app.celery --beat --schedule=/tmp/celerybeat-schedule --loglevel=INFO --pidfile=/tmp/celerybeat.pid
