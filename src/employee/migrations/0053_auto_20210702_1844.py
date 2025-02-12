# Generated by Django 3.2.5 on 2021-07-02 12:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import employee.models.attachment


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0052_auto_20210702_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='file_name',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(upload_to=employee.models.attachment.user_directory_path),
        ),
        migrations.AlterField(
            model_name='employee',
            name='joining_date',
            field=models.DateField(default=datetime.datetime(2021, 7, 2, 12, 44, 45, 581359, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='resignation',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 7, 2, 12, 44, 45, 584913, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salaryhistory',
            name='active_from',
            field=models.DateField(default=datetime.datetime(2021, 7, 2, 12, 44, 45, 582102, tzinfo=utc)),
        ),
    ]
