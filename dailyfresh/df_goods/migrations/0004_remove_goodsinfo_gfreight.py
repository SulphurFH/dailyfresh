# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0003_goodsinfo_gfreight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodsinfo',
            name='gfreight',
        ),
    ]
