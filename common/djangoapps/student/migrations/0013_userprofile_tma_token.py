# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_userpreprofile_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='tma_token',
            field=models.CharField(default=b'1e4e053f605992bf935c97a35b6be81e0308e35e7b550aa88bf50f36984c6b1465f48bf681eaa91fec6829e3fab09996c8b82689fb3ad6978dcd336651271f9f7b9d20e03b2d785755413ad8cf85329b', max_length=80, db_index=True, blank=True),
        ),
    ]
