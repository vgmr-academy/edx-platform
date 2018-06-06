# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microsite_configuration', '0002_auto_20160202_0228'),
        ('third_party_auth', '0005_add_site_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='MicrositesCredentials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('VM_status', models.CharField(max_length=255, db_index=True)),
                ('logout_uri', models.CharField(max_length=3000, db_index=True)),
                ('client_id', models.CharField(max_length=255, db_index=True)),
                ('client_secret', models.CharField(max_length=255, db_index=True)),
                ('microsite', models.ForeignKey(to='microsite_configuration.Microsite')),
            ],
        ),
    ]
