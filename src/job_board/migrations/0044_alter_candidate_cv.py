# Generated by Django 3.2.6 on 2021-09-01 08:50

from django.db import migrations, models
import job_board.models.candidate


class Migration(migrations.Migration):

    dependencies = [
        ('job_board', '0043_auto_20210827_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='cv',
            field=models.FileField(upload_to=job_board.models.candidate.candidate_email_path, validators=[job_board.models.candidate.validate_file_extension]),
        ),
    ]
