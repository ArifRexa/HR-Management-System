# Generated by Django 3.2.8 on 2023-09-12 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0176_hrpolicy_hrpolicypublic_hrpolicysection'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeNOC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('noc_body', tinymce.models.HTMLField()),
                ('noc_pdf', models.FileField(blank=True, null=True, upload_to='')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_employeenoc_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('employee', models.OneToOneField(limit_choices_to={'active': True}, on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
