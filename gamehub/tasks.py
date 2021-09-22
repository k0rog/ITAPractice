from celery import shared_task
from django.core.management import call_command


@shared_task
def pull_games():
    call_command('pull_games')
    # print(123)
