# myproject/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagementSystem.settings')

# Создаем объект Celery
app = Celery('StudentManagementSystem')

# Используем настройки из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи в приложениях
app.autodiscover_tasks()

