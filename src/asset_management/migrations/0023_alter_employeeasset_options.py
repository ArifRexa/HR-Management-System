# Generated by Django 3.2.8 on 2023-12-01 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset_management', '0022_alter_credential_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employeeasset',
            options={'verbose_name': 'Employee Asset', 'verbose_name_plural': 'Employee Assets'},
        ),
    ]
