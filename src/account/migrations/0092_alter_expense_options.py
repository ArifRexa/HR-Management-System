# Generated by Django 3.2.8 on 2023-02-03 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0091_expense_is_approved'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'permissions': (('can_approve_expense', 'Can Approve Expense'),)},
        ),
    ]
