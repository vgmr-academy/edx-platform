# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_userpreprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpreprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='userpreprofile',
            name='email',
            field=models.CharField(db_index=True, max_length=255, blank=True),
        ),
    ]
