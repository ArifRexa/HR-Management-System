# Generated by Django 3.2.8 on 2023-03-09 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0141_merge_20230309_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='skip_lunch_amount',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Number of lunch skipp from salary'),
        ),
    ]
