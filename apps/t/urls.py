from django.conf.urls import url, include
from django.urls import path
from .views import UnfinishView,FinishView,AddTaskView,UploadView

urlpatterns = [

url(r'^unfinish/$', UnfinishView.as_view(), name="unfinish"),
url(r'^finish/$', FinishView.as_view(), name="finish"),
url(r'^unfinish/addtask/$', AddTaskView.as_view(), name="addtask"),
url(r'^upload/(?P<report_no>.*)$', UploadView.as_view(), name="upload"),


]
