# Generated by Django 3.2.5 on 2021-07-02 11:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_alter_expense_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 2, 11, 54, 49, 276483, tzinfo=utc)),
        ),
    ]
