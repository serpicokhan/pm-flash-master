# Generated by Django 3.2.6 on 2023-06-10 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0002_remove_assetcadcoordination_z'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetcadcoordination',
            name='z',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
