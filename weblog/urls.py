from django.urls import path
from . import views

urlpatterns = [
    path('',views.weblog,name='weblog'),
    path('single-post/',views.single_post,name='single-post'),
]


