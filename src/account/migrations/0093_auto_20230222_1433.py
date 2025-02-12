# Generated by Django 3.2.8 on 2023-02-22 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0092_alter_expense_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fund',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='fund',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='FundCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_fundcategory_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='fund',
            name='fund_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='account.fundcategory'),
        ),
    ]
