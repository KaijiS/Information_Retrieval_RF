# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-18 17:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_auto_20171019_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Title'),
        ),
    ]
