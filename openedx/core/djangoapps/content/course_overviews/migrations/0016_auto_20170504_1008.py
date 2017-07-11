# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0015_auto_20170504_0854'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseoverview',
            old_name='category',
            new_name='categ',
        ),
    ]
