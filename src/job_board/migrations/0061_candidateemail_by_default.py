# Generated by Django 3.2.8 on 2024-02-22 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_board', '0060_candidateemail_candidateemailattatchment'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateemail',
            name='by_default',
            field=models.BooleanField(default=False),
        ),
    ]
