
import  json

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from utils.mixin_utils import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Count

from core.settings import  REDIS_HOST, REDIS_PORT,REDIS_PASSWORD
from apps.utils.tencentcloud_sms import send_single_sms
from django_users.forms import DynamicLoginPostForm,DynamicLoginForm
import random
import redis

from .models import UserProfile
from t.models import wj_unfinish
from grp_archive.models import archive
from django_users.forms import LoginForm, ModifyPwdForm
from django.http.response import HttpResponseRedirect,HttpResponseNotFound,HttpResponseServerError


# Create your views here.



class DynamicLoginView(View):
    """
    动态验证码登录
    """

    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        if login_form.is_valid():
            # 需求：没有注册依然也可以登录
            # 查询表中，有没有这个手机号
            mobile = login_form.cleaned_data["mobile"]
            existed_user = UserProfile.objects.filter(username=mobile)

            if existed_user:
                # 如果用户存在的话，就取出这个用户对象
                user = existed_user[0]
            else:
                # 用户不存在，就新建一个用户(这里的用户名当然要指向mobile了)
                user = UserProfile(username=mobile)
                # 因为这个用户是使用设计验证码登录的，以前没有这用户，所以也就没有他的密码，但是密码这个字段有时必填字段
                password = str(random.randrange(10000000, 99999999))  # 生成一个8位的随机密码
                user.set_password(password)  # 以密文的方式保存到数据库
                user.username = mobile  # 因为这个是必填字段，所以要给mobile也指定一个值
                user.save()

            # 执行登录操作
            login(request, user)

            # 用户登陆之前正在访问哪个页面，就让他登陆后停留在哪个页面
            next = request.GET.get("next", "")
            if next:
                return redirect(next)

            return redirect(reverse("index"))
        else:
            # 当为手机验证码登录失败是，这里为True
            dynamic_login = True
            # 动态图形验证码
            d_form = DynamicLoginForm()

            return render(request, "login.html", {
                "login_form": login_form,
                "dynamic_login": dynamic_login,
                'd_form': d_form,

            })


class SendSmsView(View):
    """
    发送短信验证码
    """

    def post(self, request, *args, **kwargs):
        # 验证图形验证码是否正确
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():

            mobile = send_sms_form.cleaned_data["mobile"]
            # 随机生成验证码

            code = random.randrange(1000, 9999)  # 生成一个4位的随机密码
            re_json = send_single_sms(mobile,1526589,[code,5])


            if re_json["result"] == 0:
                re_dict["status"] = "success"

                # 把手机验证码存储到redis
                r = redis.Redis(host='localhost', port=6379, password='123456.',db=0, charset="utf8", decode_responses=True)


                r.set(str(mobile), code)  # 手机号与验证码（有就覆盖，没有就创建）

                r.expire(str(mobile), 300)  # 300秒后过期

            else:
                re_dict["msg"] = re_json["re_json"]
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]

        return JsonResponse(re_dict)





class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

class LoginView(View):
    def get(self, request):
        # 判断用户是否已经登录
        if request.user.is_authenticated:
            # 已经登录的用户，直接重定向到首页
            return redirect(reverse("index"))

        next = request.GET.get("next", "")
        # 动态图形验证码
        login_form = DynamicLoginForm()
        return render(request, "login.html",
            {"login_form": login_form,
            "next": next,})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            try:
                user_prof = UserProfile.objects.get(username=user_name)
                if user_prof.password == '123456':
                    user_prof.password = make_password(pass_word)
                    user_prof.save()
            except:
                pass
                # return HttpResponse('出错了，请联系工作人员',content_type='text/plain;charset=utf-8')

            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    messages.success(request, "用户未激活!")
                    return render(request, "login.html", {"msg":"用户未激活！"})
            else:

                messages.success(request, "用户名或密码错误!")
                return render(request, "login.html", {"msg":"用户名或密码错误！"})
        else:
            return render(request, "login.html", {"login_form":login_form})




class IndexView(View):
    @method_decorator(login_required)
    def get(self,request):


        return render( request,'index.html')
class HomeView(View):

    def get(self,request):
        dpt_list = ['湖州', '金华','义乌','台州','丽水','嘉兴','萧山','衢州','舟山','杭州','绍兴','西溪']
        #剩余任务量
        wj_sum = [wj_unfinish.objects.filter(dpt_name = i ).count()  for i in dpt_list]
        #分公司常规量
        wj_sum2 = [wj_unfinish.objects.filter(Q(dpt_name = i)&
                                              (Q(is_pref = None)|Q(is_pref = ''))&
                                              (Q(dpt_class = None)|Q(dpt_class = ''))
                                              ).count()  for i in dpt_list]
        #机构专项量
        wj_sum3 = [wj_unfinish.objects.filter(Q(dpt_name = i)&
                                              (Q(is_pref = None)|Q(is_pref = ''))&
                                              (~Q(dpt_class = None) & ~Q(dpt_class = ''))
                                              ).count()  for i in dpt_list]


        #每日优先量
        wj_sum4 = [wj_unfinish.objects.filter(Q(dpt_name=i) &
                                              (Q(is_pref="Y"))
                                              ).count() for i in dpt_list]

        bd_sum =[archive.objects.filter(third_department_abbr_name = i ).count()  for i in dpt_list]
        bd_sum =[archive.objects.filter(Q(third_department_abbr_name = i) & Q(is_return=None)).count()  for i in dpt_list]

        wj_num = wj_unfinish.objects.all().count()
        bd_num = archive.objects.all().count()
        content = {
            'dpt_list':dpt_list,
         'wj_sum':wj_sum,
         'wj_sum2':wj_sum2,
         'wj_sum3':wj_sum3,
         'wj_sum4':wj_sum4,
        'bd_sum':bd_sum,
        'wj_num':wj_num,
        'bd_num':bd_num,


        }

        return render( request,'welcome.html',content)


class NotOpeView(View):
    def get(self,request):

        return render( request,'not-open-base.html')

class UserInfo(View):
    def get(self, request):

        name = request.user.name
        username = request.user.username
        dpt1 = request.user.dpt1
        dpt2 = request.user.dpt2
        dpt3 = request.user.dpt3

        content ={
            "name":name,
            "username":username,
            "dpt1":dpt1,
            "dpt2":dpt2,
            "dpt3":dpt3,
        }



        return render(request, 'user-show.html',content)


class PasswordResetView(View):
    def get(self, request):
        return render(request, 'user-password-edit.html')

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                content = {
                    'error': '两次密码输入不一致'
                }
                return render(request, 'user-password-edit.html', content)
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            content ={
                'sucess_state':'sucess'
            }

            return render(request, 'user-password-edit.html', content)
        else:

            content = {
                'error': '长度不得小于5'
            }


        return    render(request, 'user-password-edit.html',content)
