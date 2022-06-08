# Generated by Django 3.2.13 on 2022-06-07 10:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='archive',
            fields=[
                ('id', models.CharField(max_length=128)),
                ('policy_no', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='保单号')),
                ('endorse_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='批单号')),
                ('is_reverse', models.CharField(blank=True, max_length=50, null=True, verbose_name='是否倒签单')),
                ('scene_name_list', models.CharField(blank=True, max_length=50, null=True, verbose_name='批改场景名')),
                ('planning_premium', models.CharField(blank=True, max_length=50, null=True, verbose_name='签单保费(批改保费)')),
                ('third_department_abbr_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='三级机构')),
                ('fourth_department_abbr_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='四级机构')),
                ('channel_new', models.CharField(blank=True, max_length=50, null=True, verbose_name='渠道')),
                ('employee_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='业务员名称')),
                ('employee_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='业务员代码')),
                ('product_class_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='产品大类名称')),
                ('product_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='产品细分')),
                ('tbr_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='投保人名称')),
                ('underwrite_date', models.DateTimeField(blank=True, null=True, verbose_name='签单时间')),
                ('material', models.CharField(blank=True, max_length=50, null=True, verbose_name='需回收材料')),
                ('upload_um', models.CharField(blank=True, max_length=50, null=True, verbose_name='上载人um号')),
                ('upload_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='上载时间')),
                ('is_return', models.CharField(blank=True, max_length=50, null=True, verbose_name='是否归还')),
                ('tracer', models.CharField(blank=True, max_length=50, null=True, verbose_name='追踪人')),
                ('tracer_dept', models.CharField(blank=True, max_length=50, null=True, verbose_name='追踪机构')),
                ('trace_date', models.DateTimeField(blank=True, null=True, verbose_name='更新状态时间')),
                ('return_material', models.CharField(blank=True, max_length=50, null=True, verbose_name='已回收材料')),
                ('backup8', models.CharField(blank=True, max_length=50, null=True, verbose_name='备用字段8')),
                ('backup9', models.CharField(blank=True, max_length=50, null=True, verbose_name='备用字段9')),
                ('backup10', models.CharField(blank=True, max_length=50, null=True, verbose_name='备用字段10')),
            ],
            options={
                'verbose_name': '团非车清单',
                'verbose_name_plural': '团非车清单',
            },
        ),
        migrations.CreateModel(
            name='AutoIncrementFields',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]