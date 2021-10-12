import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'pulling-games-to-database': {
        'task': 'gamehub.tasks.pull_games',
        'schedule': 30.0,
    }
}
