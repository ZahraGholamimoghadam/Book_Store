import urllib
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from account.mixins import *
from .models import *
from basket.models import Basket
from django.views.decorators.http import require_POST
from django.contrib import messages
from account.models import Address
from .forms import CouponForm
from book.models import Category
from django.utils import timezone
from .forms import CreateCodeDiscountForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

# Create your views here.


@login_required
def create_order(request):
    if request.method == "GET":
        addresses = Address.objects.filter(user=request.user)
        parent_categories = Category.objects.filter(is_sub_category=False)
        return render(request, 'order/select_address.html', {'addresses': addresses,
                                                             'parent_categories': parent_categories})
    else:
        # print(request.POST['address_pk'])
        address = Address.objects.get(pk=request.POST['address_pk'])
        order = Order.objects.create(user=request.user, address=address)
        baskets = Basket.objects.filter(user=request.user)
        """
        After creating order, shopping basket of the user will be removed.
        So we store shopping basket's information in the order item model.
        """
        for basket in baskets:
            order_item = OrderItem.objects.create(order_id=order.id, book_id=basket.book_id, quantity=basket.quantity)
            order_item.book.number_of_sell += order_item.quantity
            order_item.save()
        # Remove shopping basket after creating order.
        Basket.objects.filter(user=request.user).delete()
        return redirect('order:enter_discount_code', order.id)


def enter_discount_code(request, id):
    order = Order.objects.get(id=id)
    coupon_form = CouponForm()
    parent_categories = Category.objects.filter(is_sub_category=False)
    return render(request, 'order/enter_discount_code.html', {'order': order, 'coupon_form': coupon_form,
                                                        'parent_categories': parent_categories})


@require_POST
def apply_discount_code(request, id):
    coupon_form = CouponForm(request.POST)
    if coupon_form.is_valid():
        code = coupon_form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, start_date__lte=timezone.now(),
                                        end_date__gte=timezone.now())
        except Coupon.DoesNotExist:
            messages.error(request, 'کد وارد شده نامعتبر است و یا منقضی شده است', 'danger')
            return redirect('order:enter_discount_code', id)
        order = Order.objects.get(id=id)
        order.discount = coupon.discount_percent
        order.save()
    return redirect('order:enter_discount_code', order.id)


class CreateCodeDiscountView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    model = Coupon
    form_class = CreateCodeDiscountForm
    template_name = 'order/create_code_discount.html'
    success_url = reverse_lazy('book:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.filter(is_sub_category=False)
        return context
