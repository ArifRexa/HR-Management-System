# Generated by Django 3.2.8 on 2024-05-31 19:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0244_alter_bookconferenceroom_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookconferenceroom',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
