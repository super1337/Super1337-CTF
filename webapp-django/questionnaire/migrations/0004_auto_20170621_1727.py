# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 17:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0003_auto_20170621_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 21, 17, 27, 8, 12759, tzinfo=utc), editable=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 21, 17, 27, 8, 12801, tzinfo=utc), editable=False),
        ),
    ]
