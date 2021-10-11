from django.db import models
from .managers import CustomUserManager

# Create your models here.

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='تلفن همراه')
    email = models.CharField(max_length=300, unique=True, verbose_name='ایمیل')
    username = None
    USERNAME_FIELD = 'email'  # Unique identifier is set with email.
    REQUIRED_FIELDS = ['phone_number']  # Email is required by default.
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Customer(User):
    class Meta:
        proxy = True
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتری ها'

    def __str__(self):
        return self.email


class Staff(User):
    class Meta:
        proxy = True
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارمند ها'

    def __str__(self):
        return self.email


class Admin(User):
    class Meta:
        proxy = True
        verbose_name = 'مدیر'
        verbose_name_plural = 'مدیرها'

    def __str__(self):
        return self.email


class Address(models.Model):
    state = models.CharField(max_length=50, verbose_name='استان')
    city = models.CharField(max_length=40, verbose_name='شهر')
    address = models.TextField(max_length=300, verbose_name='ادامه آدرس')
    postal_code = models.IntegerField(verbose_name='کد پستی')
    is_default = models.BooleanField(default=False, verbose_name='آدرس پیش فرض')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'

    def __str__(self):
        return f"{self.state}-{self.city}-{self.address}"














