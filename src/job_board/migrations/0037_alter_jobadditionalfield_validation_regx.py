# Generated by Django 3.2.5 on 2021-08-09 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_board', '0036_auto_20210806_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobadditionalfield',
            name='validation_regx',
            field=models.CharField(choices=[('(.*)', 'All'), ('(?:git@|https://)github.com[:/](.*)', 'Git Hub'), ('(?:https://www.|https://)linkedin.com[:/](.*)', 'Linkedin'), ('(?:https://www.|https://)figma.com[:/](.*)', 'Figma'), ('(?:https://www.|https://)behance.net[:/](.*)', 'Behance'), ('(?:https://www.|https://)youtube.com[:/](.*)', 'Youtube'), ('(?:https://www.|https://)(?:facebook|fb).com[:/](.*)', 'Facebook'), ('(?:https://www.|https://)twitter.com[:/](.*)', 'Twitter'), ('^[0-9]*$', 'NUmber Only')], default='(.*)', max_length=255),
        ),
    ]
