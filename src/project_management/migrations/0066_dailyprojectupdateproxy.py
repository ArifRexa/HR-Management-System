# Generated by Django 3.2.8 on 2023-02-28 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0065_alter_projecthour_forcast'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyProjectUpdateProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('project_management.dailyprojectupdate',),
        ),
    ]
