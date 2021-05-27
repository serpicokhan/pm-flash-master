# Generated by Django 2.0.2 on 2021-05-27 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0003_auto_20210525_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetcategory',
            name='code',
            field=models.CharField(default=None, max_length=50, verbose_name='کد'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assettypesetting',
            name='settingLocation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmms.Asset', verbose_name='مکان'),
        ),
    ]
