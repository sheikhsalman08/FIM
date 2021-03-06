# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-30 11:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_post_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField(default=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('by_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner+', to=settings.AUTH_USER_MODEL)),
                ('of_post_id', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='like of post +', to='users.Post')),
            ],
        ),
    ]
