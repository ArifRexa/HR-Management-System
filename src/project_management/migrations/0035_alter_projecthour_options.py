# Generated by Django 4.1.3 on 2022-11-11 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0034_alter_projecthour_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projecthour',
            options={'permissions': [('show_all_hours', 'Can show all hours just like admin')]},
        ),
    ]
