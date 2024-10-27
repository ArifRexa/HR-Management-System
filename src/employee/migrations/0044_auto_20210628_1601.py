# Generated by Django 3.2.4 on 2021-06-28 10:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0043_auto_20210628_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='joining_date',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 10, 1, 50, 558048, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='resignation',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 10, 1, 50, 560566, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salaryhistory',
            name='active_from',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 10, 1, 50, 558639, tzinfo=utc)),
        ),
    ]
