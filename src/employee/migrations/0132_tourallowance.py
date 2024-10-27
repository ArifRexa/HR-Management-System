# Generated by Django 3.2.8 on 2023-02-17 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0131_employeeactivity_is_updated_by_bot'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourAllowance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('expense_per_person', models.PositiveIntegerField()),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_tourallowance_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('employees', models.ManyToManyField(blank=True, limit_choices_to={'active': True}, to='employee.Employee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
