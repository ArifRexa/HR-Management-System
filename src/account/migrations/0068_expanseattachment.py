# Generated by Django 3.2.5 on 2021-08-02 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0067_auto_20210720_1945'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpanseAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attachment', models.FileField(upload_to='uploads/expanse/%y/%m')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_expanseattachment_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('expanse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.expense')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
