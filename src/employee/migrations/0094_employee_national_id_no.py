# Generated by Django 3.2.6 on 2021-09-29 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0093_alter_leave_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='national_id_no',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
