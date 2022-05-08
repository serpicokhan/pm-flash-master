# Generated by Django 3.2.6 on 2022-05-06 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmms', '0010_alter_assetmetertemplate_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='task_inspection',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='taskTypes',
            field=models.IntegerField(blank=True, choices=[(1, 'عمومی'), (2, 'متنی'), (3, 'متریک'), (4, 'بازرسی')], null=True, verbose_name='انتخاب نوع فعالیت'),
        ),
    ]