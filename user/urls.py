from django.urls import path 
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.login_register_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('ajax/cities/', views.load_cities, name='load_cities'),
    path('api/register-api/', views.register_user_api, name='login_api'),
    path('api/login-api/', views.LoginAPIView.as_view(),name='login_api'),
    path('api/logout-api/', views.logout_api,name='logout_api'),
    path('api/address-api/',views.AddressAPIView.as_view(),name='address_api'),
    path('api/address-api/<int:address_id>',views.AddressAPIView.as_view(),name='address_api_delete'),
    path('api/profile-api/', views.get_user_profile_api, name='profile-api')
]
