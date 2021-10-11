from django import forms
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from .models import Coupon


class CouponForm(forms.Form):
    code = forms.CharField(max_length=100)


class CreateCodeDiscountForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ('code', 'discount_percent', 'max_discount', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        super(CreateCodeDiscountForm, self).__init__(*args, **kwargs)
        self.fields["start_date"] = JalaliDateField(label=('تاریخ شروع'), widget=AdminJalaliDateWidget)
        self.fields["end_date"] = JalaliDateField(label=('تاریخ پایان'), widget=AdminJalaliDateWidget)
