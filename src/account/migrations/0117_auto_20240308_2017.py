# Generated by Django 3.2.8 on 2024-03-08 20:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0116_merge_0115_auto_20240131_1740_0115_auto_20240131_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensegroup',
            name='tds_rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='expensegroup',
            name='vds_rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
