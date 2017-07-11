# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0016_auto_20170504_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseoverview',
            name='categ',
            field=models.TextField(default=b'None'),
        ),
    ]
