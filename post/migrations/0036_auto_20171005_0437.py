# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0035_auto_20170905_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_down',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='post_up',
            field=models.IntegerField(default=0),
        ),
    ]
