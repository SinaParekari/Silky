from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='shop'),
    path('product_detial/<slug>', views.product_detail_view, name='product_detail'), #need slug
    path('add_review/<slug:slug>', views.add_review_view, name='add_review'),
    path('search', views.search_product, name='search_products'),
    path('search_category/<slug:slug>', views.search_product_by_category, name='search_category'),
    path('api/product-list-api/',views.ProductListAPIView.as_view(),name='product_list_api'),
    path('api/product-detail-api/<slug:slug>',views.ProductDetailAPIView.as_view(),name='product_detail_api'),

]
