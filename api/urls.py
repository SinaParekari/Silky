from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [
    path('category/', include('category.urls')),
    path('user/',include('user.urls')),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('product/',include('product.urls'))
]
