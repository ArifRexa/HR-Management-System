# Generated by Django 3.2.8 on 2024-01-31 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0211_hrpolicy_policy_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hrpolicy',
            name='policy_file',
            field=models.FileField(default='', upload_to='src/media/'),
        ),
    ]
