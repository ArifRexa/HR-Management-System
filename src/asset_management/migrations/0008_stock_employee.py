# Generated by Django 3.2.5 on 2021-09-30 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0094_employee_national_id_no'),
        ('asset_management', '0007_auto_20210930_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='employee',
            field=models.ForeignKey(limit_choices_to={'active': True}, null=True, on_delete=django.db.models.deletion.RESTRICT, to='employee.employee'),
        ),
    ]
