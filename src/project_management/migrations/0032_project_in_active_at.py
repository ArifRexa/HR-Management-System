# Generated by Django 4.0.2 on 2022-09-05 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0031_tag_project_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='in_active_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
