# Generated by Django 4.0 on 2023-10-12 10:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0002_shop_goods_good_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop_goods',
            name='good_link',
            field=models.URLField(default=''),
        ),
    ]
