# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0011_courseoverview_is_required_atp'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseoverview',
            name='content_data',
            field=models.TextField(default={b'webzine': False, b'document_pdf': False, b'quiz': False, b'video': False, b'serious_game': False, b'text_image': False}),
        ),
    ]
