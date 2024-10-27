# Generated by Django 3.2.8 on 2024-03-11 13:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0117_auto_20240308_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensegroup',
            name='tds_rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='expensegroup',
            name='vds_rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
