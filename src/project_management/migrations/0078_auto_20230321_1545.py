# Generated by Django 3.2.8 on 2023-03-21 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0077_merge_20230316_1250'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projecthour',
            options={'permissions': [('show_all_hours', 'Can show all hours just like admin'), ('select_hour_type', 'Can select Project Hour type'), ('cto_approved_hour', 'Can approved and give feedback from CTO')], 'verbose_name_plural': 'Weekly Project Hours'},
        ),
        migrations.AddField(
            model_name='projecthour',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='projecthour',
            name='cto_feedback',
            field=models.TextField(blank=True, null=True),
        ),
    ]
