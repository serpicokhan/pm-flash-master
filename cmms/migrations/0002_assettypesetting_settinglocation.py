# Generated by Django 2.0.2 on 2021-05-25 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assettypesetting',
            name='settingLocation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmms.Asset'),
        ),
    ]