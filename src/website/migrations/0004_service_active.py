# Generated by Django 4.0.2 on 2022-03-29 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_service_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
