# Generated by Django 3.2.8 on 2024-04-02 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0138_auto_20240401_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='designation',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
