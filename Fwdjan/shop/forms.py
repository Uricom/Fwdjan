from django import forms

from shop.models import Shop_goods


class Shop_form(forms.ModelForm):
    class Meta:
        model = Shop_goods
        fields = ['good_name', 'good_opys', 'good_price', 'good_link', 'good_kat', 'good_image']
        widgets = {'good_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'good_opys': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                   'good_price': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
                   'good_link': forms.TextInput(attrs={'class': 'form-control'}),
                   'good_kat': forms.Select(attrs={'class': 'form-control'})
                   }
