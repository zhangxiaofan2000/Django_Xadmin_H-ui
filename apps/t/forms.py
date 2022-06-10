from django import forms

from t.models import wj_finish,wj_unfinish

class SoundRecordForm(forms.ModelForm):

    class Meta:
        model = wj_unfinish
        fields = ['id', 'dpt_name', 'report_no', 'report_date', 'register_date', 'car_person',
                 'estimate_amount', 'car_amount', 'injured_amount', 'visited', 'tracer',
                  'visit_phone', 'wj_reason1', 'wj_reason2', 'wj_reason3', 'is_coupon', 'remake',
                  'update_time', 'finish_time', 'visited_phone', 'visit_dpt', 'visit_dpt2', 'num_issued',
                  'dpt_class', 'is_pref', 'counter_specify',
                  'sound_record'
                  ]

class FinshInfoForm(forms.ModelForm):
    class Meta:
        model = wj_finish
        fields = ['id', 'dpt_name', 'report_no', 'report_date', 'register_date','car_person',
                 'injured_person','estimate_amount','car_amount','injured_amount','visited','tracer',
                  'visit_phone','wj_reason1' ,'wj_reason2','wj_reason3', 'is_coupon','remake',
                  'update_time','finish_time','visited_phone','visit_dpt','visit_dpt2' ,'num_issued',
                  'dpt_class' ,'is_pref' ,'counter_specify' ,'event_type','complaint_risk' ,'case_closed',
                  'sound_record','tracering_date'
                  ]

