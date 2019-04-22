# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.db import migrations
from django.contrib.auth.admin import User


def create_superuser(apps, schema_editor):
    """
    在 django migrations 的时候, 自动创建两个用户
    DCMMC: 仅用于测试
    """
    if not User.objects.filter(username='admin').exists():
        superuser = User()
        superuser.is_active = True
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.username = 'admin'
        superuser.email = 'xwt97294597@gmail.com'
        superuser.set_password('admin666')
        superuser.save()
    if not User.objects.filter(username='17775110118').exists():
        user = User()
        user.is_active = True
        user.is_superuser = False
        user.is_staff = False
        user.username = '17775110118'
        user.set_password('97294597')
        user.email = 'xwt97294597@gmail.com'
        user.save()


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_superuser)
    ]

