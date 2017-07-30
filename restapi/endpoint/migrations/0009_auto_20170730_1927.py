# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-30 09:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoint', '0008_auto_20170730_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='angry',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='recording',
            name='fear',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='recording',
            name='happy',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='recording',
            name='neutral',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='recording',
            name='sad',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
    ]
