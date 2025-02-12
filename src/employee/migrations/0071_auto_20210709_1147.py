# Generated by Django 3.2.5 on 2021-07-09 05:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0070_auto_20210708_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='joining_date',
            field=models.DateField(default=datetime.datetime(2021, 7, 9, 5, 46, 13, 260876, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='resignation',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 9, 5, 46, 13, 265356, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salaryhistory',
            name='active_from',
            field=models.DateField(default=datetime.datetime(2021, 7, 9, 5, 46, 13, 261626, tzinfo=utc)),
        ),
    ]
