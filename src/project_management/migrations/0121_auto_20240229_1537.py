# Generated by Django 3.2.8 on 2024-02-29 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0120_alter_enabledailyupdatenow_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='enabledailyupdatenow',
            name='name',
            field=models.CharField(default='config', max_length=24),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='enabledailyupdatenow',
            name='last_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
