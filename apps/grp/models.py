from django.db import models
from datetime import datetime
# Create your models here.




class AutoIncrementFields(models.Model):
    """
    provide a unique ID for all models of code sign
    """
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return str(self.id)

class archive(models.Model):

    id = models.CharField(max_length=128)
    def save(self, *args, **kwargs):

        time = str(datetime.now())
        _ = AutoIncrementFields.objects.create()
        self.id = 'BD' +time[0:4]+time[5:7]+time[8:10]+ str(_.id)
        return super(archive, self).save(*args, **kwargs)


    policy_no = models.CharField(max_length=50,verbose_name='保单号',primary_key=True)
    endorse_no = models.CharField(max_length=50,null=True,blank=True,verbose_name='批单号')
    is_reverse = models.CharField(max_length=50,null=True,blank=True,verbose_name='是否倒签单')
    scene_name_list = models.CharField(max_length=50,null=True,blank=True,verbose_name='批改场景名')
    planning_premium = models.CharField(max_length=50,null=True,blank=True,verbose_name='签单保费(批改保费)')
    third_department_abbr_name = models.CharField(max_length=50,null=True,blank=True,verbose_name='三级机构')
    fourth_department_abbr_name = models.CharField(max_length=50,null=True,blank=True,verbose_name='四级机构')
    channel_new = models.CharField(max_length=50,null=True,blank=True,verbose_name='渠道')
    employee_name = models.CharField(max_length=50,null=True,blank=True,verbose_name='业务员名称')
    employee_code = models.CharField(max_length=50,null=True,blank=True,verbose_name='业务员代码')
    product_class_name = models.CharField(max_length=50,null=True,blank=True,verbose_name='产品大类名称')
    product_name = models.CharField(max_length=50,null=True,blank=True,verbose_name='产品细分')
    tbr_name = models.CharField(max_length=50,null=True,blank=True,verbose_name='投保人名称')
    underwrite_date = models.DateTimeField(null=True,blank=True,verbose_name='签单时间')
    material = models.CharField(max_length=50,null=True,blank=True,verbose_name='需回收材料')
    upload_um = models.CharField(max_length=50,null=True,blank=True,verbose_name='上载人um号')
    upload_date = models.DateTimeField(default=datetime.now,null=True,blank=True,verbose_name='上载时间')
    is_return = models.CharField(max_length=50,null=True,blank=True,verbose_name='是否归还')
    tracer = models.CharField(max_length=50,null=True,blank=True,verbose_name='追踪人')
    tracer_dept = models.CharField(max_length=50,null=True,blank=True,verbose_name='追踪机构')
    trace_date = models.DateTimeField(null=True,blank=True,verbose_name='更新状态时间')
    return_material = models.CharField(max_length=50,null=True,blank=True,verbose_name='已回收材料')
    backup8 = models.CharField(max_length=50,null=True,blank=True,verbose_name='备用字段8')
    backup9 = models.CharField(max_length=50,null=True,blank=True,verbose_name='备用字段9')
    backup10 = models.CharField(max_length=50,null=True,blank=True,verbose_name='备用字段10')


    class Meta:
        verbose_name = u"团非车清单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.policy_no
