# Generated by Django 3.2.6 on 2021-11-30 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0003_auto_20211130_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='partCategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dasdadassa', to='cmms.partcategory', verbose_name='دسته بندی'),
        ),
    ]
