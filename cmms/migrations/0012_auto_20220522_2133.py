# Generated by Django 3.2.6 on 2022-05-22 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0011_auto_20220506_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='taskCompletionNote',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='یادداشت تکمیلی'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='taskDescription',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='توضیحات'),
        ),
    ]
