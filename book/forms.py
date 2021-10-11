from django import forms
from .models import *
from order.models import Coupon
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['created', 'updated', 'available']


class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['created', 'updated', 'available']


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['created', 'updated']


class CreateCashDiscountForm(forms.ModelForm):
    class Meta:
        model = CashDiscount
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CreateCashDiscountForm, self).__init__(*args, **kwargs)
        self.fields["start_date"] = JalaliDateField(label=('تاریخ شروع'), widget=AdminJalaliDateWidget)
        self.fields["end_date"] = JalaliDateField(label=('تاریخ پایان'), widget=AdminJalaliDateWidget)


class CreatePercentDiscountForm(forms.ModelForm):
    class Meta:
        model = PercentDiscount
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CreatePercentDiscountForm, self).__init__(*args, **kwargs)
        self.fields["start_date"] = JalaliDateField(label=('تاریخ شروع'), widget=AdminJalaliDateWidget)
        self.fields["end_date"] = JalaliDateField(label=('تاریخ پایان'), widget=AdminJalaliDateWidget)


