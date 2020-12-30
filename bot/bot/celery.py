from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Setting the Default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot.settings')

app = Celery('bot')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'backend_cleanup': {
        'task': 'celery.backend_cleanup',
        'schedule': 600,  # 10 minutes
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
