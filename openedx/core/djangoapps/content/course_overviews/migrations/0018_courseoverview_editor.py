# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0017_auto_20170504_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseoverview',
            name='editor',
            field=models.TextField(default=b'None'),
        ),
    ]
