# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wname', models.CharField(max_length=20)),
                ('wchuohao', models.CharField(max_length=20)),
                ('wjianjie', tinymce.models.HTMLField()),
                ('wshiji', models.CharField(max_length=100)),
                ('wsex', models.IntegerField()),
                ('wpic', models.ImageField(upload_to=b'df_work')),
                ('whobby', models.CharField(max_length=100)),
                ('wdanshen', models.BooleanField(default=True)),
            ],
        ),
    ]
