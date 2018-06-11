# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0013_userprofile_tma_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='tma_token',
            field=models.CharField(default=b'518d6cc0e709ba1651d53b9661bf91d104c60985757d7c4e4346ed47b7f8ec02564fbabe63e2f309a52a91d53e79f22ff85f9311954c7757506c5e07009c4d90fb609772ae1afc652a241e3d98823bc5', max_length=255, db_index=True, blank=True),
        ),
    ]
