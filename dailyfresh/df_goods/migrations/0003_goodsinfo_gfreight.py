# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0002_auto_20170405_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsinfo',
            name='gfreight',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
