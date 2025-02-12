# Generated by Django 3.2.8 on 2023-01-24 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0129_employeeactivity_updated_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('maturity_date', models.DateField()),
                ('scale', models.FloatField(default=10.0, help_text='Percentage of basic salary')),
                ('note', models.TextField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='provident_fund_account_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
