# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_order', '0002_auto_20170407_2337'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderinfo',
            old_name='isPlay',
            new_name='isPay',
        ),
    ]
