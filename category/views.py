from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from .serializers import CategorySerializer
from .models import Category

# Create your views here.

#region --------------------- API --------------------------------------------------------

@api_view(['GET'])
def all_categories_api(request : Request):
    if request.method == 'GET':
        category = Category.objects.all()
        Category_serializers = CategorySerializer(category, many=True)
        return Response(Category_serializers.data, status.HTTP_200_OK)

#endregion -------------------------------------------------------------------------------
