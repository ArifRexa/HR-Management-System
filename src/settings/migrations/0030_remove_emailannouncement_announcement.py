# Generated by Django 3.2.8 on 2024-02-08 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0029_emailannouncement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailannouncement',
            name='announcement',
        ),
    ]
