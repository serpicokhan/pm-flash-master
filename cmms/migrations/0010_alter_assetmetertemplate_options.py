# Generated by Django 3.2.6 on 2022-05-05 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0009_alter_bmgtemplate_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assetmetertemplate',
            options={'ordering': ['assetMeterTemplateDesc']},
        ),
    ]
