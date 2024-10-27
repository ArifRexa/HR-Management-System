# Generated by Django 3.2.8 on 2023-11-24 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0185_auto_20231121_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='status',
            field=models.CharField(choices=[('pending', '⏳ Pending'), ('approved', '✅ Approved'), ('rejected', '⛔ Rejected')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='leavemanagement',
            name='status',
            field=models.CharField(choices=[('pending', '⏳ Pending'), ('approved', '✅ Approved'), ('rejected', '⛔ Rejected')], default='pending', max_length=20),
        ),
    ]
