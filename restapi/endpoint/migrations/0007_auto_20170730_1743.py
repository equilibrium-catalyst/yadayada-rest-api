# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-30 07:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0006_auto_20170730_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recording',
            name='emotions',
        ),
        migrations.AddField(
            model_name='recording',
            name='angry',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='recording',
            name='fear',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='recording',
            name='happy',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='recording',
            name='neutral',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='recording',
            name='sad',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='recording',
            name='transcript',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]