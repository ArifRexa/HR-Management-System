# Generated by Django 3.2.8 on 2024-01-25 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0023_merge_20240122_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
