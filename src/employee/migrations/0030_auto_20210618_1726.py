# Generated by Django 3.2.4 on 2021-06-18 11:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0029_auto_20210618_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='resignation',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 6, 18, 11, 26, 1, 539550, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employee',
            name='joining_date',
            field=models.DateField(default=datetime.datetime(2021, 6, 18, 11, 26, 1, 537075, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='resignation',
            name='status',
            field=models.CharField(choices=[('pending', '⏳ Pending'), ('approved', '✔ Approved'), ('rejected', '⛔ Rejected')], default='pending', max_length=25),
        ),
        migrations.AlterField(
            model_name='salaryhistory',
            name='active_from',
            field=models.DateField(default=datetime.datetime(2021, 6, 18, 11, 26, 1, 537660, tzinfo=utc)),
        ),
    ]
