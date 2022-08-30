# Generated by Django 3.2.13 on 2022-08-28 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, verbose_name='数量')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='单价')),
                ('comment', models.TextField(default='', verbose_name='评价信息')),
                ('score', models.SmallIntegerField(choices=[(0, '0分'), (1, '20分'), (2, '40分'), (3, '60分'), (4, '80分'), (5, '100分')], default=5, verbose_name='满意度评分')),
                ('is_anonymous', models.BooleanField(default=False, verbose_name='是否匿名评价')),
                ('is_commented', models.BooleanField(default=False, verbose_name='是否评价了')),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
                'db_table': 'tb_order_goods',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('order_id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='订单号')),
                ('total_count', models.IntegerField(default=1, verbose_name='商品总数')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品总金额')),
                ('freight', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='运费')),
                ('pay_method', models.SmallIntegerField(choices=[(1, '货到付款'), (2, '支付宝')], default=1, verbose_name='支付方式')),
                ('status', models.SmallIntegerField(choices=[(1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成'), (6, '已取消')], default=1, verbose_name='订单状态')),
            ],
            options={
                'verbose_name': '订单基本信息',
                'verbose_name_plural': '订单基本信息',
                'db_table': 'tb_order_info',
            },
        ),
        migrations.CreateModel(
            name='OrderGoodsSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderGoods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='xadmin_inline.ordergoods', verbose_name='订单')),
            ],
            options={
                'verbose_name': '订单商品规格信息',
                'verbose_name_plural': '订单商品规格信息',
                'db_table': 'tb_order_goodsSpecification',
            },
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skus', to='xadmin_inline.orderinfo', verbose_name='订单'),
        ),
    ]
