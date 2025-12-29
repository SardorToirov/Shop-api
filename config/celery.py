import os
from celery import Celery

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Celery app nomi (PROJECT NOMI)
app = Celery('config')

# Celery config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks.py
app.autodiscover_tasks()
