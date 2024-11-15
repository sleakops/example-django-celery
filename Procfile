web: python manage.py runserver 0.0.0.0:8000
worker: celery -A core.celery worker -l INFO --concurrency 1 --max-tasks-per-child 1 --prefetch-multiplier 1 -n celery@%h