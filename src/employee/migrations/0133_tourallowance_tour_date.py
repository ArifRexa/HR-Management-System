# Generated by Django 3.2.8 on 2023-02-22 12:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0132_tourallowance'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourallowance',
            name='tour_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
