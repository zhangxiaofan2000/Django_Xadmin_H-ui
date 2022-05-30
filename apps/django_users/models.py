from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser




class UserProfile(AbstractUser):

    password = models.CharField(default='123456', max_length=128,verbose_name='密码')
    name = models.CharField(max_length=30, verbose_name='姓名')

    dpt1 = models.CharField(max_length=20,verbose_name='机构')
    dpt2 = models.CharField(max_length=20,verbose_name='网点',blank=True,null=True)
    dpt3 = models.CharField(max_length=20,verbose_name='岗位',blank=True,null=True)

    # add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name="用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.username

