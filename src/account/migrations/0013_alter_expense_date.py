# Generated by Django 3.2.4 on 2021-06-26 07:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_expense_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 6, 26, 7, 11, 56, 769945, tzinfo=utc)),
        ),
    ]
