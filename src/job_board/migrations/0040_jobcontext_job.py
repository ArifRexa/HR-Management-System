# Generated by Django 3.2.6 on 2021-08-27 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job_board', '0039_jobcontext'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobcontext',
            name='job',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='job_board.job'),
            preserve_default=False,
        ),
    ]
