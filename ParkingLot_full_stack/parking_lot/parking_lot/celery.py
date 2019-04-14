from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from .settings import host_role, host_num
import sys
import inspect
from celery.concurrency import asynpool

asynpool.PROC_ALIVE_TIMEOUT = 100.0  # set this long enough

# 识别不到 parking_lot.HyperLPR.tasks 只能这样了
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
hyperLPR_path = os.path.join(parent_dir, 'HyperLPR')
sys.path.insert(0, hyperLPR_path)

from tasks import indoorCameraRecognize # noqa
from tasks import outdoorCameraRecognize # noqa

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
    print(host_role)
    if host_role and host_role.endswith('camera'):
        print('开启摄像头车牌识别定时任务')
        if host_role.startswith('indoor'):
            sender.add_periodic_task(2.0, indoorCameraRecognize.s(host_num))
        elif host_role.startswith('outdoor'):
            sender.add_periodic_task(2.0, outdoorCameraRecognize.s(host_num))
    else:
        print('当前结点为核心服务器, 不启用车牌识别任务')


# bind=True to refer to the current task instance
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
