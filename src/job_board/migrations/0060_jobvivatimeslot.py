# Generated by Django 3.2.8 on 2024-02-23 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job_board', '0059_alter_candidateassessment_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobVivaTimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_post', models.CharField(choices=[('junior', 'Junior'), ('senior', 'Senior'), ('intern', 'Intern')], max_length=20)),
                ('duration', models.PositiveIntegerField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('date', models.DateField()),
                ('candidate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='job_board.candidate')),
            ],
        ),
    ]
