from django.urls import path 
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.login_register_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('ajax/cities/', views.load_cities, name='load_cities'),
    path('register-api/', views.register_user_api, name='login_api'),
    path('login-api/', views.LoginAPIView.as_view(),name='login_api'),
    path('logout-api/', views.logout_api,name='logout_api'),
    path('address-api/',views.AddressAPIView.as_view(),name='address_api'),
    path('address-api/<int:address_id>',views.AddressAPIView.as_view(),name='address_api_delete'),

]
