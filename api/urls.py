from django.urls import path, include


urlpatterns = [
    path('category/', include('category.urls')),
    path('user/',include('user.urls')),
    path('product/',include('product.urls')),
    path('cart/',include('cart.urls')),
]
