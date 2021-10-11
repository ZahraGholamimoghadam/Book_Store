from django.urls import path, include
from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.basket_detail, name='basket_detail'),
    path('add/<int:id>', views.add_to_basket, name='add_to_basket'),
    path('remove/<int:id>', views.remove_from_basket, name='remove_from_basket'),
    path('increase_one_book/<int:id>', views.increase_one_book, name='increase_one_book'),
    path('decrease_one_book/<int:id>', views.decrease_one_book, name='decrease_one_book'),
]
