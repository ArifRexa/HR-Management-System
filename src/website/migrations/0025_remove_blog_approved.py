# Generated by Django 3.2.8 on 2024-01-26 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0024_blog_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='approved',
        ),
    ]
