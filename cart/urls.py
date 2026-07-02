from django.urls import path
from . import views

urlpatterns = [
    path('add/<slug:slug>/',views.add_to_cart,name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('',views.cart_view,name='cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path("address/main/<int:address_id>/",views.set_main_address,name="set_main_address"),
    path('coupon/apply/',views.apply_coupon,name='apply_coupon'),
    path('apply-coupon/', views.apply_discount, name='apply_coupon'),
]
