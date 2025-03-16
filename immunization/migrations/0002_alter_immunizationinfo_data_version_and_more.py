# Generated by Django 4.1 on 2025-03-15 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('immunization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='immunizationinfo',
            name='data_version',
            field=models.IntegerField(verbose_name='数据版本'),
        ),
        migrations.AlterUniqueTogether(
            name='immunizationinfo',
            unique_together={('id', 'data_time', 'data_version')},
        ),
    ]
