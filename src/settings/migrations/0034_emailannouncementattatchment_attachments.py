# Generated by Django 3.2.8 on 2024-02-08 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0033_auto_20240208_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailannouncementattatchment',
            name='attachments',
            field=models.FileField(blank=True, null=True, upload_to='email_attachments/'),
        ),
    ]
