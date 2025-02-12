# Generated by Django 3.2 on 2021-06-10 15:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0018_auto_20210610_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='payable_salary',
        ),
        migrations.AlterField(
            model_name='employee',
            name='joining_date',
            field=models.DateField(default=datetime.datetime(2021, 6, 10, 15, 10, 2, 375758, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salaryhistory',
            name='active_from',
            field=models.DateField(default=datetime.datetime(2021, 6, 10, 15, 10, 2, 376344, tzinfo=utc)),
        ),
    ]
