from datetime import datetime
import time
import json

from django.shortcuts import render
from django.views.generic import View
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.forms.models import model_to_dict

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.context_processors import PermWrapper
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.mixin_utils import LoginRequiredMixin

from apps.t.models import wj_unfinish,wj_finish
from apps.t.forms import SoundRecordForm,FinshInfoForm







class UnfinishView(View):
    '''
    查看未完成未决回访
    '''

    def get_content(self,request):

        # 获取权限
        hav_view_prem = False
        count = 0
        count = count + request.user.user_permissions.filter(codename='view_wj_unfinish').count()
        for i in request.user.groups.all():
            count = count + i.permissions.filter(codename='view_wj_unfinish').count()
        if count != 0:
            hav_view_prem = True

        search = request.GET.get('search')
        if search:
            all_tracer_task = wj_unfinish.objects.filter(Q(tracer=request.user.username)&
                                                         (Q(report_no=search)|
                                                         Q(dpt_name=search)|
                                                         Q(report_no__icontains=search)|
                                                         Q(wj_reason1__icontains=search)|
                                                         Q(case_closed__icontains=search)))
        else:
            all_tracer_task = wj_unfinish.objects.filter(tracer=request.user.username)

        # 取数据
        nums = wj_unfinish.objects.filter(tracer=None).count()
        #对任务进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_tracer_task, 10, request=request)

        all_tracer_task = p.page(page)

        content = {
            "hav_view_prem": hav_view_prem,
            "nums": nums,
            "all_tracer_task": all_tracer_task,
        }
        return content

    def get(self,request):

        content = self.get_content(request)

        return render(request, 'weijue-unfinish-list.html', content)


    def post(self, request):

        content = self.get_content(request)

        # 验证表单
        post_task = wj_unfinish.objects.get(report_no=request.POST.get("report_no"))


        # save_file_form = SoundRecordForm(request.POST, request.FILES, instance=post_task)
        # if save_file_form.is_valid():
        #     save_file_form.save(commit=False)
        #     # save_file_form.data = finish_form.data
        #     save_file_form.save()



        finish_task = wj_finish.objects.filter(report_no=request.POST.get("report_no")).first()
        data = model_to_dict(post_task)
        data.update(request.POST.dict())
        data['wj_reason1'] = request.POST.get("wj_reason1")
        data['case_closed'] = request.POST.get("case_closed")

        data['remake'] = request.POST.get("remake")
        data['finish_time'] = datetime.now()

        finish_form = FinshInfoForm(data, request.FILES, instance=finish_task)



        if finish_form.is_valid():
            finish_form.save()
            post_task.delete()


        elif 'wj_reason1' in finish_form.errors.keys() :
            # messages.success(request,"请选择未决原因")
            content['error']='请选择未决原因'
            return render(request, 'weijue-unfinish-list.html', content)

        elif 'case_closed' in finish_form.errors.keys() :
            # messages.success(request,"请选择结案类型")
            content['error'] = '请选择结案类型'
            return render(request, 'weijue-unfinish-list.html', content)

        # elif 'sound_record' in finish_form.errors.keys() :
        #     # messages.success(request, "请上传录音文件")
        #     content['error'] = '请上传录音文件'
        #     return render(request, 'weijue-unfinish-list.html', content)

        content['sucess_state'] = 'sucess'
        return render(request, 'weijue-unfinish-list.html', content)
        # save_file_form = SoundRecordForm(request.POST, request.FILES,instance=request.user)
        # finish_time
        # if save_file_form.is_valid():
        #     post_files = request.FILES.getlist('save_files')
        #     for file in post_files:
        #         save_file_model = SoundRecordForm()
        #         save_file_model.save_file = file
        #         save_file_model.save()
        #         # Unfinsh_Info_Form.save()
        #         print(file.name)







class FinishView(View):

    def get_content(self,request):

        # 获取权限
        hav_view_prem = False
        count = 0
        count = count + request.user.user_permissions.filter(codename='view_wj_unfinish').count()
        for i in request.user.groups.all():
            count = count + i.permissions.filter(codename='view_wj_unfinish').count()
        if count != 0:
            hav_view_prem = True

        search = request.GET.get('search')
        if search:
            finish_task = wj_finish.objects.filter(Q(tracer=request.user.username)&
                                                         (Q(report_no=search)|
                                                         Q(dpt_name=search)|
                                                         Q(report_no__icontains=search)|
                                                         Q(wj_reason1__icontains=search)|
                                                         Q(case_closed__icontains=search))).order_by('-finish_time')
        else:
            finish_task = wj_finish.objects.filter(tracer=request.user.username).order_by('-finish_time')

        # 取数据
        nums = wj_finish.objects.all().count()
        #对任务进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(finish_task, 10, request=request)

        finish_task = p.page(page)

        content = {
            "hav_view_prem": hav_view_prem,
            "nums": nums,
            "finish_task": finish_task,
        }
        return content

    def get(self,request):

        content = self.get_content(request)

        return render(request, 'weijue-finish-list.html', content)



class AddTaskView(View):

    def get(self, request):

        def select(select_task):
            select_task.tracering_date = datetime.now()
            select_task.tracer = request.user.username
            select_task.save()

        total_num =  wj_unfinish.objects.all().count()
        tracer_task_nums = wj_unfinish.objects.filter(tracer=request.user.username).count()

        if total_num > 0 :
            # 判断是否达到上限
            if tracer_task_nums >= 5:
                messages.success(request, "最多可以领取5个任务")
            # 领取【优先的】【本机构】【且为自己专项或未指定过的】
            else:
                select_task = wj_unfinish.objects.filter(Q(tracer=None)&
                                                         Q(dpt_name=request.user.dpt1)&
                                                         (Q(counter_specify='')|Q(counter_specify=None)|Q(counter_specify=request.user.username))&
                                                         Q(is_pref='Y')).first()


                # addtask.id = select_task.id
                if select_task:
                    select(select_task)

                # 若没有【优先的】【本机构】【且为自己专项或未指定过的】 则领取【非优先的】【本机构】【个人指定或未指定的】
                else:
                    select_task = wj_unfinish.objects.filter(Q(tracer=None) &
                                                             Q(dpt_name=request.user.dpt1) &
                                                             (Q(counter_specify='') | Q(counter_specify=None))|Q(counter_specify=request.user.username)).first()


                    if select_task:
                        select(select_task)
                    # 若没有【非优先的】【本机构】【未指定过的任务】 则领取【优先的】【非本机构】【非人员指定】
                    else:
                        select_task = wj_unfinish.objects.filter(Q(tracer=None) &
                                                                 (Q(dpt_class=None)|Q(dpt_class="")) &
                                                                 (Q(counter_specify='') | Q(counter_specify=None))&
                                                                 Q(is_pref="")).first()


                        if select_task:
                            select(select_task)
                        # 若没有【非优先的】【非本机构】【非个人指定】 则领取【非优先的】【非本机构】【非人员指定】
                        else:
                            select_task = wj_unfinish.objects.filter(Q(tracer=None) &
                                                                     (Q(dpt_class=None) | Q(dpt_class="")) &
                                                                     (Q(counter_specify='') | Q(counter_specify=None))).first()

                            if select_task:
                                select(select_task)



        else:
            messages.success(request, "当前无回访任务")

        content = UnfinishView().get_content(request=request)

        return render(request, 'weijue-unfinish-list.html', content)



class test(View):
    def get(self,request):

        return render(request,'product-brand.html')
