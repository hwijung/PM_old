# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarms', '0007_auto_20150727_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='site',
            field=models.TextField(max_length=512),
        ),
    ]
