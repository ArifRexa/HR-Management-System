# Generated by Django 3.2.4 on 2021-06-28 09:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0041_auto_20210627_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='joining_date',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 9, 59, 55, 753010, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='resignation',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 9, 59, 55, 755553, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salaryhistory',
            name='active_from',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 9, 59, 55, 753586, tzinfo=utc)),
        ),
    ]
