# Generated by Django 3.2.4 on 2021-06-28 14:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_alter_expense_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 14, 45, 59, 526302, tzinfo=utc)),
        ),
    ]
