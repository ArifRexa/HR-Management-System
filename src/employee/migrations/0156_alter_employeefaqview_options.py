# Generated by Django 3.2.8 on 2023-04-14 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0155_alter_config_cto_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employeefaqview',
            options={'permissions': (('employee_faqs_view', 'Can Employee FAQ list view.'),), 'verbose_name': 'FAQ List', 'verbose_name_plural': 'FAQ List'},
        ),
    ]
