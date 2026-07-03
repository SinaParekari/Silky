from django.shortcuts import render
from .services.order_service import OrderService
#rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import OrderSerializer
from rest_framework import status

# Create your views here.

#region ----------------------- API Views ------------------------------
class OrderAPIView(APIView):
    def get(self, request:Request):
        cart = request.user.cart.first()

        order = OrderService.create_from_cart(cart)

        serializer = OrderSerializer(order)

        return Response(serializer.data , status=status.HTTP_200_OK)

#endregion -------------------------------------------------------------
