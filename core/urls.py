"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve
from django.urls import path

import xadmin
from core.settings import MEDIA_ROOT,STATIC_ROOT


from django_users.views import IndexView, HomeView, NotOpeView, PasswordResetView, UserInfo, LoginView, LogoutView,DynamicLoginView,SendSmsView


urlpatterns = [
    url('^$', IndexView.as_view(), name="index"),
    url('^welcome/', HomeView.as_view(), name="home"),
    url('^notopen/', NotOpeView.as_view(), name="notopen"),
    url('^pwreset/', PasswordResetView.as_view(), name="pwreset"),
    url('^userinfo/', UserInfo.as_view(), name="userinfo"),


    url(r'^xadmin/', xadmin.site.urls),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),

    url(r'^captcha/', include('captcha.urls')),
    path('dynamic_login/', DynamicLoginView.as_view(), name="dynamic_login"),
    url(r'^send_sms/', SendSmsView.as_view(), name="send_sms"),




    url(r'^weijue/', include(('t.urls', "t"), namespace="weijue")),
    url(r'^grp/', include(('grp_archive.urls', "grp_archive"), namespace="grp")),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),


]
