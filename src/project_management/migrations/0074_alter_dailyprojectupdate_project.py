# Generated by Django 3.2.8 on 2023-03-14 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0073_dailypprojectupdategroupbyproject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyprojectupdate',
            name='project',
            field=models.ForeignKey(limit_choices_to={'active': True}, on_delete=django.db.models.deletion.RESTRICT, related_name='projects', to='project_management.project'),
        ),
    ]
