# Generated by Django 4.1.4 on 2022-12-22 18:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0046_alter_projecttoken_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttoken',
            name='token',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
