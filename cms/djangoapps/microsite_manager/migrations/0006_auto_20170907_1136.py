# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microsite_manager', '0005_micrositeadminmanager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='micrositeadminmanager',
            name='microsite',
            field=models.ForeignKey(to='microsite_configuration.Microsite'),
        ),
    ]
