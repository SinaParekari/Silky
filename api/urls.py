from django.urls import path, include


urlpatterns = [
    path('category/', include('category.urls')),
    path('user/',include('user.urls')),
]
