# Generated by Django 3.2.4 on 2021-06-29 10:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_alter_expense_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 6, 29, 10, 0, 43, 233685, tzinfo=utc)),
        ),
    ]
