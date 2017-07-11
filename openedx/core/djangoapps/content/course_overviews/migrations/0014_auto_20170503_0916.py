# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0013_auto_20170503_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseoverview',
            name='grading_note',
            field=models.IntegerField(default=60),
        ),
    ]
