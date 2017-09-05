# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-30 10:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0028_post_post_comments_post_images_post_like'),
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
