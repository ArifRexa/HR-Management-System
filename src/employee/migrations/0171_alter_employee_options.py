# Generated by Django 3.2.8 on 2023-08-04 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0170_employee_device_allowance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'permissions': (('can_see_formal_summery_view', 'Can able to see emloyee summary view'), ('can_access_all_employee', 'Can acccess all employee'))},
        ),
    ]
