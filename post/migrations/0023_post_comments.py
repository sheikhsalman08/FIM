# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-29 11:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0022_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(blank=True, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('visibility_by_admin', models.BooleanField(default=True)),
                ('by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner+', to=settings.AUTH_USER_MODEL)),
                ('of_post_id', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='comment of post +', to='post.Post')),
            ],
        ),
    ]
