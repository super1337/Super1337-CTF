# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0008_auto_20170625_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='tags',
            field=models.ManyToManyField(blank=True, to='questionnaire.Tag'),
        ),
    ]