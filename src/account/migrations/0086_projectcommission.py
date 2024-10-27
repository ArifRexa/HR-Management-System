# Generated by Django 4.0.2 on 2022-09-20 16:12

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0032_project_in_active_at'),
        ('employee', '0104_employee_show_in_web'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0085_income_loss_hours_alter_income_convert_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectCommission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(default=datetime.datetime(2022, 9, 20, 16, 12, 31, 14693))),
                ('payment', models.FloatField()),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('employee', models.ForeignKey(limit_choices_to={'active': True}, on_delete=django.db.models.deletion.RESTRICT, to='employee.employee')),
                ('project', models.ForeignKey(limit_choices_to={'active': True}, on_delete=django.db.models.deletion.RESTRICT, to='project_management.project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
