# Generated by Django 3.2.8 on 2024-06-03 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0246_auto_20240603_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookconferenceroom',
            name='end_time',
        ),
        migrations.AlterField(
            model_name='bookconferenceroom',
            name='manager_or_lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee'),
        ),
    ]
