# Generated by Django 4.1.3 on 2022-12-05 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0113_alter_employeeactivity_end_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='lunch_allowance',
            field=models.BooleanField(default=True),
        ),
    ]
