# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys
import gc

from celery import Celery
from celery.signals import task_postrun

dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
appname = os.path.basename(dirname)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{appname}.settings.settings')

from django.conf import settings

app = Celery(appname)

settings.CELERYBEAT_SCHEDULER = 'beatx.schedulers.Scheduler'
settings.beatx_store = settings.REDIS_URL
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.LOCAL_APPS + settings.APPS)


# See https://groups.google.com/d/msg/celery-users/jVc3I3kPtlw/fPfnoP_DhuoJ
@task_postrun.connect
def collect_after_task(**kwargs):
    gc.collect()
