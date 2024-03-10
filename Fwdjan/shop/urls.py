from django.urls import path

from shop.views import *

#    shop_start, shop_start_new, shop_k1, shop_create, show_detail, shop_update, shop_delete)

urlpatterns = [
    path('detail/<int:good_id>/', show_detail, name='detail'),
    path('update/<int:good_id>/', shop_update, name='update'),
    path('delete/<int:good_id>/', shop_delete, name='delete'),
    path('create/', shop_create, name='create'),
    path('login/', usr_login, name='login'),
    path('logout/', usr_logout, name='logout'),
    path('new/<str:kat_id>/', shop_start_new, name='new')
]
