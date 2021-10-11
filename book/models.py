from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.db import models
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    slug = models.SlugField(allow_unicode=True, unique=True, null=True, blank=True, verbose_name='اسلاگ')
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                                        related_name='categories', verbose_name='دسته بندی پدر')
    is_sub_category = models.BooleanField(default=False, verbose_name='زیر دسته')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book:category', args=[self.slug, self.id])


class PercentDiscount(models.Model):
    percent_amount = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='درصد تخفیف')
    max_discount = models.IntegerField(verbose_name='بیشترین مقدار')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع', null=True, blank=True)
    end_date = models.DateTimeField(verbose_name='تاریخ انقضا', null=True, blank=True)

    class Meta:
        verbose_name = 'تخفیف درصدی'
        verbose_name_plural = 'تخفیف های درصدی'

    def __str__(self):
        return f"{self.percent_amount}%"


class CashDiscount(models.Model):
    cash_amount = models.IntegerField(verbose_name='مقدار تخفیف (تومان)')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع', null=True, blank=True)
    end_date = models.DateTimeField(verbose_name='تاریخ انقضا', null=True, blank=True)

    class Meta:
        verbose_name = 'تخفیف نقدی'
        verbose_name_plural = 'تخفیف های نقدی'

    def __str__(self):
        return f" (T) {self.cash_amount} "


class Book(models.Model):
    title = models.CharField(max_length=500, verbose_name='عنوان')
    author = models.CharField(max_length=200, verbose_name='نویسنده')
    inventory = models.PositiveIntegerField(verbose_name='موجودی')
    available = models.BooleanField(default=True, verbose_name='موجود')
    unit_price = models.PositiveIntegerField(verbose_name='قیمت واحد')
    final_price = models.PositiveIntegerField(verbose_name='قیمت نهایی')
    percent_discount = models.ForeignKey(PercentDiscount, on_delete=models.SET_NULL, blank=True, null=True,
                                         verbose_name='تخفیف درصدی')
    cash_discount = models.ForeignKey(CashDiscount, on_delete=models.SET_NULL, blank=True, null=True,
                                      verbose_name='تخفیف نقدی')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    image = models.ImageField(upload_to='book/', verbose_name='تصویر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='بروزرسانی')
    category = models.ManyToManyField(Category, blank=True, verbose_name='دسته بندی')
    number_of_sell = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتابها'

    @property
    def final_price(self):
        """
        This method returns book's price with applying discount.
        The discount amount resulting the percentage discount should not exceed a certain amount.
        If the amount of the discount exceeds the initial price of the book, the original price
        of the book will be returned.
        """
        now = timezone.now()
        if self.percent_discount:
            cash_discount = (self.percent_discount.percent_amount / 100) * self.unit_price
            if cash_discount > self.percent_discount.max_discount:
                cash_discount = self.percent_discount.max_discount
        if not self.cash_discount and not self.percent_discount:
            return self.unit_price
        if not self.cash_discount and self.percent_discount:
            if self.percent_discount.start_date < now < self.percent_discount.end_date:
                return self.unit_price - cash_discount
        if not self.percent_discount and self.cash_discount:
            if self.cash_discount.start_date < now < self.cash_discount.end_date:
                x = self.unit_price - self.cash_discount.cash_amount
                if x > 0:
                    return x
                else:
                    return self.unit_price
        elif self.percent_discount.start_date < now < self.percent_discount.end_date and \
                self.cash_discount.start_date < now < self.cash_discount.end_date:
            x = self.unit_price - (cash_discount + self.cash_discount.cash_amount)
            if x > 0:
                return x
            else:
                return self.unit_price
        return self.final_price
