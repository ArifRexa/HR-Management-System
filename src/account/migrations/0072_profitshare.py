# Generated by Django 3.2.6 on 2021-09-09 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0071_expense_expanse_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfitShare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('payment_amount', models.FloatField()),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_profitshare_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('user', django_userforeignkey.models.fields.UserForeignKey(limit_choices_to={'is_superuser': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
