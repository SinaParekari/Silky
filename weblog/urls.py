from django.urls import path
from . import views

urlpatterns = [
    path('',views.weblog,name='weblog'),
    path('single-post/<slug:slug>',views.single_post,name='single-post'),
    path("single-post/<slug:slug>/toggle-like/",views.toggle_weblog_like,name="toggle_weblog_like"),
    path("single-post/<slug:slug>/review/",views.submit_review,name="submit_review")
]


