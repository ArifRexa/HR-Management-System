# Generated by Django 3.2.5 on 2021-07-06 07:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0036_alter_expense_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 6, 7, 41, 1, 631118, tzinfo=utc)),
        ),
    ]
