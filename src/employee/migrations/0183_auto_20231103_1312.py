# Generated by Django 3.2.8 on 2023-11-03 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0182_alter_employeeneedhelp_need_help_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='present_address',
            field=models.TextField(null=True, verbose_name='Present Address'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.TextField(null=True, verbose_name='Permanent Address'),
        ),
    ]
