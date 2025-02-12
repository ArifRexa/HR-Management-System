# Generated by Django 3.2.8 on 2024-06-03 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0245_bookconferenceroom_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookconferenceroom',
            name='manager_or_lead',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='employee.employee'),
        ),
        migrations.AlterField(
            model_name='employeerating',
            name='month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June')], default=6),
        ),
    ]
