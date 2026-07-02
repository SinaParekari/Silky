from django.urls import path 
from . import views


urlpatterns = [
    path('get_categories/',views.all_categories_api,name='categories_api'),
    path('get_descendants_categories/<int:id>', views.get_descendants_categories,name='get-descendants-api')
]
