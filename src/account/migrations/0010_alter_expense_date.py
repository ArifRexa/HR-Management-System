# Generated by Django 3.2.4 on 2021-06-26 06:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_expense_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 6, 26, 6, 12, 3, 384338, tzinfo=utc)),
        ),
    ]
