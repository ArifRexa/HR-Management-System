# Generated by Django 3.2.8 on 2024-01-17 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_alter_blog_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='tag',
            field=models.ManyToManyField(related_name='tags', to='website.Tag'),
        ),
    ]
