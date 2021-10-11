from django.contrib import admin

from django.contrib import admin
from .models import *

# Register your models here.


class CategoryInlines(admin.TabularInline):
    model = Book.category.through
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_sub_category', 'parent_category')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_sub_category',)
    inlines = [CategoryInlines]


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'unit_price', 'inventory', 'available')
    list_editable = ('unit_price', 'inventory')
    search_fields = ['title', 'author']
    readonly_fields = ('number_of_sell', 'final_price',)
    fieldsets = (
        ('اطلاعات کلی', {
            'fields': (('title', 'author'), ('unit_price', 'inventory'), 'category')
        }),
        ('اطلاعات جزئی', {
            'classes': ('collapse',),
            'fields': ('image', 'percent_discount', 'cash_discount', 'description', 'available')
        }),
    )

    @admin.action(description='اعمال عدم موجودی برای کتابهای انتخاب شده')
    def make_available(self, request, queryset):
        queryset.update(available=False)
    actions = [make_available]


class CashDiscountAdmin(admin.ModelAdmin):
    list_display = ['cash_amount', 'start_date', 'end_date', ]
    list_filter = ('cash_amount',)
    list_display_links = ('cash_amount', )
    list_editable = ['start_date', 'end_date']
    fields = ('cash_amount', ('start_date', 'end_date'),)
    date_hierarchy = 'end_date'


class PercentDiscountAdmin(admin.ModelAdmin):
    list_display = ['percent_amount', 'start_date', 'end_date', 'max_discount']
    list_filter = ('percent_amount',)
    list_display_links = ('percent_amount',)
    list_editable = ['start_date', 'end_date']
    fields = (('percent_amount', 'max_discount'), ('start_date', 'end_date'))
    date_hierarchy = 'end_date'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(CashDiscount, CashDiscountAdmin)
admin.site.register(PercentDiscount, PercentDiscountAdmin)



