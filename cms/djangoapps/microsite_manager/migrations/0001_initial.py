# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MicrositeDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=250)),
                ('logo', models.CharField(max_length=250)),
                ('language_code', models.CharField(max_length=250)),
                ('color_code', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Microsite Details',
                'verbose_name_plural': 'Microsite Details',
            },
        ),
    ]
