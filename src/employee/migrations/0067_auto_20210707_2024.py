# Generated by Django 3.2.5 on 2021-07-07 14:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0066_auto_20210706_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='joining_date',
            field=models.DateField(default=datetime.datetime(2021, 7, 7, 14, 24, 31, 399438, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='resignation',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 7, 14, 24, 31, 403999, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salaryhistory',
            name='active_from',
            field=models.DateField(default=datetime.datetime(2021, 7, 7, 14, 24, 31, 400265, tzinfo=utc)),
        ),
    ]
