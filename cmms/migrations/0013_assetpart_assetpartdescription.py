# Generated by Django 3.2.6 on 2022-01-02 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0012_alter_schedule_schtriggertime'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetpart',
            name='assetPartDescription',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='توضیح'),
        ),
    ]
