# Generated by Django 3.2.6 on 2021-08-14 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0012_assetmeterreading_assetmetermeterreadingunit'),
    ]

    operations = [
        migrations.AddField(
            model_name='metercode',
            name='meterAbbr',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='اختصار'),
        ),
    ]
