# Generated by Django 3.2.8 on 2024-03-14 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0125_projectchallenges_projectdesign_projectkeyfeature_projectoverview_projectsolution_projectstatement'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_challenges',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='project_management.projectchallenges'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_design',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='project_management.projectdesign'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_key_feature',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='project_management.projectkeyfeature'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_overview',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='project_management.projectoverview'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_solution',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='project_management.projectsolution'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_statement',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='project_management.projectstatement'),
        ),
    ]
