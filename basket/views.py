from django.shortcuts import render, redirect
from book.models import Book, Category
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='account:login')  # If the user is not logged in, she will be redirected to the login page
def basket_detail(request):
    baskets = Basket.objects.filter(user_id=request.user.id)
    user = request.user
    total_with_discount = 0
    total_discount_free = 0
    for basket in baskets:
        total_with_discount += basket.quantity * basket.book.final_price
        total_discount_free += basket.quantity * basket.book.unit_price
    parent_categories = Category.objects.filter(is_sub_category=False)
    return render(request, 'basket/basket_details.html', {'baskets': baskets, 'total_with_discount': total_with_discount,
                                                          'total_discount_free': total_discount_free, 'user': user,
                                                          'parent_categories': parent_categories})


@login_required(login_url='account:login')
def add_to_basket(request, id):
    url = request.META.get('HTTP_REFERER')  # for redirecting user to the current page
    if request.method == 'POST':
        form = BasketForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            object = Basket.objects.filter(user_id=request.user.id, book_id=id)
            if object:
                object = Basket.objects.get(user_id=request.user.id, book_id=id)
                object.quantity += quantity
                object.save()
            else:
                Basket.objects.create(book_id=id, user_id=request.user.id, quantity=quantity)
    return redirect('basket:basket_detail')


@login_required(login_url='account:login')
def remove_from_basket(request, id):
    url = request.META.get('HTTP_REFERER')
    Basket.objects.filter(id=id).delete()
    return redirect(url)


@login_required(login_url='account:login')
def increase_one_book(request, id):
    url = request.META.get('HTTP_REFERER')
    basket = Basket.objects.get(id=id)
    book = Book.objects.get(id=basket.book.id)
    if book.inventory > basket.quantity:
        basket.quantity += 1
    basket.save()
    return redirect(url)


@login_required(login_url='account:login')
def decrease_one_book(request, id):
    url = request.META.get('HTTP_REFERER')
    basket = Basket.objects.get(id=id)
    if basket.quantity == 1:
        basket.delete()
    else:
        basket.quantity -= 1
        basket.save()
    return redirect(url)
