# Generated by Django 3.2.6 on 2021-08-14 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0017_assetmeterreading_assetmetermeterreadingunit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metercode',
            name='meterAbbr',
        ),
    ]