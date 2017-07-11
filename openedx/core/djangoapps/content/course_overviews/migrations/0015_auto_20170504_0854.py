# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0014_auto_20170503_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseoverview',
            name='grading_note',
        ),
        migrations.AddField(
            model_name='courseoverview',
            name='category',
            field=models.TextField(default=None),
        ),
    ]
