# Generated by Django 3.2.8 on 2024-04-03 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0030_ourachievement'),
    ]

    operations = [
        migrations.CreateModel(
            name='OurJourney',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
    ]
