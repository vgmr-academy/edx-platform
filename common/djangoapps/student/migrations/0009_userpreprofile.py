# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0008_auto_20161117_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreprofile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level_1', models.CharField(db_index=True, max_length=255, blank=True)),
                ('level_2', models.CharField(db_index=True, max_length=255, blank=True)),
                ('level_3', models.CharField(db_index=True, max_length=255, blank=True)),
                ('level_4', models.CharField(db_index=True, max_length=255, blank=True)),
                ('user', models.OneToOneField(related_name='preprofile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'auth_user_preprofile',
            },
        ),
    ]
