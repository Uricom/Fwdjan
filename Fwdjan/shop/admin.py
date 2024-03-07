from django.contrib import admin

# Register your models here.
from shop.models import Shop_goods, Shop_kategory


class shop_goodsModelAdmin(admin.ModelAdmin):
    list_display = ('good_name', 'good_price', 'good_kat')
    list_display_links = ('good_name',)
    list_editable = ('good_price', 'good_kat',)
    list_filter = ('good_kat',)


class shop_kategoryModelAdmin(admin.ModelAdmin):
    list_display = ('kat_kod', 'kat_name', 'kat_sort')
    list_display_links = ('kat_name',)
    list_editable = ('kat_kod', 'kat_sort')
    list_filter = ('kat_kod',)


admin.site.register(Shop_goods, shop_goodsModelAdmin)
admin.site.register(Shop_kategory, shop_kategoryModelAdmin)
