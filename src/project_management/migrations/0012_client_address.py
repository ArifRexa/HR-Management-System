# Generated by Django 3.2.8 on 2021-11-19 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0011_alter_employeeprojecthour_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
