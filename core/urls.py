from django.urls import path 
from . import views
urlpatterns = [
    path('', views.home_page, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_us_view, name='about'),
    path('rules/', views.rules_view, name='rules')
]
