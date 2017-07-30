# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-30 07:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0004_remove_recording_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='filename',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='recording',
            name='hashtags',
            field=models.ManyToManyField(blank=True, to='endpoint.Hashtag'),
        ),
    ]