# Generated by Django 4.0 on 2024-03-06 15:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0015_shop_kategory_kat_sort'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_kategory',
            name='kat_sort',
            field=models.IntegerField(default=1, verbose_name='Порядок категорії'),
        ),
    ]