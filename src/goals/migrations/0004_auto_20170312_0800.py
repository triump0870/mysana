# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-12 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0003_auto_20170310_2039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subgoal',
            name='goal',
        ),
        migrations.AddField(
            model_name='goal',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Subgoal',
        ),
    ]