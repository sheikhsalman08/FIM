# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-29 10:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_auto_20170829_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='by',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]