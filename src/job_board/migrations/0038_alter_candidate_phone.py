# Generated by Django 3.2.5 on 2021-08-09 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_board', '0037_alter_jobadditionalfield_validation_regx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='phone',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
