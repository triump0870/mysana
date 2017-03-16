from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from kombu import Exchange, Queue

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysana.settings.development')

app = Celery('mysana', broker=settings.BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_DEFAULT_QUEUE='mysana',
    CELERY_QUEUES=(
        Queue('mysana', Exchange('mysana'), routing_key='mysana'),
    ),
    CELERYBEAT_SCHEDULE={
        'notification-every-day-morning': {
            'task': 'goals.tasks.daily_notification',
            'schedule': crontab(hour=9, minute=0)
        },
    },
    CELERY_TIMEZONE='India/Kolkata',
    CELERY_ACCEPT_CONTENT=['application/json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json'
)
