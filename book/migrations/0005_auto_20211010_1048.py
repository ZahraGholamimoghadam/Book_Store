# Generated by Django 3.2.4 on 2021-10-10 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_auto_20211005_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='available',
            field=models.BooleanField(default=True, verbose_name='موجود'),
        ),
        migrations.AlterField(
            model_name='book',
            name='number_of_sell',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
