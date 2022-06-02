import xadmin


from grp.models import archive
from import_export import resources

class GrpUnfinishRes(resources.ModelResource):

    class Meta:
        model = archive
        skip_unchanged = True
        report_skipped = True
        # exclude = ('id',)
        fields = ('id','policy_no','endorse_no','is_reverse','scene_name_list',
                  'planning_premium','third_department_abbr_name','fourth_department_abbr_name',
                  'channel_new','employee_name','employee_code',
                  'product_class_name','product_name','tbr_name',
                  'underwrite_date','material',)
        # exclude = ()


class GrpUnfinishAdmin(object):
    import_export_args = {'import_resource_class': GrpUnfinishRes,
                          'export_resource_class': GrpUnfinishRes,}

    list_display = ['policy_no','is_reverse',
                  'planning_premium', 'third_department_abbr_name','fourth_department_abbr_name',
                  'channel_new','employee_name',
                  'product_class_name','product_name','tbr_name',
                  'underwrite_date','material']

    search_fields = ['report_no', 'is_return', 'tracer']
    ordering = ['is_return']
    model_icon = 'fa fa-list'
    list_filter = ['is_return','policy_no', 'is_reverse', 'product_class_name', 'underwrite_date', 'trace_date']



xadmin.site.register(archive, GrpUnfinishAdmin)
