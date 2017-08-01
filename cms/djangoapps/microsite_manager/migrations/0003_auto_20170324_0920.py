# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microsite_manager', '0002_auto_20170324_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='micrositedetail',
            name='logo',
            field=models.FileField(upload_to=b''),
        ),
    ]
