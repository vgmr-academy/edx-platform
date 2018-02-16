# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('microsite_configuration', '0002_auto_20160202_0228'),
        ('microsite_manager', '0004_auto_20170324_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='MicrositeAdminManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('microsite', models.OneToOneField(related_name='microsite_admin', to='microsite_configuration.Microsite')),
                ('user', models.OneToOneField(related_name='microsite_admin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'microsite_admin_manager',
            },
        ),
    ]
