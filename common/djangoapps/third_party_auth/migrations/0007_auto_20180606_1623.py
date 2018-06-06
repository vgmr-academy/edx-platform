# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('third_party_auth', '0006_micrositescredentials'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='micrositescredentials',
            options={'verbose_name_plural': 'Microsites Credentials'},
        ),
    ]
