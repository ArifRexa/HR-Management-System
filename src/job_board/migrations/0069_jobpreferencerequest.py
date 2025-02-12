# Generated by Django 3.2.8 on 2024-04-04 13:51

from django.db import migrations, models
import job_board.models.candidate


class Migration(migrations.Migration):

    dependencies = [
        ('job_board', '0068_merge_20240308_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPreferenceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('preferred_designation', models.CharField(max_length=100)),
                ('cv', models.FileField(upload_to=job_board.models.candidate.candidate_email_path, validators=[job_board.models.candidate.validate_file_extension])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
