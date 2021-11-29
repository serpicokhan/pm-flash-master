# Generated by Django 3.2.6 on 2021-11-29 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0006_auto_20211129_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='partcategory',
            name='code',
            field=models.CharField(default=None, max_length=50, unique=True, verbose_name='کد'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partcategory',
            name='description',
            field=models.CharField(default=1, max_length=50, verbose_name='توضیحات'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partcategory',
            name='name',
            field=models.CharField(default='1', max_length=50, verbose_name='نام'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partcategory',
            name='priority',
            field=models.IntegerField(null=True, verbose_name='اولویت'),
        ),
        migrations.AlterField(
            model_name='partcategory',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
