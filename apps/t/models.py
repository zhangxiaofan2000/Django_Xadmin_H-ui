import random
import os
from uuid import uuid4


from django.db import models
from datetime import datetime
from django.utils.deconstruct import deconstructible

from apps.django_users.models import UserProfile
# Create your models here.
REASON1_CHIOCES=(
    ("无人接听","无人接听"),
    ("联系通畅","联系通畅"),
    ("有历史记录","有历史记录"),
)

CASE_CLOSED_CHIOCES=(
    ("0结案","0结案"),
    ("不结案","不结案"),
    ("有历史记录","有历史记录"),
)


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(instance.pk, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

class AutoIncrementFields(models.Model):
    """
    provide a unique ID for all models of code sign
    """
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return str(self.id)

class wj_task(models.Model):

    id = models.CharField(max_length=128)
    def save(self, *args, **kwargs):

        time = str(datetime.now())
        _ = AutoIncrementFields.objects.create()
        self.id = 'WJ' +time[0:4]+time[5:7]+time[8:10]+ str(_.id)
        return super(wj_task, self).save(*args, **kwargs)



    dpt_name = models.CharField(max_length=20,verbose_name='机构名称')
    report_no = models.CharField(max_length=30,verbose_name='报案号',primary_key=True)
    report_date = models.DateTimeField(verbose_name='报案时间')
    register_date = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    car_person = models.CharField(max_length=80,blank=True,null=True,verbose_name='car_person(在此为被回访人)')
    injured_person = models.CharField(max_length=80,blank=True,null=True,verbose_name='injured_person(没有用到)')
    estimate_amount = models.DecimalField( max_digits=10, blank=True,null=True,decimal_places=2,verbose_name='立案金额')
    car_amount =models.DecimalField( max_digits=10, blank=True,null=True,decimal_places=2,verbose_name='car_amount(没有用到)')
    injured_amount = models.DecimalField( max_digits=10, blank=True,null=True,decimal_places=2,verbose_name='injured_amount(没有用到)')
    visited = models.CharField(max_length=30,blank=True,null=True,verbose_name='visited(没有用到)')
    tracer = models.CharField(max_length=30,blank=True,null=True,verbose_name='回访柜面')
    tracering_date = models.DateTimeField(verbose_name='回访时间',blank=True,null=True)
    visit_phone = models.CharField(max_length=20,blank=True,null=True,verbose_name="柜面电话")
    wj_reason1 = models.CharField(max_length=100,choices=REASON1_CHIOCES,blank=True,null=True,verbose_name='未决原因1')
    wj_reason2 = models.CharField(max_length=100,blank=True,null=True,verbose_name='未决原因2')
    wj_reason3 = models.CharField(max_length=100,blank=True,null=True,verbose_name='未决原因3(没有用到)')
    is_coupon = models.CharField(max_length=20,blank=True,null=True,verbose_name ='is_coupon(没有用到)')
    remake = models.CharField(max_length=300,blank=True,null=True,verbose_name = '备注')
    update_time = models.DateTimeField(verbose_name='更新时间',blank=True,null=True)
    finish_time = models.DateTimeField(verbose_name='回访结束时间',blank=True,null=True)
    visited_phone =  models.CharField(max_length=20,blank=True,null=True,verbose_name="被回访人电话")
    visit_dpt = models.CharField(max_length=20,blank=True,null=True,verbose_name="柜面机构")
    visit_dpt2 = models.CharField(max_length=20,blank=True,null=True,verbose_name="柜面网点")
    num_issued = models.CharField(max_length=30,blank=True,null=True,verbose_name="num_issued(没有用到)")
    dpt_class = models.CharField(max_length=20,blank=True,null=True,verbose_name='岗位')
    is_pref = models.CharField(max_length=20,blank=True,null=True,verbose_name='is_pref(没有用到)')
    counter_specify = models.CharField(max_length=20,blank=True,null=True,verbose_name='counter_specify(没有用到)')
    event_type = models.CharField(max_length=20,verbose_name='案件类型')
    complaint_risk = models.CharField(max_length=30,blank=True,null=True,verbose_name='投诉风险')
    case_closed = models.CharField(max_length=10,choices=CASE_CLOSED_CHIOCES,blank=True,null=True,verbose_name='结案类型')
    
    # TODO:确定上传录音文件的相对路径
    sound_record = models.FileField(upload_to=PathAndRename("t_sound_record/"),blank=True,null=True, verbose_name=u"回访录音")
    class Meta:
        abstract = True



class wj_unfinish(wj_task):

    class Meta:
        verbose_name = u"未完成任务"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.report_no


class wj_finish(wj_task):


    tracer = models.CharField(max_length=30, verbose_name='回访柜面')
    tracering_date = models.DateTimeField(verbose_name='回访时间')
    # update_time = models.DateTimeField(verbose_name='更新时间')
    finish_time = models.DateTimeField(verbose_name='回访结束时间')

    class Meta:
        verbose_name = u"已完成任务"

        verbose_name_plural = verbose_name

    def __str__(self):
        return self.report_no

# class wj_recording(models.Model):
#
#     report = models.ForeignKey(wj_finish,verbose_name='保单',on_delete=models.DO_NOTHING)
#     tracer = models.ForeignKey(UserProfile,verbose_name='追踪柜员',on_delete=models.DO_NOTHING)
#
#
#     sound_record = models.FileField(upload_to="t_sound_record/%Y/%m",null=True,blank=True)
#
#     class Meta:
#         verbose_name = u"未决回访录音"
#
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.sound_record
