# Generated by Django 3.2.8 on 2023-02-08 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0060_alter_dailyprojectupdate_hours'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailyprojectupdate',
            name='description',
        ),
    ]
