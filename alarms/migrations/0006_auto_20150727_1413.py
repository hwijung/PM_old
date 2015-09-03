# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarms', '0005_auto_20150726_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='title',
            field=models.SlugField(unique=True, max_length=32),
        ),
    ]
