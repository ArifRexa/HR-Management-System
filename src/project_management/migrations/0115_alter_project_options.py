# Generated by Django 3.2.8 on 2023-12-01 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0114_alter_projectreport_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['title']},
        ),
    ]
