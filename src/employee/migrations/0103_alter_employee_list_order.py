# Generated by Django 4.0.2 on 2022-08-01 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0102_alter_employee_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='list_order',
            field=models.IntegerField(default=100),
        ),
    ]
