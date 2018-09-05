# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_userpreprofile_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreprofile',
            name='last_invite',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
