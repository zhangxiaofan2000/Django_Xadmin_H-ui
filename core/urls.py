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
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve

import xadmin
from core.settings import MEDIA_ROOT


from django_users.views import IndexView,HomeView,NotOpeView,PasswordResetView,UserInfo,LoginView,LogoutView


urlpatterns = [
    url('^$', IndexView.as_view(), name="index"),
    url('^welcome/', HomeView.as_view(), name="home"),
    url('^notopen/', NotOpeView.as_view(), name="notopen"),
    url('^pwreset/', PasswordResetView.as_view(), name="pwreset"),
    url('^userinfo/', UserInfo.as_view(), name="userinfo"),


    url(r'^xadmin/', xadmin.site.urls),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),

    url(r'^weijue/', include(('t.urls', "t"), namespace="weijue")),
    url(r'^grp/', include(('grp.urls', "grp"), namespace="grp")),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
