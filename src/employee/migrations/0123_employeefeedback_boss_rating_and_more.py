# Generated by Django 4.1.4 on 2022-12-19 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0122_auto_20221216_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeefeedback',
            name='boss_rating',
            field=models.FloatField(default=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeefeedback',
            name='happiness_index_rating',
            field=models.FloatField(default=3),
            preserve_default=False,
        ),
    ]
