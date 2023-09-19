# Generated by Django 3.2.6 on 2023-09-17 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0009_alter_tolidamar_tolidmoshakhase'),
    ]

    operations = [
        migrations.AddField(
            model_name='tolidamar',
            name='isheatset',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='tolidamar',
            name='meghdar',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='tolidamar',
            name='registered_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='tolidamar',
            name='tedad',
            field=models.FloatField(null=True),
        ),
        migrations.AlterModelTable(
            name='tolidamar',
            table='tolidamar',
        ),
    ]