# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarms', '0006_auto_20150727_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='site',
            field=models.URLField(max_length=512),
        ),
    ]
