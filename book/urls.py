from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.all_books, name='home'),
    # path('parent_categories', views.parent_categories, name='parent_categories'),
    path('all_books/', views.all_books, name='all_books'),
    path('details/<int:id>/', views.book_details, name='details'),
    path('categoty/<slug>/<int:id>', views.all_books, name='category'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('create_book/', views.CreateBookView.as_view(), name='create_book'),
    path('edit_book/<int:pk>/', views.EditBookView.as_view(), name='edit_book'),
    path('delete_book/<int:pk>/', views.DeleteBookView.as_view(), name='delete_book'),
    path('create_category/', views.CreateCategoryView.as_view(), name='create_category'),
    path('create_cash_diacount/', views.CreateCashDiscountView.as_view(), name='create_cash_discount'),
    path('create_percent_diacount/', views.CreatePercentDiscountView.as_view(), name='create_percent_discount'),
    path('most_selling_books/', views.most_selling_books, name='most_selling_books'),
]
