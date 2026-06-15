from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='shop'),
    path('product_detial/<slug>', views.product_detail_view, name='product_detail'), #need slug
]