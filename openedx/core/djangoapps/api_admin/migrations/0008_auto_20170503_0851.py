# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_admin', '0007_auto_20170420_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiaccessrequest',
            name='status',
            field=models.CharField(default=b'pending', help_text='Status of this API access request', max_length=255, db_index=True, choices=[(b'pending', 'Pending'), (b'denied', 'Denied'), (b'approved', 'Approved')]),
        ),
        migrations.AlterField(
            model_name='historicalapiaccessrequest',
            name='status',
            field=models.CharField(default=b'pending', help_text='Status of this API access request', max_length=255, db_index=True, choices=[(b'pending', 'Pending'), (b'denied', 'Denied'), (b'approved', 'Approved')]),
        ),
    ]
