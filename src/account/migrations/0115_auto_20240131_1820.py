# Generated by Django 3.2.8 on 2024-01-31 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0114_dailypaymentvoucher'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyJournal',
            fields=[
            ],
            options={
                'verbose_name': 'Account Journal (Monthly)',
                'verbose_name_plural': 'Accounts Journals (Monthly)',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('account.accountjournal',),
        ),
        migrations.AlterModelOptions(
            name='dailypaymentvoucher',
            options={'verbose_name': 'Payment Voucher (Daily)', 'verbose_name_plural': 'Payment Vouchers (Daily)'},
        ),
    ]
