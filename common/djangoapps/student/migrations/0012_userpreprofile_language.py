# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_auto_20170913_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreprofile',
            name='language',
            field=models.CharField(db_index=True, max_length=255, blank=True),
        ),
    ]
