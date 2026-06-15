from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='shop'),
    path('product_detial/', views.product_detial_view, name='product_detail'), #need slug
]