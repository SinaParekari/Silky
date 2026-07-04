from django.urls import path
from . import views
urlpatterns = [
    path('api/payment/',views.OrderAPIView.as_view(),name='create_order_api')
]
