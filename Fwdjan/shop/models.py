from django.db import models
from django.urls import reverse

kat_name = None


def kategory_name():
    global kat_name
    if (not kat_name):
        kat_name = list(Shop_kategory.objects.order_by('kat_sort').values_list('kat_kod', 'kat_name'))
    return kat_name


def upload_location(instance, filename):
    return f"{instance.id}, {filename}"


class Shop_kategory(models.Model):
    kat_kod = models.CharField(max_length=5, unique=True, verbose_name="Код категорії")
    kat_name = models.CharField(max_length=100, verbose_name="Назва категорії")
    kat_sort = models.IntegerField(default=1, verbose_name="Порядок категорії")

    def __str__(self):
        return self.kat_name


class Shop_goods(models.Model):
    # good_kat = models.CharField(max_length=5, choices=kategory_name(), default='', verbose_name="Категорія товару")
    good_kat = models.ForeignKey(Shop_kategory, on_delete=models.PROTECT, to_field='kat_kod', default='1',
                                 related_name='ram', verbose_name="Категорія товару")
    good_name = models.CharField(max_length=150, verbose_name="Назва товару")
    good_opys = models.TextField(editable=True, default='', verbose_name="Детальний опис товару")
    good_price = models.DecimalField(default=0, decimal_places=2, max_digits=10, verbose_name="Вартість товару")
    good_link = models.URLField(editable=True, default='', verbose_name="Посилання на оригінальний товар:")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    date_update = models.DateTimeField(auto_now=True)
    good_image = models.ImageField(null=True, blank=True, height_field='height_field',
                                   width_field='width_field', upload_to=upload_location)

    def __str__(self):
        return self.good_name

    def get_absolute_url(self, tpp=1):
        return reverse('detail', kwargs={'good_id': self.pk})

    def get_absolute_url_1(self):
        return reverse('update', kwargs={'good_id': self.pk})
