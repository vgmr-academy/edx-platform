# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0014_auto_20170504_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditconfig',
            name='cache_ttl',
            field=models.PositiveIntegerField(default=0, help_text='Specified in seconds. Enable caching by setting this to a value greater than 0.', verbose_name='Cache Time To Live'),
        ),
    ]
