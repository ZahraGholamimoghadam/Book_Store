
from django.contrib import admin
from .models import *

# Register your models here.


class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'quantity']


admin.site.register(Basket, BasketAdmin)

