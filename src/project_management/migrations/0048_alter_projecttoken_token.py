# Generated by Django 4.1.4 on 2022-12-22 19:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0047_alter_projecttoken_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttoken',
            name='token',
            field=models.CharField(default=uuid.uuid4, max_length=255),
        ),
    ]
