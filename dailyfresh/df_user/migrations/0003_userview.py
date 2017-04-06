# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0002_auto_20170405_2214'),
        ('df_user', '0002_auto_20170403_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gid', models.ForeignKey(to='df_goods.GoodsInfo')),
                ('uid', models.ForeignKey(to='df_user.UserInfo')),
            ],
        ),
    ]
