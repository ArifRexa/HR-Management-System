# Generated by Django 3.2.8 on 2023-04-04 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0090_alter_codereview_review_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codereview',
            name='review_at',
            field=models.DateTimeField(null=True),
        ),
    ]
