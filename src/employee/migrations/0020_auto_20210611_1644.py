# Generated by Django 3.2 on 2021-06-11 10:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0019_auto_20210610_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='joining_date',
            field=models.DateField(default=datetime.datetime(2021, 6, 11, 10, 44, 13, 464052, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salaryhistory',
            name='active_from',
            field=models.DateField(default=datetime.datetime(2021, 6, 11, 10, 44, 13, 464609, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='LeaveManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_leave', models.FloatField()),
                ('message', models.TextField()),
                ('note', models.TextField(null=True)),
                ('leave_type', models.CharField(choices=[('casual', 'Casual Leave'), ('medical', 'Medical Leave'), ('non_paid', 'Non Paid Leave')], max_length=20)),
                ('approved_at', models.DateField(null=True)),
                ('approve_by', models.ForeignKey(limit_choices_to={'is_superuser': True}, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_leavemanagement_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LeaveAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attachment', models.FileField(help_text='Image , PDF or Docx file ', upload_to='')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_leaveattachment_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('leave', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.leavemanagement')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
