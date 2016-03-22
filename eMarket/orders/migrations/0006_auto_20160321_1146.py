# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20160321_1142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraddress',
            old_name='add_type',
            new_name='addr_type',
        ),
    ]
