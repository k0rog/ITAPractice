web: gunicorn config.wsgi --log-file -
beat: celery -A config beat
worker: celery -A config worker -l INFO --pool=solo