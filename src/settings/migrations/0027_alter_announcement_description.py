# Generated by Django 3.2.8 on 2023-09-22 18:00

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):
    dependencies = [
        ("settings", "0026_employeefoodallowance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="description",
            field=tinymce.models.HTMLField(),
        ),
    ]
