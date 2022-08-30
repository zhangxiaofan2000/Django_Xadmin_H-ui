
from django import forms
from django_users.models import UserProfile
import redis
from core.settings import REDIS_HOST, REDIS_PORT
from captcha.fields import CaptchaField



class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)



class DynamicLoginForm(forms.Form):
    """
    图形验证码
    """
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


class DynamicLoginPostForm(forms.Form):
    """
    手机动态验证码
    """
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):
        # 取出moblie和code
        mobile = self.data.get("mobile")
        code = self.data.get("code")

        r = redis.Redis(host='localhost', port=6379, password='123456.',db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(mobile)
        if code != redis_code:
            # 调用forms里面的方法，抛出异常
            raise forms.ValidationError("手机验证码不正确")
        return self.cleaned_data
