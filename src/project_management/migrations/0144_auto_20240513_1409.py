# Generated by Django 3.2.8 on 2024-05-13 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0143_auto_20240506_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='industries',
            field=models.ManyToManyField(blank=True, related_name='projects', to='project_management.ProjectIndustry'),
        ),
        migrations.AlterField(
            model_name='project',
            name='platforms',
            field=models.ManyToManyField(blank=True, related_name='projects', to='project_management.ProjectPlatform'),
        ),
        migrations.AlterField(
            model_name='project',
            name='services',
            field=models.ManyToManyField(blank=True, related_name='projects', to='project_management.ProjectService'),
        ),
    ]
