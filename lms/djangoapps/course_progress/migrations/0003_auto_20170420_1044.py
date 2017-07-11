# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openedx.core.djangoapps.xmodule_django.models


class Migration(migrations.Migration):

    dependencies = [
        ('course_progress', '0002_studentcourseprogress'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studenthistory',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='studenthistory',
            name='student',
        ),
        migrations.AlterField(
            model_name='studentcourseprogress',
            name='course_id',
            field=openedx.core.djangoapps.xmodule_django.models.CourseKeyField(max_length=255, verbose_name=b'Course ID', db_index=True),
        ),
        migrations.AlterUniqueTogether(
            name='studentcourseprogress',
            unique_together=set([('student', 'course_id')]),
        ),
        migrations.DeleteModel(
            name='StudentHistory',
        ),
    ]
