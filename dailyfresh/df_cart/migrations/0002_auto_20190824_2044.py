# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartinfo',
            name='ctoun',
        ),
        migrations.AddField(
            model_name='cartinfo',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
