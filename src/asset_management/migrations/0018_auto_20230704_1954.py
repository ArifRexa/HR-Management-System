# Generated by Django 3.2.8 on 2023-07-04 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0170_employee_device_allowance'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asset_management', '0017_alter_credential_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='code',
            field=models.SlugField(default=uuid.uuid4, max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='last_assigned',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='need_repair',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='asset',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.CreateModel(
            name='EmployeeAssignedAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset_management.asset')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asset_management_employeeassignedasset_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
