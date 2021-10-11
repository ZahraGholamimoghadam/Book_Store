from django.db import models
from book.models import *
from account.models import User
from django.forms import ModelForm


# Create your models here.

class Basket(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='کتاب')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    quantity = models.PositiveIntegerField(verbose_name='تعداد')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'


class BasketForm(ModelForm):
    class Meta:
        model = Basket
        fields = ['quantity']
