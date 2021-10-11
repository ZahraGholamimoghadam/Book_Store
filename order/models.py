from django.db import models
from account.models import User, Address
from book.models import *
from django.forms import ModelForm

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name='کاربر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت سفارش')
    status = models.CharField(max_length=20, default='سفارش', verbose_name='وضعیت')
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='آدرس')
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name='تخفیف')
    # discount=models.ForeignKey(Coupon, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    def __unicode__(self):
        return 'Policy: ' + self.name

    @property
    def total_price(self):
        """
         We use related name for getting all order_items related to this order.
        """
        total = sum(i.final_price() for i in self.order_items.all())
        if self.discount:
            return total - (self.discount / 100) * total
        return total

    def counting_order_items(self):
        order_items = self.order_items.all()
        return sum([order_item.quantity for order_item in order_items])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name='سفارش')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='کتاب')
    quantity = models.IntegerField(verbose_name='تعداد')
    # user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.order.user.email

    def user(self):
        return self.order.user

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم های سفارش'

    def final_price(self):
        return self.quantity * self.book.final_price


class Coupon(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name='کد تخفیف')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ انقضا')
    discount_percent = models.IntegerField(blank=True, null=True, verbose_name='درصد تخفیف')
    max_discount = models.IntegerField(verbose_name='بیشترین مقدار')

    class Meta:
        verbose_name = 'کوپن'
        verbose_name_plural = 'کوپن ها'

    def __str__(self):
        return f"{self.discount_percent}%"









