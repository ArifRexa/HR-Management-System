# Generated by Django 3.2.8 on 2023-08-25 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset_management', '0021_auto_20230816_1425'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='credential',
            options={'permissions': [('access_all_credentials', 'Can able to see all credentials'), ('can_edit_credential', 'Can edit credential')]},
        ),
    ]
