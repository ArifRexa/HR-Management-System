# Generated by Django 3.2 on 2021-07-06 14:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0044_auto_20210706_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 6, 14, 12, 31, 701536, tzinfo=utc)),
        ),
    ]
