from datetime import datetime
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from apps.grp.models import archive
from django.shortcuts import render

# Create your views here.





class UnfinishView(View):
    '''
    查看未完成团非车清单
    '''

    def get_content(self,request):

        # 获取权限
        hav_view_prem = False
        count = 0
        count = count + request.user.user_permissions.filter(codename='view_archive').count()
        for i in request.user.groups.all():
            count = count + i.permissions.filter(codename='view_archive').count()
        if count != 0:
            hav_view_prem = True

        search = request.GET.get('search')
        if search:
            all_tracer_task = archive.objects.filter(Q(policy_no=search)&Q(third_department_abbr_name=request.user.dpt1))
        else:
            all_tracer_task = archive.objects.filter(Q(is_return=None)&Q(third_department_abbr_name=request.user.dpt1))

        # 取数据
        nums = archive.objects.filter(tracer=None).count()
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

        return render(request, 'grp-unfinish-list.html', content)


    def post(self, request):

        content = self.get_content(request)

        # 验证表单
        post_task = archive.objects.get(policy_no=request.POST.get("policy_no"))

        post_task.is_return = "已归还"
        post_task.tracer = request.user.username
        post_task.tracer_dept = request.user.dpt1
        post_task.trace_date = datetime.now()
        post_task.return_material = post_task.material
        post_task.save()



        #
        #
        #
        # if finish_form.is_valid():
        #     finish_form.save()
        #     post_task.delete()
        #
        #
        # elif 'wj_reason1' in finish_form.errors.keys() :
        #     # messages.success(request,"请选择未决原因")
        #     content['error']='请选择未决原因'
        #     return render(request, 'grp-unfinish-list.html', content)
        #
        # elif 'case_closed' in finish_form.errors.keys() :
        #     # messages.success(request,"请选择结案类型")
        #     content['error'] = '请选择结案类型'
        #     return render(request, 'grp-unfinish-list.html', content)
        #
        # elif 'sound_record' in finish_form.errors.keys() :
        #     # messages.success(request, "请上传录音文件")
        #     content['error'] = '请上传录音文件'
        #     return render(request, 'grp-unfinish-list.html', content)
        #
        content['sucess_state'] = 'sucess'
        return render(request, 'grp-unfinish-list.html', content)
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
        count = count + request.user.user_permissions.filter(codename='view_archive').count()
        for i in request.user.groups.all():
            count = count + i.permissions.filter(codename='view_archive').count()
        if count != 0:
            hav_view_prem = True

        search = request.GET.get('search')
        if search:
            finish_task = archive.objects.filter(Q(tracer=request.user.username)&Q(policy_no=search)&Q(third_department_abbr_name=request.user.dpt1))

        else:
            finish_task = archive.objects.filter(Q(tracer=request.user.username)).order_by('-trace_date')

        # 取数据
        nums = archive.objects.filter(tracer=request.user.username).count()
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

        return render(request, 'grp-finish-list.html', content)