# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0005_auto_20170503_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditconfig',
            name='cache_ttl',
            field=models.PositiveIntegerField(default=0, help_text='Indiqu\xe9s en secondes. Active la mise en cache en r\xe9glant \xe0 une valeur plus grande que 0.', verbose_name='Time To Live de la Cache'),
        ),
    ]
