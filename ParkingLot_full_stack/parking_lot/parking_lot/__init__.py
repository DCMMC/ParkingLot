from __future__ import absolute_import, unicode_literals
from .settings import host_role

if host_role != 'core':
    # This will make sure the app is always imported when
    # Django starts so that shared_task will use this app.
    from .celery import app as celery_app
    # print('Start Celery with Django')

    __all__ = ('celery_app',)
