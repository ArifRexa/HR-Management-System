# Generated by Django 3.2.8 on 2024-03-18 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0127_auto_20240314_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_key_feature',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='project_management.projectkeyfeature'),
        ),
    ]
