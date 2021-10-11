from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from basket.models import Basket
from order.models import Order
from book.models import PercentDiscount


# Register your models here.

class CustomerAddressInline(admin.StackedInline):
    model = Address
    fields = ['state', 'city', 'postal_code', 'is_default']
    readonly_fields = ['state', 'city', 'postal_code', 'is_default']
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'is_superuser', 'is_staff')
    search_fields = ('email',)
    inlines = [CustomerAddressInline]

    def get_queryset(self, request):
        return User.objects.filter(is_staff=False)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'is_superuser', 'is_staff')
    search_fields = ('email', )
    list_display_links = ('email',)
    list_editable = ('phone_number',)

    def get_queryset(self, request):
        return User.objects.filter(is_staff=True, is_superuser=False)


@admin.register(Admin)
class CustomAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'is_superuser', 'is_staff', 'password')
    search_fields = ('email',)
    list_editable = ('phone_number',)

    def get_queryset(self, request):
        return User.objects.filter(is_superuser=True)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'city', 'address', 'is_default')

    list_filter = ('state',)
    search_fields = ('city', 'state',)
















