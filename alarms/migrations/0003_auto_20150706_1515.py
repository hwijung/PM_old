# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alarms', '0002_settings_activated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=32)),
                ('site', models.CharField(max_length=512)),
                ('activated', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activated', models.IntegerField(default=1)),
                ('noti_email', models.BooleanField(default=True)),
                ('noti_SMS', models.BooleanField(default=False)),
                ('noti_push', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='SearchWords',
            new_name='SearchWord',
        ),
        migrations.RemoveField(
            model_name='alarms',
            name='user',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='user',
        ),
        migrations.AlterField(
            model_name='searchword',
            name='alarms',
            field=models.ManyToManyField(to='alarms.Alarm'),
        ),
        migrations.DeleteModel(
            name='Alarms',
        ),
        migrations.DeleteModel(
            name='Settings',
        ),
    ]
