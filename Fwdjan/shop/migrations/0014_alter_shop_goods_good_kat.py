# Generated by Django 4.0 on 2024-03-04 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0013_shop_kategory_shop_goods_date_update_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_goods',
            name='good_kat',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, related_name='ram',
                                    to='shop.shop_kategory', to_field='kat_kod', verbose_name='Категорія товару'),
        ),
    ]
