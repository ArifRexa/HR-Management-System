# Generated by Django 3.2.8 on 2024-01-19 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0107_remove_accountjournal_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountjournal',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
