# Generated by Django 3.2.6 on 2023-05-20 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0010_alter_asset_assettavali'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ringamar',
            unique_together={('ShiftTypes', 'assetName', 'assetAmarDate')},
        ),
    ]
