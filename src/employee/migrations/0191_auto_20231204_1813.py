# Generated by Django 3.2.8 on 2023-12-04 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0190_auto_20231204_1534'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employeeexperttech',
            options={'ordering': ('technology__name',), 'verbose_name': 'Employee Expert Tech', 'verbose_name_plural': 'Employee Expert Techs'},
        ),
        migrations.RemoveField(
            model_name='employeeexpertise',
            name='technology_level',
        ),
        migrations.AddField(
            model_name='employeeexpertise',
            name='technology_level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='technology_level', to='employee.employeeexperttech', verbose_name='Expertise Tech'),
        ),
        migrations.AlterUniqueTogether(
            name='employeeexperttech',
            unique_together={('technology', 'level')},
        ),
    ]
