# Generated by Django 4.0 on 2024-03-06 15:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0014_alter_shop_goods_good_kat'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop_kategory',
            name='kat_sort',
            field=models.IntegerField(default=1),
        ),
    ]
