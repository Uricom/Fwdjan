# Generated by Django 4.0 on 2023-10-12 10:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop_goods',
            name='good_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
