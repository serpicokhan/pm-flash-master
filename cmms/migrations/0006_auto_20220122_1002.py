# Generated by Django 3.2.6 on 2022-01-22 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0005_alter_assetmeterreading_assetmetermeterreadingunit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaserequest',
            name='PurchaseRequestAssetName',
        ),
        migrations.AddField(
            model_name='purchaserequest',
            name='PurchaseRequestPartName',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='RequestedPart', to='cmms.part', verbose_name='مشخصات قطعه'),
        ),
        migrations.AlterField(
            model_name='purchaserequest',
            name='PurchaseRequestAssetQty',
            field=models.FloatField(blank=True, verbose_name='تعداد'),
        ),
        migrations.AlterField(
            model_name='purchaserequest',
            name='PurchaseRequestNotInList',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='purchaserequest',
            name='PurchaseRequestWO',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ImpactedWO', to='cmms.workorder', verbose_name='درخواست مربوطه'),
        ),
    ]
