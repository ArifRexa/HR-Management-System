# Generated by Django 3.2.8 on 2023-04-07 02:53

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0018_alter_employeefaqview_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeefaq',
            name='answer',
            field=tinymce.models.HTMLField(),
        ),
    ]
