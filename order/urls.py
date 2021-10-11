from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('<int:id>/', views.enter_discount_code, name='enter_discount_code'),
    path('create_order/', views.create_order, name='create_order'),
    path('coupon/<int:id>/', views.apply_discount_code, name='coupon'),
    path('create_code_diacount/', views.CreateCodeDiscountView.as_view(), name='create_code_discount'),
]
