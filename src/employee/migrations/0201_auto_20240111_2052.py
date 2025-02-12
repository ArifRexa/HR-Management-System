# Generated by Django 3.2.8 on 2024-01-11 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0200_alter_employee_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavemanagement',
            name='manager',
            field=models.ForeignKey(limit_choices_to=models.Q(('active', True), models.Q(('manager', True), ('lead', True), _connector='OR')), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leave_management_manager', to='employee.employee'),
        ),
        migrations.AlterField(
            model_name='leavemanagement',
            name='status',
            field=models.CharField(choices=[('pending', '⏳ Pending'), ('approved', '✅ Approved'), ('rejected', '⛔ Rejected'), ('need_action', '◌ Need Further Discussion')], default='pending', max_length=20),
        ),
    ]
