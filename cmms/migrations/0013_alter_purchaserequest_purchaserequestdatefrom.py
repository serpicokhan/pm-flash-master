# Generated by Django 3.2.6 on 2022-06-25 11:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0012_auto_20220522_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaserequest',
            name='PurchaseRequestDateFrom',
            field=models.DateField(default=datetime.datetime(2022, 6, 25, 11, 57, 11, 84492), verbose_name='تاریخ درخواست'),
            preserve_default=False,
        ),
    ]