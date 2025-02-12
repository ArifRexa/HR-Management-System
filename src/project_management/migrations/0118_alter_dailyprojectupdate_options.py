# Generated by Django 3.2.8 on 2024-02-13 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0117_merge_0116_auto_20231204_1458_0116_auto_20231207_1553'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dailyprojectupdate',
            options={'permissions': [('see_all_employee_update', 'Can see all daily update'), ('can_approve_or_edit_daily_update_at_any_time', 'Can approve or update daily project update at any time')], 'verbose_name': 'Daily Project Update', 'verbose_name_plural': 'Daily Project Updates'},
        ),
    ]
