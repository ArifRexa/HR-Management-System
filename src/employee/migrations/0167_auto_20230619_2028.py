# Generated by Django 3.2.8 on 2023-06-19 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0166_alter_employeelunch_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bankaccount',
            options={'permissions': (('can_edit_all_bank_account', 'Can edit all bank account'), ('can_approve_bank_account_info', 'Can approve bank account info'))},
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='is_approved',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='cto_email',
            field=models.TextField(null=True, verbose_name='Tech Lead Alert Emails'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='need_cto',
            field=models.BooleanField(default=False, verbose_name='I need help from Tech Lead'),
        ),
    ]
