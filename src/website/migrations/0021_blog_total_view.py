# Generated by Django 3.2.8 on 2024-01-19 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0020_alter_blogcomment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='total_view',
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
    ]
