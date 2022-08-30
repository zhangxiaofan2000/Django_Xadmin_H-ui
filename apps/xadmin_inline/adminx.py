import xadmin
'''
conda activate t_plat2

conda activate t_plat

cd /root/home/t_plat

python manage.py runserver 0.0.0.0:8000

python manage.py makemigrations


python manage.py migrate

/root/redis-6.0.3/src/redis-server /root/redis-6.0.3/redis.conf


'''



from xadmin_inline.models import OrderInfo,OrderGoods,OrderGoodsSpecification
from import_export import resources
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field



class OrderInfoRes(resources.ModelResource):

    class Meta:
        model = OrderInfo
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        fields = ('order_id', 'total_count','total_amount','freight','pay_method','status','id')


class OrderGoodsSpecificationInline(object):

    model = OrderGoodsSpecification
    show_change_link = True
    extra = 0

class OrderGoodsInline(object):

    model = OrderGoods
    style = 'stacked' #one，accordion，tab，stacked，table
    show_change_link = True
    extra = 0
    inlines = (OrderGoodsSpecificationInline,)


class OrderInfoAdmin(object):

    import_export_args = {'import_resource_class': OrderInfoRes,
                          'export_resource_class': OrderInfoRes,}

    list_display = ['order_id', 'total_count','total_amount','freight','pay_method','status' ]

    # exclude = ('order_id', 'total_count','total_amount','freight','pay_method','status')
    search_fields = ['order_id','total_count',]
    ordering = ['total_count']
    list_filter =['order_id', 'total_count','total_amount','freight']
    model_icon = 'fa fa-square'
    inlines = (OrderGoodsInline,)




class OrderGoodsAdmin(object):



    list_display = ['order__order_id', 'count','price','comment','score','is_anonymous','is_commented']

    search_fields = ['order__order_id',]
    ordering = ['count']
    list_filter =[ 'count','price',]
    model_icon = 'fa fa-square'



class OrderGoodsSpecificationAdmin(object):


    list_display = ['orderGoods__order__order_id' ]



xadmin.site.register(OrderInfo, OrderInfoAdmin)



