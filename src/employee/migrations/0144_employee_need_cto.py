# Generated by Django 3.2.8 on 2023-03-29 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0143_alter_commentagainstemployeefeedback_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='need_cto',
            field=models.BooleanField(default=False, verbose_name='I need help from CTO'),
        ),
    ]
