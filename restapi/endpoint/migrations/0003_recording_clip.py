# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-29 08:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0002_auto_20170729_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='clip',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
