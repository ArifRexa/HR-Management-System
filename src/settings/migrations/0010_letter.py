# Generated by Django 3.2.5 on 2021-07-07 16:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('settings', '0009_bank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('header', models.TextField()),
                ('sticky_header', models.BooleanField(default=False)),
                ('body', tinymce.models.HTMLField()),
                ('footer', models.TextField()),
                ('sticky_footer', models.BooleanField(default=False)),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='settings_letter_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
