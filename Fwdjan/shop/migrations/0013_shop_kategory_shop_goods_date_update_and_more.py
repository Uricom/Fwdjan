# Generated by Django 4.0 on 2024-03-04 15:49

from django.db import migrations, models

import shop.models


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0012_alter_shop_goods_good_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop_kategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kat_kod', models.CharField(max_length=5, unique=True, verbose_name='Код категорії')),
                ('kat_name', models.CharField(max_length=100, verbose_name='Назва категорії')),
            ],
        ),
        migrations.AddField(
            model_name='shop_goods',
            name='date_update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='shop_goods',
            name='good_image',
            field=models.ImageField(blank=True, height_field='height_field', null=True,
                                    upload_to=shop.models.upload_location, width_field='width_field'),
        ),
        migrations.AlterField(
            model_name='shop_goods',
            name='good_kat',
            field=models.CharField(choices=[('1', 'Автомобільні шини та диски'), ('2', "Комп'ютери  та  ноутбуки"),
                                            ('3', 'Побутова хімія для дому'), ('4', 'Електроінструменти'),
                                            ('5', 'Побутова техніка')], default='', max_length=5,
                                   verbose_name='Категорія товару'),
        ),
    ]
