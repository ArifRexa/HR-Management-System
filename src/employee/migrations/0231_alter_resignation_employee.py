# Generated by Django 3.2.8 on 2024-02-19 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0230_merge_20240213_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resignation',
            name='employee',
            field=models.ForeignKey(limit_choices_to={'active': True, 'user__is_superuser': False}, on_delete=django.db.models.deletion.CASCADE, to='employee.employee'),
        ),
    ]
