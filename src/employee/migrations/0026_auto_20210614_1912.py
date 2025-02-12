# Generated by Django 3.2 on 2021-06-14 13:12

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('settings', '0007_alter_publicholidaydate_public_holiday'),
        ('employee', '0025_auto_20210614_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='joining_date',
            field=models.DateField(default=datetime.datetime(2021, 6, 14, 13, 12, 38, 276604, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employee',
            name='leave_management',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settings.leavemanagement'),
        ),
        migrations.AlterField(
            model_name='salaryhistory',
            name='active_from',
            field=models.DateField(default=datetime.datetime(2021, 6, 14, 13, 12, 38, 277274, tzinfo=utc)),
        ),
    ]
