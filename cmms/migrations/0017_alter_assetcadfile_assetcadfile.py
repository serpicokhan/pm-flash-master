# Generated by Django 3.2.6 on 2023-04-17 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0016_assetcadfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetcadfile',
            name='assetCadFile',
            field=models.FileField(max_length=200, upload_to='documents/%Y/%m/%d'),
        ),
    ]
