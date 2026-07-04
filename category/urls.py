from django.urls import path 
from . import views


urlpatterns = [
    path('api/get_categories/',views.all_categories_api,name='categories_api'),
    path('api/get_descendants_categories/<int:id>', views.get_descendants_categories,name='get-descendants-api')
]
