# Generated by Django 3.2.8 on 2024-04-01 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0237_alter_observation_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeerating',
            name='month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April')], default=4),
        ),
    ]
