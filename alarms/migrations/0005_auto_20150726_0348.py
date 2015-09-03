# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('alarms', '0004_auto_20150726_0305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='title',
            field=models.CharField(unique=True, max_length=32, validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z]*$', b'Only alphanumeric characters are allowed.')]),
        ),
    ]
