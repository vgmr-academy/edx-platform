# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0012_courseoverview_content_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseoverview',
            name='grading_note',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='courseoverview',
            name='is_graded',
            field=models.BooleanField(default=True),
        ),
    ]
