# Generated by Django 3.2.8 on 2023-09-13 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0177_employeenoc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeenoc',
            name='noc_pdf',
            field=models.FileField(blank=True, null=True, upload_to='noc/'),
        ),
    ]
