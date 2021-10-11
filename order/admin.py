from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter


# Register your models here.


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'book', 'quantity', 'get_final_price']
    readonly_fields = ['get_user', 'book', 'quantity', 'get_final_price']

    def get_user(self, obj):
        return obj.user()

    def get_final_price(self, obj):
        return obj.final_price()

    get_final_price.short_description = 'قیمت کل نهایی'  # For renaming column name.
    get_user.short_description = 'کاربر'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['get_user', 'book', 'quantity', 'get_final_price']

    def get_user(self, obj):
        return obj.user()

    def get_final_price(self, obj):
        return obj.final_price()

    get_final_price.short_description = 'قیمت کل نهایی'  # For renaming column name.
    get_user.short_description = 'کاربر'
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'status', 'get_total_price', 'address']
    readonly_fields = ['user', 'created', 'status', 'get_total_price', 'discount', 'address']

    def get_total_price(self, obj):
        return obj.total_price
    get_total_price.short_description = 'قیمت کل نهایی'

    inlines = [OrderItemInline]


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'start_date', 'end_date', 'discount_percent']
    fields = ('code', ('discount_percent', 'max_discount'), ('start_date', 'end_date'))
    list_editable = ['discount_percent', 'start_date', 'end_date']
    sortable_by = ['start_date', 'end_date', 'discount_percent']
    date_hierarchy = 'end_date'


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Coupon, CouponAdmin)
