# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('course_creators', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecreator',
            name='note',
            field=models.CharField(help_text="Commentaires optionnels pour cet utilisateur (par exemple, pourquoi l'acc\xe8s \xe0 la cr\xe9ation de cours a \xe9t\xe9 refus\xe9)", max_length=512, blank=True),
        ),
        migrations.AlterField(
            model_name='coursecreator',
            name='state',
            field=models.CharField(default=b'unrequested', help_text='\xc9tat actuel du cr\xe9ateur du cours', max_length=24, choices=[(b'unrequested', 'non demand\xe9'), (b'pending', 'en attente'), (b'granted', 'autoris\xe9'), (b'denied', 'refus\xe9')]),
        ),
        migrations.AlterField(
            model_name='coursecreator',
            name='state_changed',
            field=models.DateTimeField(help_text="Date de la derni\xe8re modification de l'\xe9tat", verbose_name=b'state last updated', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='coursecreator',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, help_text='Utilisateur de Studio'),
        ),
    ]
