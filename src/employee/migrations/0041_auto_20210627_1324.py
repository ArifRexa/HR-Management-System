# Generated by Django 3.2.4 on 2021-06-27 07:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0040_auto_20210627_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='joining_date',
            field=models.DateField(default=datetime.datetime(2021, 6, 27, 7, 23, 54, 189445, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='resignation',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 6, 27, 7, 23, 54, 189445, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salaryhistory',
            name='active_from',
            field=models.DateField(default=datetime.datetime(2021, 6, 27, 7, 23, 54, 189445, tzinfo=utc)),
        ),
    ]
