# Generated by Django 3.2.6 on 2021-08-14 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0008_auto_20210814_1005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assetmeterreading',
            name='assetMeterMeterReadingUnit',
        ),
    ]