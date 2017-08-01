# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microsite_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='micrositedetail',
            name='language_code',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
