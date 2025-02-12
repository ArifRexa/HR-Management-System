# Generated by Django 3.2.8 on 2023-01-24 16:06

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0128_auto_20230118_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeactivity',
            name='updated_by',
            field=django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities_updated', to=settings.AUTH_USER_MODEL, verbose_name='Updated By'),
        ),
    ]
