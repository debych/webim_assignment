import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webim.settings')

app = Celery('webim')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-number-every-5-sec': {
        'task': 'main.tasks.UpdateRandomNumber',
        'schedule': 5.0,
    },
}