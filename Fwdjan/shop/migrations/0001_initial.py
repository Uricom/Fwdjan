# Generated by Django 4.0 on 2023-10-12 09:41

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='shop_goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('good_kat', models.CharField(max_length=10)),
                ('good_name', models.CharField(max_length=150)),
            ],
        ),
    ]
