from django.urls import path, include
from ecomapp.views import home_page
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from ecomapp.views import (product_detail,
                           category_detail,
                           view_cart,
                           add_to_cart_view,
                           remove_from_cart_view,
                           change_item_qty,
                           checkout_view,
                           order_view,
                           )


urlpatterns = [
    path('', home_page, name='home'),
    path('product/<str:slug>', product_detail, name='product_detail_url'),
    path('product/<str:slug>', product_detail, name='product_detail_url'),
    path('add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('order/', order_view, name='order'),
    path('remove_from_cart/', remove_from_cart_view, name='remove_from_cart'),
    path('category/<str:slug>', category_detail, name='category_detail_url'),
    path('cart/', view_cart, name='cart'),
    path('change_item_qty/', change_item_qty, name='change_item_qty'),
]
