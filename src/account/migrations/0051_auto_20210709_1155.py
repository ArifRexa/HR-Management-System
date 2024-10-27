# Generated by Django 3.2.5 on 2021-07-09 05:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0010_alter_employeeprojecthour_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0050_auto_20210709_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 9, 5, 55, 48, 713643, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hours', models.FloatField()),
                ('hour_rate', models.FloatField()),
                ('date', models.DateField(default=datetime.datetime(2021, 7, 9, 5, 55, 48, 714199, tzinfo=utc))),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_income_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='project_management.project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
