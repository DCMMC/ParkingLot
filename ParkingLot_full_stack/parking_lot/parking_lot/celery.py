from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from parking_lot.HyperLPR.tasks import indoorCameraRecognize
from parking_lot.HyperLPR.tasks import outdoorCameraRecognize
from .settings import host_role, host_num

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_lot.settings')

app = Celery('parking_lot')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls indoorCameraRecognize every 1 seconds.
    # `.s()` 函数是 Signature 的简称, 也就是调用 Celery 任务
    if host_role and host_role != 'core':
        if host_role.startswith('indoor'):
            sender.add_periodic_task(1.0, indoorCameraRecognize.s(host_num))
        elif host_role.startswith('outdoor'):
            sender.add_periodic_task(1.0, outdoorCameraRecognize.s(host_num))
    else:
        print('当前结点为核心服务器, 不启用车牌识别任务')


# bind=True to refer to the current task instance
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
