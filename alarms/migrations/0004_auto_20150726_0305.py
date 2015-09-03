# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarms', '0003_auto_20150706_1515'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Sites',
            new_name='Site',
        ),
    ]
