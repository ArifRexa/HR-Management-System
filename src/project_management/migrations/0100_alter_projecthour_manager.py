# Generated by Django 3.2.8 on 2023-05-25 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0165_auto_20230525_1750'),
        ('project_management', '0099_alter_dailyprojectupdate_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecthour',
            name='manager',
            field=models.ForeignKey(limit_choices_to=models.Q(('active', True), models.Q(('manager', True), ('lead', True), _connector='OR')), on_delete=django.db.models.deletion.CASCADE, to='employee.employee'),
        ),
    ]
