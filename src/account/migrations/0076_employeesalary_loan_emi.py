# Generated by Django 3.2.5 on 2021-10-01 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0075_loan_effective_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeesalary',
            name='loan_emi',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
