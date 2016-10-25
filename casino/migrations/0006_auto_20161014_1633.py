# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-14 13:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('casino', '0005_bet_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='creation_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 14, 13, 33, 4, 939000, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='bet',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 14, 13, 33, 4, 939000, tzinfo=utc)),
        ),
    ]