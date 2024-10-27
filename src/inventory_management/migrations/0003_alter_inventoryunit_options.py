

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0002_inventoryunit_allow_decimal'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventoryunit',
            options={'verbose_name': 'Inventory Item Unit', 'verbose_name_plural': 'Inventory Item Units'},
        ),
    ]
