import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emailsender.settings')

app = Celery('emailsender')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
