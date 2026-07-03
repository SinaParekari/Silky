from django.urls import path
from . import views
urlpatterns = [
    path('/payment/',views.OrderAPIView.as_view(),name='create_order_api')
]
