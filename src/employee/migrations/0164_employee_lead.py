# Generated by Django 3.2.8 on 2023-05-25 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0163_learning'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='lead',
            field=models.BooleanField(default=False),
        ),
    ]
