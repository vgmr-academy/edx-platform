# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('microsite_manager', '0006_auto_20170907_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='micrositeadminmanager',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
