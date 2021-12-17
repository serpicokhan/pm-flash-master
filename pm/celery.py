# from __future__ import absolute_import
# import os
# from celery import Celery
# from django.conf import settings
#
# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pm.settings')
# app = Celery('pm')
#
# # Using a string here means the worker will not have to
# # pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pm.settings')
# Set default Django settings os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
app = Celery('pm')
# Celery will apply all configuration keys with defined namespace  app.config_from_object('django.conf:settings', namespace='CELERY')
# Load tasks from all registered apps
# app.autodiscover_tasks()
app.config_from_object('django.conf:settings')
