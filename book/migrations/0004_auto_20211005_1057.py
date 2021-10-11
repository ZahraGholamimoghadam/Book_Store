# Generated by Django 3.2.4 on 2021-10-05 07:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_auto_20210928_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashdiscount',
            name='cash_amount',
            field=models.IntegerField(verbose_name='مقدار تخفیف (تومان)'),
        ),
        migrations.AlterField(
            model_name='percentdiscount',
            name='percent_amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف'),
        ),
    ]
