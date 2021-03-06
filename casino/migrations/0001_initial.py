# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-08 11:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(editable=False)),
                ('last_modified', models.DateTimeField()),
                ('res', models.CharField(choices=[('1', 'HOME_WIN'), ('X', 'TIE'), ('2', 'AWAY_WIN')], max_length=1)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('home_team', models.CharField(max_length=40)),
                ('away_team', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='bet',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='casino.Competition'),
        ),
    ]
