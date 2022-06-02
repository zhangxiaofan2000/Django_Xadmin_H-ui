import xadmin


from t.models import wj_unfinish,wj_finish
from import_export import resources

class UnfinishRes(resources.ModelResource):

    class Meta:
        model = wj_unfinish
        skip_unchanged = True
        report_skipped = True
        # exclude = ('id',)
        fields = ('dpt_name','report_no','report_date','estimate_amount','event_type','id')
        # exclude = ()

class FinishRes(resources.ModelResource):

    class Meta:
        model = wj_finish
        skip_unchanged = True
        report_skipped = True
        # exclude = ('id',)
        # fields = ('name', 'description',)
        # exclude = ()




class UnfinishAdmin(object):

    import_export_args = {'import_resource_class': UnfinishRes,
                          'export_resource_class': UnfinishRes,}

    list_display = ['report_no', 'dpt_name','report_date','register_date','estimate_amount','event_type' ]

    exclude = ('report_no', 'dpt_name','report_date','register_date','estimate_amount','event_type')
    search_fields = ['report_no','event_type',]
    ordering = ['report_date']
    list_filter =['report_no', 'dpt_name','event_type','finish_time']
    model_icon = 'fa fa-square'
    readonly_fields = ['report_no', 'dpt_name','report_date','register_date','estimate_amount','event_type' ]

class FinishAdmin(object):

    import_export_args = {'import_resource_class': FinishRes, 'export_resource_class': FinishRes}

    list_display = ['report_no', 'dpt_name','report_date','register_date','estimate_amount','event_type','tracer','tracering_date','update_time','finish_time',]
    exclude = ['report_no', 'dpt_name','report_date','register_date','estimate_amount','event_type','tracer','tracering_date','update_time','finish_time']
    readonly_fields = ['report_no', 'dpt_name','report_date','register_date','estimate_amount','event_type','tracer','tracering_date','update_time','finish_time']
    ordering = ['report_date','event_type','tracer']
    search_fields = ['report_no']
    list_filter =['report_no', 'dpt_name','event_type','finish_time']
    model_icon = 'fa fa-check-square'


xadmin.site.register(wj_unfinish, UnfinishAdmin)
xadmin.site.register(wj_finish, FinishAdmin)
