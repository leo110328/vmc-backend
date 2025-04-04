# Generated by Django 4.1 on 2025-03-30 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MedicationUseInfo',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='UUID')),
                ('user_id', models.CharField(max_length=32, verbose_name='用户ID')),
                ('chicken_flock_id', models.CharField(max_length=32, verbose_name='鸡群ID')),
                ('chicken_name', models.CharField(max_length=32, verbose_name='鸡群ID')),
                ('medication_name', models.CharField(max_length=32, verbose_name='药物名称')),
                ('medication_dose', models.CharField(max_length=32, verbose_name='药物剂量')),
                ('medication_measure', models.CharField(max_length=32, verbose_name='药物用量')),
                ('usage_duration', models.CharField(max_length=32, verbose_name='使用天数')),
                ('data_time', models.CharField(max_length=10, verbose_name='数据时间')),
                ('data_version', models.IntegerField(verbose_name='数据版本')),
                ('create_time', models.CharField(max_length=50, verbose_name='新增时间')),
                ('create_by', models.CharField(max_length=32, verbose_name='新增人')),
                ('update_time', models.CharField(max_length=50, verbose_name='更新时间')),
                ('update_by', models.CharField(max_length=32, verbose_name='更新人')),
                ('deleted', models.BooleanField(default=0, max_length=32, verbose_name='数据是否已删除[0:未删除,1:已删除]')),
            ],
            options={
                'db_table': 'medication_use_info',
                'unique_together': {('id', 'data_time', 'data_version')},
            },
        ),
    ]
