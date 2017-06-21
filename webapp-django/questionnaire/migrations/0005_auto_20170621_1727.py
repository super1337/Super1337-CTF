# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 17:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0004_auto_20170621_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='modified',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
