# Generated by Django 3.2.5 on 2021-08-09 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0090_auto_20210803_0232'),
        ('project_management', '0010_alter_employeeprojecthour_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprojecthour',
            name='employee',
            field=models.ForeignKey(limit_choices_to={'active': True, 'manager': False}, on_delete=django.db.models.deletion.RESTRICT, to='employee.employee'),
        ),
    ]
