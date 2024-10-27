# Generated by Django 4.0 on 2022-01-25 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0095_alter_attachment_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='tax_info',
            field=models.CharField(blank=True, help_text='<TIN NUMBER>, Circle-<CIRCLE NO>, Zone-<ZONE NO> i.e: 59530389237, Circle–138, Zone-11', max_length=255, null=True),
        ),
    ]
