# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-29 11:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0026_auto_20170829_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='by_id',
        ),
        migrations.RemoveField(
            model_name='post_comments',
            name='by_id',
        ),
        migrations.RemoveField(
            model_name='post_comments',
            name='of_post_id',
        ),
        migrations.RemoveField(
            model_name='post_images',
            name='of_post_id',
        ),
        migrations.RemoveField(
            model_name='post_like',
            name='by_id',
        ),
        migrations.RemoveField(
            model_name='post_like',
            name='of_post_id',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Post_comments',
        ),
        migrations.DeleteModel(
            name='Post_images',
        ),
        migrations.DeleteModel(
            name='Post_like',
        ),
    ]