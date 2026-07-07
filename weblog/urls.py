from django.urls import path
from . import views

urlpatterns = [
    path('',views.weblog,name='weblog'),
    path('single-post/<slug:slug>',views.single_post,name='single-post'),
    path("single-post/<slug:slug>/toggle-like/",views.toggle_weblog_like,name="toggle_weblog_like"),
    path("single-post/<slug:slug>/review/",views.submit_review,name="submit_review"),
    path('api/',views.WeblogListAPIView.as_view(),name="weblog_list_api"),
    path('single-post/api/<slug:slug>',views.WeblogDetailAPIView.as_view(),name='sinlge-post_api'),
    path('category/',views.CategoryAPIView.as_view(),name='weblog-category-api'),
    path('toggle-like/<slug:slug>',views.ToggleWebloglikeAPIView.as_view(),name="toggle-like-api"),
]


